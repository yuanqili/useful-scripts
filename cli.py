from __future__ import print_function
import re
import sys
import os
import terminalsize


def flashcard(texts, title='', footnote='', style=0):
    boxes = ['─│┌┬┐├┼┤└┴┘', '═║╔╦╗╠╬╣╚╩╝', '']
    box = boxes[style]
    symbols = '✔︎✗◇❖◎◉●✺'

    # cols, rows = os.get_terminal_size(0)
    cols, rows = terminalsize.get_terminal_size()

    print(box[2], end='')
    if title == '':
        print(box[0] * (cols - 2) + box[4])
    else:
        print('(' + title + ')' + box[0] * (cols - 4 - len(title)) + box[4])

    for text in texts:
        strs = text_adjust(text, cols - 4)
        print(box[1] + ' ' * (cols - 2) + box[1])
        for i in range(len(strs)):
            if i == 0:
                print(box[5] + symbols[3] + ' ' + strs[i] + box[1])
            else:
                print(box[1] + ' ' * 2 + strs[i] + box[1])

    print(box[8] + box[0] * (cols - 2) + box[10])


def text_adjust(text, width):
    if text == '':
        return []
    if len(text) < width:
        return [text + ' ' * (width - len(text))]
    text = text.split()
    linelen = 0
    ret = []
    line = ''
    for word in text:
        if linelen + len(word) + 1 > width:
            ret.append(line + ' ' * (width - linelen))
            line = word + ' '
            linelen = len(word) + 1
        else:
            line += word + ' '
            linelen += len(word) + 1
    ret.append(line + ' ' * (width - linelen))
    return ret


def terminal_size():
    return terminalsize.get_terminal_size()


palette = {
    'black': '\033[30m',
    'red': '\033[91m',
    'green': '\033[32m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'pink': '\033[95m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'gray': '\033[37m',
    'default': '\033[0m',
}

highlighter = {
    'black': '\033[40m',
    'red': '\033[101m',
    'green': '\033[102m',
    'yellow': '\033[103m',
    'blue': '\033[104m',
    'pink': '\033[105m', 'magenta': '\033[105m',
    'cyan': '\033[106m',
    'white': '\033[107m',
    'gray': '\033[47m',
}

formatter = {
    'default': '\033[0m',
    'bold': '\033[1m',
    'faint': '\033[2m',
    'italic': '\033[3m',        # Doesn't work on Ubuntu/Mac terminal.
    'underline': '\033[4m',
    'blinking': '\033[5m',
    'fast_blinking': '\033[6m', # Doesn't work on Ubuntu/Mac terminal.
    'reverse': '\033[7m',       # Note: This reverses the back-/foreground color.
    'hide': '\033[8m',
    'strikethrough': '\033[9m', # Doesn't work on Ubuntu/Mac terminal.
}


def color_print(s, color=None, highlight=None, end='\n', file=sys.stdout,
                **kwargs):
    if color in palette and color != 'default':
        s = palette[color] + s
    # Highlight / Background color.
    if highlight and highlight in highlighter:
        s = highlighter[highlight] + s
    # Custom string format.
    for name, value in kwargs.items():
        if name in formatter and value:
            s = formatter[name] + s
    print(s + palette['default'], end=end, file=file)


def color_str(s, color=None, highlight=None, **kwargs):
    if color in palette and color != 'default':
        s = palette[color] + s
    # Highlight / Background color.
    if highlight and highlight in highlighter:
        s = highlighter[highlight] + s
    # Custom string format.
    for name, value in kwargs.items():
        if name in formatter and value:
            s = formatter[name] + s
    return s + palette['default']


if __name__ == '__main__':

    word = ['Incipient means something is in an early stage of existence. In its incipient form, basketball was played with a soccer ball and peach baskets for goals. Bouncy orange balls and nets came later.',
            'Incipient comes from the Latin incipere "to begin." The related, and more commonly used, word inception means the beginning or the start. It is important to note that when something is in an incipient stage, there is a chance it will never come to completion. So be on the lookout for incipient trouble or an incipient crisis — you might be able to prevent it from happening.',
            '[noun] only partly in existence; imperfectly formed']

    flashcard(word, title='incipient', style=0)
