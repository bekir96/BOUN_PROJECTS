from utils import CONTENT_FILE_NAME, CORPUS_FILE_NAME, SEPERATOR_URL, RECOMMENDATITON_NUMBER
from prep import Prep
from corpus import *
import requests
import json
import sys
import os
import pickle
from macosfile import MacOSFile

dict_url = dict()
dict_cos_sim = AutoVivification()


'''
    Function 'get_html' exract the content of url and return it
    @params
    content: url
    @return
    data: html content
'''
def get_html(content):
    webUrl = ""
    data = ""
    try:
        webUrl  = requests.get(content)
        print('Content: {}, status: {} '.format(content, webUrl.raise_for_status()))

        data = webUrl.text
    except requests.exceptions.RequestException as err:     # Exception satisfies that if getting url is broken.
        print(err)

    return data


'''
    Function 'read_file' exract the content of file and return it with list
    @params
    filename: name of given file
    @return
    content: list of all url
'''
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    content = [x.strip() for x in content] 
    return content


'''
    Function 'cosine_similarity_description' calculate cosine similarity to description between given url and all url,
    and put results into dict_cos_sim with key url->desc and value cos_similarity 
    @params
    corpus: all information about model
    input_url: given url as arg
    @return
    None
'''
def cosine_similarity_description(corpus: Corpus, input_url):
    for url in corpus.url_tf_idf:
        cos_similarity = 0.0 
        for word in corpus.url_tf_idf[url]:
            if word in corpus.input_url_tf_idf[input_url]:
                cos_similarity += (corpus.url_tf_idf[url][word] * corpus.input_url_tf_idf[input_url][word])
        
        temp = corpus.url_length[url] * corpus.input_url_length[input_url]

        if temp == 0: cos_similarity = 0
        else: cos_similarity/= (corpus.url_length[url] * corpus.input_url_length[input_url])

        dict_cos_sim[url]['desc'] = cos_similarity


'''
    Function 'cosine_similarity_description' calculate cosine similarity to genre between given url and all url,
    and put results into dict_cos_sim with key url->genre and value cos_similarity 
    @params
    corpus: all information about model
    input_url: given url as arg
    @return
    None
'''
def cosine_similarity_genres(corpus: Corpus, input_url):
    for url in corpus.genre_url_tf_idf:
        cos_similarity = 0.0 
        for word in corpus.genre_url_tf_idf[url]:
            if word in corpus.input_genre_url_tf_idf[input_url]:
                cos_similarity += (corpus.genre_url_tf_idf[url][word] * corpus.input_genre_url_tf_idf[input_url][word])
        
        temp = (corpus.genre_url_length[url] * corpus.input_genre_url_length[input_url])

        if temp == 0: cos_similarity = 0
        else: cos_similarity/= (corpus.genre_url_length[url] * corpus.input_genre_url_length[input_url])

        dict_cos_sim[url]['genre'] = cos_similarity


'''
    Function 'new_cosine calculate' real cosine similarity with alpha = 0.5 and put results into dict_cos_sim 
    with key url and value temp 
    @params
    None
    @return
    None
'''
def new_cosine():
    for url in dict_cos_sim:
        temp = -sys.maxsize-1
        alpha = 0.50
        if "genre" in dict_cos_sim[url] and "desc" in dict_cos_sim[url]:
            value = dict_cos_sim[url]['genre']*alpha + dict_cos_sim[url]['desc']*(1-alpha)
            temp = value if temp < value else temp
        elif "genre" in dict_cos_sim[url]:
            temp = dict_cos_sim[url]['genre']
        else:
            temp = dict_cos_sim[url]['desc']

        dict_cos_sim[url] = temp


'''
    Function 'evaluation' calculate precision and average precision as output, and also print all evaluated books as
    recommend with title and author.
    @params
    prep: all information about book with given url.
    corpus_dict: all information about books
    @return
    None
'''
def evaluation(prep:Prep, corpus_dict:dict()):
    count = 0.0
    total_ap = 0.0
    count_p = 0
    print("BOOKS I RECOMMEND")
    print("*" * 40)
    for url in dict_cos_sim:
        print("Title: {}".format(corpus_dict[url]["title"]))
        print("Author:" + ', '.join(author for author in corpus_dict[url]["author"]))
        print()
        count+=1
        if url in prep.recommendatiton:
            count_p+=1
        total_ap+=count_p/count    
    
    print("*" * 40)
    print("EVALUATION RESULT")
    print("Total correct predicate: {}".format(str(count_p)))
    print("P: {}".format(str(float(count_p/RECOMMENDATITON_NUMBER))) )
    print("AP@{}: {}".format(str(RECOMMENDATITON_NUMBER), str(total_ap/RECOMMENDATITON_NUMBER)))



'''
    Function 'pickle_dump' pickle obj to file with using MacOSFile.
    @params
    obj: class object    
    file_path: output file name
    @return
    None
'''
def pickle_dump(obj, file_path):
    with open(file_path, 'wb') as f:
        return pickle.dump(obj, MacOSFile(f), protocol=pickle.HIGHEST_PROTOCOL)


'''
    Function 'pickle_load' unpickle file to obj with using MacOSFile.
    @params
    file_path: output gile name
    @return
    obj: desired class obj
'''
def pickle_load(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(MacOSFile(f))

def load_file_json(filename):
    with open(filename) as f:
        return json.load(f)


if __name__ == "__main__":
    input_arg = sys.argv[1]

    # Control whether arg is file or not
    if os.path.isfile(input_arg):
        if os.path.isfile(CONTENT_FILE_NAME):
            os.remove(CONTENT_FILE_NAME)

        corpus = Corpus()
        content = read_file(filename=input_arg)

        # Traverse all url of given file
        for url in content:
            data = get_html(content=url)
            prep = Prep(data=data)
            prep.prepare()

            # Control html content of url is empty or not
            if prep.title == "":
                # If url is broke, change url to get request
                url_new = SEPERATOR_URL + "en/" + url.split(SEPERATOR_URL)[1]
                data = get_html(content=url_new)
                prep = Prep(data=data)
                prep.prepare()
                corpus.fill_dict(url, prep.for_corpus)
                del prep
            else:
                corpus.fill_dict(url, prep.for_corpus)
                del prep

        corpus.prepare()
        pickle_dump(corpus, CORPUS_FILE_NAME)
        del corpus

    else:
        corpus = Corpus()
        corpus = pickle_load(CORPUS_FILE_NAME)

        data_input = get_html(content=input_arg)
        prep = Prep(data=data_input)
        prep.prepare()

        # Output content of book with given url
        prep.__str__()

        corpus.fill_input_dict(input_arg, prep.for_corpus)
        corpus.prepare_input()

        cosine_similarity_description(corpus=corpus, input_url=input_arg)
        cosine_similarity_genres(corpus=corpus, input_url=input_arg)
        new_cosine()

        # Filter dict_cos_sim with highest RECOMMENDATITON_NUMBER+1 value
        dict_cos_sim = {key: dict_cos_sim[key] for key in sorted(dict_cos_sim, key=dict_cos_sim.get, reverse=True)[:RECOMMENDATITON_NUMBER+1]}
        
        # Control whether given url is in dict_cos_sim or not
        if input_arg in dict_cos_sim:
            # If given url is in dict_cos_sim, then remove it
            dict_cos_sim.pop(input_arg)
        else:
            # If given url is not in dict_cos_sim, then remove lowest value
            min_key = min(dict_cos_sim.keys(), key=lambda k: dict_cos_sim[k])
            del dict_cos_sim[min_key]

        evaluation(prep=prep, corpus_dict=corpus.corpus_dict)
    