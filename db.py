from tinydb import TinyDB, Query
import json

dictionary = TinyDB('./db/dict.json')

filenames = ['./dict/KaoYan_1.json', './dict/KaoYan_2.json', './dict/KaoYan_3.json']


if __name__ == '__main__':
    for filename in filenames:
        file = open(filename,'r',encoding='utf-8')
        for line in file.readlines():
            words = line.strip()
            word_json = json.loads(words)
            dictionary.insert(word_json)
    
        file.close()
