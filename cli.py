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



    print(box[8] +  box[0] * (cols - 2) + box[10])


def text_adjust(text, width):
    if len(text) < width:
        return [text + ' ' * (width - len(text))]
    else:
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


if __name__ == '__main__':

    word = ['Incipient means something is in an early stage of existence. In its incipient form, basketball was played with a soccer ball and peach baskets for goals. Bouncy orange balls and nets came later.',
            'Incipient comes from the Latin incipere "to begin." The related, and more commonly used, word inception means the beginning or the start. It is important to note that when something is in an incipient stage, there is a chance it will never come to completion. So be on the lookout for incipient trouble or an incipient crisis — you might be able to prevent it from happening.',
            '[noun] only partly in existence; imperfectly formed']
    flashcard(word, title='incipient', style=0)

    ctrlseq = '\033[1maaa\033[0m'
    print(ctrlseq)
    print(len(ctrlseq))