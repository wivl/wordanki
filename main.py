import genanki
from tinydb import TinyDB, Query

import sys, getopt

listdb = TinyDB('./db/words.json')

dictdb = TinyDB('./db/dict.json')

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
                'qfmt': '{{Word}}<br>{{SentenceEn}}',
                'afmt': '{{FrontSide}}<br>{{SentenceZh}}<br id="answer">{{Meaning}}'
                },
            ])

WordDeck = genanki.Deck(
    2054490786,
    'Words')


def new_word(word):
    Word = Query()
    if len(listdb.search(Word.word == word)) == 0:
        listdb.insert({'word': word})
        print('Word ' + word + ' inserted' + ', ' + str(len(listdb.all())) + ' words in total.')
    else:
        print('Word ' + word + ' already exists, skipping.')


def make_notes():
    notes = []
    words = listdb.all()
    Dict = Query()
    if len(words) != 0:
        for word in words:
            item = dictdb.search(Dict.headWord == word['word'])
            print(len(item))
            if len(item) == 0:
                print('Word ' + word['word'] + ' is not in current dictionary, skipping.')
                exit(1)


            content = []
            # 单词
            content.append(item[0]['headWord'])
            # 英句
            content.append(item[0]['content']['word']['content']['sentence']['sentences'][0]['sContent'])
            # 中句
            content.append(item[0]['content']['word']['content']['sentence']['sentences'][0]['sCn'])
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
    

def gen_deck(deck, notes):
    if len(notes) == 0:
        print('Notes list is empty, skipping.')
    else:
        for note in notes:
            deck.add_note(note)
        genanki.Package(deck).write_to_file('output.apkg')




def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ha:g")
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('TODO, help')
            sys.exit()
        elif opt == '-a':
            new_word(arg)
        elif opt == '-g':
            print('TODO, generate anki deck')
            notes = make_notes()
            gen_deck(WordDeck, notes)
        else:
            print('TODO, unknown opt and print help')
            

if __name__ == '__main__':
    main(sys.argv[1:])
