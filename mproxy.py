import argparse
import socket
import functools
import logging
import select

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Connection(object):
    """TCP server/client connection abstraction."""

    def __init__(self, what):
        self.buffer = b''
        self.closed = False
        self.what = what  # server or client

    def send(self, data):
        return self.conn.send(data)

    def recv(self, bytes=8192):
        try:
            data = self.conn.recv(bytes)
            if len(data) == 0:
                logger.debug('recvd 0 bytes from %s' % self.what)
                return None
            logger.debug('rcvd %d bytes from %s' % (len(data), self.what))
            return data
        except Exception as e:
            logger.exception(
                'Exception while receiving from connection %s %r with reason %r' % (self.what, self.conn, e))
            return None

    def close(self):
        self.conn.close()
        self.closed = True

    def buffer_size(self):
        return len(self.buffer)

    def has_buffer(self):
        return self.buffer_size() > 0

    def queue(self, data):
        self.buffer += data

    def flush(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        logger.debug('flushed %d bytes to %s' % (sent, self.what))


class Server(Connection):
    """Establish connection to destination server."""

    def __init__(self, host, port):
        super(Server, self).__init__(b'server')
        self.addr = (host, int(port))

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.addr[0], self.addr[1]))


class Client(Connection):
    """Accepted client connection."""

    def __init__(self, conn, addr):
        super(Client, self).__init__(b'client')
        self.conn = conn
        self.addr = addr


class Proxy(object):

    def __init__(self, client):
        self.client = client
        self.server = None
        self.request = HTTPRequestHandler()
        self.response = HTTPResponseHandler()
        self.timeout = 5

    def run(self):
        try:
            self._process()
        except Exception as e:
            logger.exception('Exception when running the server {}'.format(e))
        finally:
            self.client.close()

    def _process(self):
        while True:
            rlist, wlist, xlist = self._get_waitable_lists()
            rl, wl, xl = select.select(rlist, wlist, xlist, self.timeout)

            self._process_wlist(wl)
            if self._process_rlist(rl):
                break

    def _get_waitable_lists(self):
        rlist, wlist, xlist = [self.client.conn], [], []
        if self.client.has_buffer():
            wlist.append(self.client.conn)
        if self.server and not self.server.closed:
            rlist.append(self.server.conn)
        if self.server and not self.server.closed and self.server.has_buffer():
            wlist.append(self.server.conn)







class HTTPConnection(object):

    def __init__(self, host, port, backlog):
        self.host, self.port, self.backlog = host, port, backlog

    def handle(self, client):
        proc = Proxy(client)
        proc.daemon = True
        proc.start()
        logger.debug('Started process {} to handle connection {}'.format(proc, client.conn))

    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(self.backlog)
            while True:
                conn, addr = self.socket.accept()
                client = Client(conn, addr)
                self.handle(client)
        except Exception as e:
            logger.exception('Exception when running the server {}'.format(e))
        finally:
            logger.info('Closing server socket')
            self.socket.close()


def main():
    parser = argparse.ArgumentParser()

    host, port = parser.hostname, parser.port
    Proxy(host, port).run()