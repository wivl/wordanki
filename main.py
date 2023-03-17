"""
The MIT License (MIT)

Copyright (c) 2023 wivl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import genanki
from tinydb import TinyDB, Query

import sys, getopt

listdb = TinyDB('./db/words.json')

dictdb = TinyDB('./db/dict.json')

CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
"""

# Card model
WordCard = genanki.Model(
        1276008402,
        "Card Model",
        fields=[
            {'name': 'Word'},
            {'name': 'SentenceEn'},
            {'name': 'SentenceZh'},
            {'name': 'Meaning'},
            ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<br><br>{{Word}}<br><br><br>{{SentenceEn}}',
                'afmt': '{{FrontSide}}<br><br>{{SentenceZh}}<br><br><br id="answer">{{Meaning}}'
                },
            ],
        css=CSS
        )

# deck model
WordDeck = genanki.Deck(
    2054490786,
    'Words')


# Add word to listdb
def new_word(word):
    Word = Query()
    if len(listdb.search(Word.word == word)) == 0:
        listdb.insert({'word': word})
        print('Word "' + word + '" inserted' + ', ' + str(len(listdb.all())) + ' words in total.')
    else:
        print('Word "' + word + '" already exists, skipping.')


# Go through listdb and generate a list of NOTES
def make_notes():
    notes = []
    words = listdb.all()
    Dict = Query()
    if len(words) != 0:
        for word in words:
            item = dictdb.search(Dict.headWord == word['word'])
            if len(item) == 0:
                print('Word "' + word['word'] + '" is not in current dictionary, skipping.')
                continue
            
            print('Adding word "' + word['word'] + '"...')


            content = []
            # 单词
            content.append(item[0]['headWord'])
            # 英句
            if 'sentence' in item[0]['content']['word']['content'].keys():

                content.append(item[0]['content']['word']['content']['sentence']['sentences'][0]['sContent'])
            # 中句
                content.append(item[0]['content']['word']['content']['sentence']['sentences'][0]['sCn'])
            else:
                content.append('<br>')
                content.append('<br>')
            # 词性
            # 意思
            meaning_str = ''
            for con in item[0]['content']['word']['content']['trans']:
                meaning_str += con['pos']
                meaning_str += ' '
                meaning_str += con['tranCn']
                meaning_str += ' '
            content.append(meaning_str)

            note = genanki.Note(
                    model=WordCard,
                    fields=content
                    )
            notes.append(note)
    else:
        print('The list is empty, skipping.')

    return notes
    

# Using list of NOTES to generate deck and save
def gen_deck(deck, notes):
    if len(notes) == 0:
        print('Notes list is empty, skipping.')
    else:
        for note in notes:
            deck.add_note(note)
        genanki.Package(deck).write_to_file('output.apkg')

def print_help():
    print('Usage: python3 main.py [opt] <arg>')
    print('\tOptions:')
    print('\t\t-h print this help')
    print('\t\t-a <word> required, add a word to list')
    print('\t\t-g generate word deck using current list')
    print('\t\t-r <filepath> required, read text file and write them to listdb')



def main(argv):
    if len(sys.argv) <= 1:
        print('len < 1')
        print_help()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(argv,"hga:r:")
    except getopt.GetoptError:
        print_help()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()

        elif opt == '-a':
            new_word(arg)
            sys.exit()

        elif opt == '-g':
            notes = make_notes()
            gen_deck(WordDeck, notes)
            sys.exit()

        elif opt == '-r':
            filename = arg
            with open(filename) as fin:
                for line in fin.readlines():
                    word = line.strip()
                    new_word(word)
                    
        else:
            print('[ERROR] Unknown option "' + opt + '"')
            print_help()
            

if __name__ == '__main__':
    main(sys.argv[1:])
