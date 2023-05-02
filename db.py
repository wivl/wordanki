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

from tinydb import TinyDB, Query
import json

dictionary = TinyDB('./db/dict.json')

filenames = ['./dict/KaoYan_2.json', './dict/CET4luan_2.json', './dict/CET6_2.json', './dict/Level8_2.json']


if __name__ == '__main__':
    for filename in filenames:
        file = open(filename,'r',encoding='utf-8')
        for line in file.readlines():
            words = line.strip()
            word_json = json.loads(words)
            Word = Query()
            if len(dictionary.search(Word.headWord == word_json['headWord'])) != 0:
                continue
            dictionary.insert(word_json)
    
        file.close()
