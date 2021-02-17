from HelperClass import Trie
import sys
import string
import pickle
import json
import shutil
import os

'''
    'parse_reuters_first', 'parse_reuters_last', 'parse_article_id', 'parse_title_first', 
    'parse_title_last', 'parse_body_first' and 'parse_body_last' variables provide the 
    values necessary to perform parse operations.
'''
parse_reuters_first = "<REUTERS"
parse_reuters_last = "</REUTERS>"
parse_article_id = "NEWID=\""
parse_title_first = "<TITLE>"
parse_title_last = "</TITLE>"
parse_body_first = "<BODY>"
parse_body_last = "</BODY>"

'''
    The 'find_str' function returns the starting index or the last index with the control 
    parameter, which is the boolean expression, whether there is a string sent as 'char' 
    in the 's' parameter and the its index.
'''
def find_str(s, char, control) -> int:
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    if control:
                        return index+len(char)
                    else:
                        return index

            index += 1

    return -1


'''
    The 'get_reuters_index' function finds the start and last index of the 'REUTERS' 
    tag.
'''
def get_reuters_index(text) -> None:
    global start_index, last_index
    start_index = find_str(text, parse_reuters_first, True)
    last_index = find_str(text, parse_reuters_last, True)
    

'''
    The 'get_reuters_index' function finds the start and last index of the 'NEWID' 
    tag and also finds 'article_id'.
'''
def get_article_id(text) -> None:
    global article_id
    start = find_str(text, parse_article_id, True)
    last = 0
    for i in range(start, sys.maxsize):
        if text[i] == "\"":
            last = i
            break
    article_id = int(' '.join(text[start:last].split()))


'''
    The 'get_title' function finds the start and last index of the 'TITLE' tag and 
    also finds 'title'.
'''
def get_title(text) -> None:
    start = find_str(text, parse_title_first, True)
    if start == -1: pass
    else:
        last = find_str(text, parse_title_last, False)
        title = removal_utilities(text[start:last])
        fill_dict(elem=title)


'''
    The 'get_body' function finds the start and last index of the 'BODY' tag and 
    also finds 'body'.
'''
def get_body(text) -> str:
    start = find_str(text, parse_body_first, True)
    if start == -1: pass
    else:
        last = find_str(text, parse_body_last, False)
        body = removal_utilities(text[start:last])
        fill_dict(elem=body)


'''
    The 'removal_utilities' function removes punctuation marks, lowers all characters, 
    and also removes all stopwords from the given parameter.
'''
def removal_utilities(text) -> set:
    elem = set(list(map(str.casefold, text.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation))).split())))
    elem = elem - (elem & text_stopwords)
    return elem


def fill_dict(elem) -> None:
    for word in elem:
        if word not in dict_reuters:
            dict_reuters[word] = set([article_id])
        else:
            dict_reuters[word].add(article_id)



if __name__ == "__main__":
    global dict_reuters, text_stopwords
    dict_reuters = dict()
    trie = Trie()

    directory = "reuters21578/"

    '''
    Putting all the words in 'stopwords.txt' into a set.
    '''
    file_name_stopwords = "stopwords.txt"
    f = open(file=file_name_stopwords, mode='r')
    text_stopwords = set(f.read().split())
    f.close()

    '''
    In order to parse all the articles in the 'reuters21578' folder, the necessary variable 
    is defined.
    '''
    file_name_sgm = ""
    list_temp = []
    list_temp.extend((i,1000) for i in range(0,21))
    list_temp.append((21,578))

    '''
    It pulls all the files in the 'reuters21578' folder one by one and sends them to the 
    auxiliary functions described above.
    '''
    for i in range(0, len(list_temp)):
        file_name_sgm = '{}/{}-{:03d}.{}'.format("reuters21578", "reut2", list_temp[i][0], "sgm")
        f = open(file=file_name_sgm, mode='r', encoding='latin-1')
        text = f.read()
        temp = text
        for i in range(0,list_temp[i][1]):
            get_reuters_index(text=temp)
            text = temp[start_index:last_index+1]
            get_article_id(text=text)
            get_title(text=text)
            get_body(text=text)
            temp = temp[last_index:]

    f.close()

    trie = Trie()
    
    for item in dict_reuters: 
        dict_reuters[item] = list(dict_reuters[item])
        trie.insert(item)

    '''
    As stated in the project description, I create two different files and fill them with 
    the 'dict_reuters' and 'trie' data structures.
    '''
    with open('inverted_index.json', 'w') as f:
        json.dump(dict_reuters, f)

    f.close()

    with open('trie.pickle', 'wb') as f:
        pickle.dump(trie, f)

    f.close()

    shutil.rmtree(directory)

    