from HelperClass import Trie
import sys
import string
import pickle
import json
import shutil
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Run with the following: \n python3 query.py $string_1")
        sys.exit(0)

    search_string = sys.argv[1]

    dict_reuters = dict()
    trie = Trie()

    '''
    Ppen the created 'inverted_index.json' and 'trie.pickle' files and fill in the 
    'dict_reuters' and 'trie' data structures.
    '''
    with open('inverted_index.json') as f:
        dict_reuters = json.load(f)

    with open('trie.pickle', 'rb') as f:
        trie = pickle.load(f)

    trie.search(search_string)

    index = set()

    for elem in trie.list_search:
        for id_for in dict_reuters[elem]:
            index.add(id_for)

    index = list(index)
    index.sort()

    with open('output.txt', 'w') as f:
        for enum, item in enumerate(index):
            f.write("%d " % item)
            # if enum != 0 and enum % 30 == 0: f.write("\n")

    print(index)


