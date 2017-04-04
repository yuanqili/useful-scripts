#!/usr/local/bin/python3

from bs4 import BeautifulSoup as bs, element
import requests
import sys
from os import system
import json
import fileinput

from spritz import spritz

url = 'https://www.vocabulary.com/dictionary/'
lexeme = 'accrete'


class Word(object):

    __slots__ = ('lexeme', 'blurb', 'definition', 'example', 'origin')

    def __init__(self, lexeme):
        self.lexeme = lexeme
        self.blurb = {}
        self.definition = []
        self.example = []

        html = requests.get(url + lexeme)
        if html.status_code != 200:
            print('fail to retrieve definition: ' + lexeme)
        soup = bs(html.content, 'html.parser')
        vocab = soup.find('div', {'class': 'definitionsContainer'})
        if vocab is None:
            print('Cannot find word', lexeme)
            return

        # add short and long explanations
        self.blurb = {'short': '', 'long': ''}
        try:
            short = vocab.find('p', {'class': 'short'}).contents
        except AttributeError:
            pass
        else:
            self.blurb['short'] = ''.join(map(lambda x: x.contents[0] if type(x) == element.Tag else x, short))
        try:
            long = vocab.find('p', {'class': 'long'}).contents
        except AttributeError:
            pass
        else:
            self.blurb['long'] = ''.join(map(lambda x: x.contents[0] if type(x) == element.Tag else x, long))

        # add definitions
        defs = vocab.find_all('div', {'class': 'sense'})
        for defi in defs:
            temp = {'pos': defi.h3.a.attrs['title'], 'meaning': defi.h3.contents[2].strip(), 'synonym': []}
            if defi.dt.contents[0] == 'Synonyms:':
                temp['synonym'] = list(map(lambda x: x.contents[0], defi.dd.find_all('a')))
            self.definition.append(temp)

    def show(self):
        print('\033[1m' + self.lexeme + '\033[0m')
        if self.blurb['short'] != '':
            print(self.blurb['short'])
        if self.blurb['long'] != '':
            print('\033[2m' + self.blurb['long'] + '\033[0m')
        for i in self.definition:
            print('\033[32m' + i['pos'] + '\033[0m', i['meaning'])

if __name__ == '__main__':

    # review mode
    if len(sys.argv) == 2 and sys.argv[1] == '-r':
        words = ''
        for line in fileinput.input(sys.argv[2:]):
            words += line
        spritz(200, words, True)

    # learn mode
    for line in fileinput.input(sys.argv[2:]):
        Word(line.strip()).show()
        system('say ' + line.strip())
        print()