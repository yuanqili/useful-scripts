#!/usr/local/bin/python3

from tinydb import TinyDB
import kmf
import dict
import cli

if __name__ == '__main__':
    db = TinyDB('vocabulary.json')
    lexeme = input()

    while lexeme != '':
        print()

        try:
            kmf.kmf_definition(lexeme)
            print()
        except:
            pass

        word = dict.Word(lexeme, db)
        print(word.short, end='\n\n')
        print(word.long)
        print('=' * cli.terminal_size()[0])

        lexeme = input()