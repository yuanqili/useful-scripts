#!/usr/local/bin/python3

from bs4 import BeautifulSoup as bs
import requests
import sys

kmf_com = 'http://gre.kmf.com/vocab/detail/'


def kmf_definition(lexeme):

    # request definition
    kmf_html = requests.get(kmf_com + lexeme)
    if kmf_html.status_code != 200:
        return
    kmf_soup = bs(kmf_html.content, 'html.parser')
    kmf_vocab = kmf_soup.find('span', {'class': 'word-d-word'})
    if kmf_vocab is None:
        return
    kmf_meanings = kmf_soup.find('div', {'class': 'word-g-translate'}).contents[1:]

    # dirty parsing work
    texts = []
    for node in kmf_meanings:
        try:
            texts.append(node.text)
        except AttributeError:
            texts.append(node.string)

    for i in range(len(kmf_meanings)):
        if kmf_meanings[i].name == 'p':
            print('\n【' + texts[i][0] + '】' + texts[i][1:], end='')
        else:
            print(texts[i], end='')
        if i+1 < len(kmf_meanings) and kmf_meanings[i+1].name == 'b':
            print('\n')

if __name__ == '__main__':
    kmf_definition(sys.argv[1])
