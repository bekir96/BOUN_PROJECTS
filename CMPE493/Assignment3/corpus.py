import math
import json

# Class for store all tf_idf calculation and length for recommendate book for input url.
class Corpus:
    def __init__(self) -> None:
        self.corpus_dict = dict()   # all information about books
        self.words = set()  # all words in descriptions of books
        self.idf = dict()   # all values of word idf
        self.url_tf = AutoVivification()    # all tf of word with url key
        self.url_tf_idf = AutoVivification()    # all tf_idf of word with url key
        self.url_length = AutoVivification()    # all length of url with url key

        self.genre_words = set()    # all words in genres of books
        self.genre_idf = dict() # all values of genre word idf
        self.genre_url_tf = AutoVivification()  # all tf of genre word with url key
        self.genre_url_tf_idf = AutoVivification()  # all tf_idf of genre word with url key
        self.genre_url_length = AutoVivification()      # all length of url with url key

        self.input_corpus_dict = dict() # all information about input books
        self.input_words = set()    # all words in description of input book
        self.input_url_tf = AutoVivification()  # all values of word idf of input book
        self.input_url_tf_idf = AutoVivification()   # all tf of word with url key  of input book
        self.input_url_length = AutoVivification()  # all length of url with url key of input book

        self.input_genre_words = set()  # all words in genre of books   of input book
        self.input_genre_url_tf = AutoVivification()    # all values of genre word idf    of input book
        self.input_genre_url_tf_idf = AutoVivification()     # all tf of genre word with url key  of input book
        self.input_genre_url_length = AutoVivification()    # all length of url with url key    of input book

    '''
    Function 'fill_dict' fill self.corpus_dict with url as key and data as value
    @params
    url: book url
    data: book data
    @return
    None
    '''
    def fill_dict(self, url, data):
        self.corpus_dict[url] = data


    '''
    Function 'fill_words' fill self.words with all words in url descriptions.
    @params
    None
    @return
    None
    '''
    def fill_words(self):
        for url in self.corpus_dict:
            for word in self.corpus_dict[url]["description"]:
                self.words.add(word)


    '''
    Function 'fill_genre_words' fill self.words with all words in url genres.
    @params
    None
    @return
    None
    '''
    def fill_genre_words(self):
        for url in self.corpus_dict:
            for genre in self.corpus_dict[url]["genres"]:
                self.genre_words.add(genre)


    '''
    Function 'fill_tf_idf' calculate tf_idf of words in description with url and also calculate url length
    @params
    None
    @return
    None
    '''
    def fill_tf_idf(self):
        url_number = len(self.corpus_dict)
        url_number = float(url_number)
        for word in self.words:
            count_idf = 0
            for url in self.corpus_dict:
                count_tf = 0
                if word in self.corpus_dict[url]["description"]:
                    count_idf+=1

                for desc_word in self.corpus_dict[url]["description"]:
                    if word == desc_word:
                        count_tf+=1

                if count_tf != 0:
                    self.url_tf[url][word] = 1 + math.log10(count_tf)

            self.idf[word] = math.log10(url_number/count_idf)

        
        for url in self.corpus_dict:
            length = 0.0
            for word in self.url_tf[url]:
                tf_idf_value = self.url_tf[url][word] * self.idf[word]
                self.url_tf_idf[url][word] = tf_idf_value

                length+=tf_idf_value**2

            self.url_length[url] = math.sqrt(length)



    '''
    Function 'fill_genre_tf_idf' calculate tf_idf of words in genre with url and also calculate url length
    @params
    None
    @return
    None
    '''
    def fill_genre_tf_idf(self):
        url_number = len(self.corpus_dict)
        url_number = float(url_number)
        for genre in self.genre_words:
            count_idf = 0
            for url in self.corpus_dict:
                count_tf = 0
                if genre in self.corpus_dict[url]["genres"]:
                    count_idf+=1

                for desc_genre in self.corpus_dict[url]["genres"]:
                    if genre == desc_genre:
                        count_tf+=1

                if count_tf != 0:
                    self.genre_url_tf[url][genre] = 1 + math.log10(count_tf)

            self.genre_idf[genre] = math.log10(url_number/count_idf)

        
        for url in self.corpus_dict:
            length = 0.0
            for genre in self.genre_url_tf[url]:
                tf_idf_value = self.genre_url_tf[url][genre] * self.genre_idf[genre]
                self.genre_url_tf_idf[url][genre] = tf_idf_value

                length+=tf_idf_value**2

            self.genre_url_length[url] = math.sqrt(length)


    '''
    Function 'prepare' call all above functions.
    @params
    None
    @return
    None
    '''
    def prepare(self):
        self.fill_words()
        self.fill_tf_idf()
        self.fill_genre_words()
        self.fill_genre_tf_idf()


    # INPUT

    '''
    Function 'fill_input_dict' fill self.input_corpus_dict with input url as key and data as value
    @params
    url: input book url
    data: input book data
    @return
    None
    '''
    def fill_input_dict(self, url, data):
        self.input_corpus_dict[url] = data
    

    '''
    Function 'fill_input_words' fill self.input_words with all words in input url description.
    @params
    None
    @return
    None
    '''
    def fill_input_words(self):
        for url in self.input_corpus_dict:
            for word in self.input_corpus_dict[url]["description"]:
                self.input_words.add(word)


    '''
    Function 'fill_input_genre_words' fill self.input_genre_words with all words in input url genres.
    @params
    None
    @return
    None
    '''
    def fill_input_genre_words(self):
        for url in self.input_corpus_dict:
            for genre in self.input_corpus_dict[url]["genres"]:
                self.input_genre_words.add(genre)


    '''
    Function 'fill_input_tf_idf' calculate tf_idf of words in description with input url and also calculate input url length
    @params
    None
    @return
    None
    '''
    def fill_input_tf_idf(self):
        for word in self.input_words:
            for url in self.input_corpus_dict:
                count_tf = 0

                for desc_word in self.input_corpus_dict[url]["description"]:
                    if word == desc_word:
                        count_tf+=1

                if count_tf != 0:
                    self.input_url_tf[url][word] = 1 + math.log10(count_tf)
        
        for url in self.input_corpus_dict:
            length = 0.0
            for word in self.input_url_tf[url]:
                tf_idf_value = self.input_url_tf[url][word] * self.idf[word]
                self.input_url_tf_idf[url][word] = tf_idf_value
                
                length+=tf_idf_value**2

            self.input_url_length[url] = math.sqrt(length)


    '''
    Function 'fill_input_genre_tf_idf' calculate tf_idf of words in genres with input url and also calculate input url length
    @params
    None
    @return
    None
    '''
    def fill_input_genre_tf_idf(self):
        for genre in self.input_genre_words:
            for url in self.input_corpus_dict:
                count_tf = 0

                for desc_genre in self.input_corpus_dict[url]["genres"]:
                    if genre == desc_genre:
                        count_tf+=1

                if count_tf != 0:
                    self.input_genre_url_tf[url][genre] = 1 + math.log10(count_tf)
        
        for url in self.input_corpus_dict:
            length = 0.0
            for genre in self.input_genre_url_tf[url]:
                tf_idf_value = self.input_genre_url_tf[url][genre] * self.genre_idf[genre]
                self.input_genre_url_tf_idf[url][genre] = tf_idf_value

                length+=(tf_idf_value**2)

            self.input_genre_url_length[url] = math.sqrt(length)


    '''
    Function 'prepare' call all above functions for input url.
    @params
    None
    @return
    None
    '''
    def prepare_input(self):
        self.fill_input_words()
        self.fill_input_tf_idf()
        self.fill_input_genre_words()
        self.fill_input_genre_tf_idf()


# This class special class for dict data structure to give 2 key at once.
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
