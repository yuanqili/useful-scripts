#!/usr/local/bin/python3

from tinydb import TinyDB, Query
import dict
import cli
import datetime

if __name__ == '__main__':
    dictionary_db = TinyDB('vocabulary.json')
    wordlist_db = TinyDB('wordlist.json')

    lexeme = input().strip()
    while lexeme != '':
        # cache search history
        word_history = wordlist_db.search(Query().lexeme == lexeme)
        if len(word_history) == 1:
            wordlist_db.remove(Query().lexeme == lexeme)
            wordlist_db.insert({'lexeme': lexeme,
                                'query_times': word_history[0]['query_times'] + 1,
                                'last_query': datetime.datetime.now().isoformat()})
        else:
            wordlist_db.insert({'lexeme': lexeme,
                                'query_times': 1,
                                'last_query': datetime.datetime.now().isoformat()})
        # show definition
        print()
        word = dict.Word(lexeme, dictionary_db)
        word.show()
        print('=' * cli.terminal_size()[0])
        lexeme = input()
