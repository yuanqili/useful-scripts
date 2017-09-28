#!/usr/local/bin/python3

from bs4 import BeautifulSoup as bs
from bs4 import element
import re
import requests
import os
import fileinput
import argparse

import cli
from tinydb import TinyDB, Query


class Word(object):
    """
    A Word object contains its definition and related information.
    """

    # API address
    vocabulary_com = 'https://www.vocabulary.com/dictionary/'
    youdao_com = 'http://dict.youdao.com/w/eng/'
    kmf_com = 'http://gre.kmf.com/vocab/detail/'

    def __init__(self, lexeme, db):
        self.lexeme = lexeme
        self.long = ''
        self.short = ''
        self.definition = []
        self.usage = []

        # if the word is already cached, return
        word_cache = db.search(Query().lexeme == lexeme)
        if len(word_cache) == 1:
            self.long = word_cache[0]['long']
            self.short = word_cache[0]['short']
            self.definition = word_cache[0]['definition']
            return

        # download word definition from vocabulary.com
        html = requests.get(Word.vocabulary_com + lexeme)
        if html.status_code != 200:
            return
        soup = bs(html.content, 'html.parser')
        vocab = soup.find('div', {'class': 'definitionsContainer'})
        if vocab is None:
            return

        # add short and long explanations
        try:
            short = vocab.find('p', {'class': 'short'}).contents
            self.short = ''.join(map(lambda x: x.contents[0] if type(x) == element.Tag else x, short))
        except AttributeError:
            pass
        try:
            long = vocab.find('p', {'class': 'long'}).contents
            self.long = ''.join(map(lambda x: x.contents[0] if type(x) == element.Tag else x, long))
        except AttributeError:
            pass

        # add English definitions
        defs = vocab.find_all('div', {'class': 'sense'})
        for d in defs:
            try:
                temp = {'pos': d.h3.a.attrs['title'], 'meaning': d.h3.contents[2].strip(), 'synonym': []}
                if d.dt.contents[0] == 'Synonyms:':
                    temp['synonym'] = list(map(lambda x: x.contents[0], d.dd.find_all('a')))
                self.definition.append(temp)
            except AttributeError:
                pass

        # cache the word
        db.insert({'lexeme': self.lexeme,
                   'long': self.long,
                   'short': self.short,
                   'definition': self.definition})

    def show(self, light=False, detail=True):
        print(cli.color_str(self.lexeme, bold=True, underline=True, italic=True))
        if light is False:
            for line in cli.text_adjust(self.short, cli.terminal_size()[0]):
                print(line)
            for line in cli.text_adjust(self.long, cli.terminal_size()[0]):
                print(cli.color_str(line, faint=True))
        if detail is True:
            for i in self.definition:
                print(cli.color_str(i['pos'], color='green'), end=' ')
                print(i['meaning'])


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--silent", action="store_true",
                        help="silent mode, no word voice")
    parser.add_argument("-L", "--light", action="store_true",
                        help="light mode, no long definitions")
    parser.add_argument("-l", "--list",
                        help="list mode, followed by a line-striped word-list file. Any other arguments are ignored")
    parser.add_argument("-a", "--auto", action="store_true",
                        help="auto mode, display all words at once, no voice")
    parser.add_argument("words", nargs="*",
                        help="word to be searched, conflicted with list mode")
    args = parser.parse_args()

    db = TinyDB('vocabulary.json')

    # review mode: not so useful, disabled currently
    # if len(sys.argv) == 3 and sys.argv[1] == '-r':
    #     words = ''
    #     for line in fileinput.input(sys.argv[2:]):
    #         words += line
    #     spritz(200, words, True)

    source = args.words
    if args.list is not None:
        for line in fileinput.input(args.list):
            source.append(line.strip())

    for word in source:
        Word(word, db).show(args.light)
        if not args.auto and not args.silent:
            os.system('say ' + word)
        print()
