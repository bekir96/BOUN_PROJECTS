from utils import *
import re
import string


# Class for store all information and data manipulation about single book
class Prep:
    def __init__(self, data):
        self.data = data
        self.title = ""     # Title of the book
        self.author = list()    # Author of the book
        self.description = ""   # Description of the book with the list
        self.real_description = ""      # Description of the book
        self.recommendatiton = list()       # Recommendatiton of the book
        self.genres = set()     # Genres of the book
        self.for_corpus = dict()    # Dict for corpus includes all information about book

    '''
    Function 'find_str' if substring is in string, find starting index or ending index of substring 
    with the control and return it, otherwise return -1.
    @params
    s:  the string we are looking for in
    char:   substring
    control:    control return is whether starting index or ending index
    @return
    index: substring index
    '''
    def find_str(self, s, char, control) -> int:
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
    Function 'find_title' if title is in string, find starting index and ending index of substring 
    with the control and put it into self.title
    @params
    None
    @return
    None
    '''
    def find_title(self):
        start = self.find_str(self.data, PARSE_TITLE_FIRST, False)
        if start != -1:
            last = self.find_str(self.data, PARSE_TITLE_LAST, True)

            title_by = self.cleanhtml(raw_html=self.data[start:last])
            self.title = title_by.split(SEPERATOR_TITLE, 1)[0].strip()


    '''
    Function 'find_author' if author is in string, find starting index and ending index of substring 
    with the control and put it into self.author
    @params
    None
    @return
    None
    '''
    def find_author(self):
        start = 0
        last = 0
        temp_data = self.data

        start = self.find_str(temp_data, PARSE_AUTHOR_NAME_FIRST, True)

        while start != -1:
            temp_data = temp_data[start:]
            last = self.find_str(temp_data, PARSE_AUTHOR_NAME_LAST, True)

            start_temp = self.find_str(temp_data, PARSE_AUTHOR_NAME_SPAN_FIRST, False)
            last_temp = self.find_str(temp_data[start_temp:], PARSE_AUTHOR_NAME_SPAN_LAST, True)

            self.author.append(self.cleanhtml(temp_data[start_temp:start_temp+last_temp]).strip())
            start = self.find_str(temp_data, PARSE_AUTHOR_NAME_FIRST, True)


    '''
    Function 'find_description' if description is in string, find starting index and ending index of substring 
    with the control and put it into self.description
    @params
    None
    @return
    None
    '''
    def find_description(self):
        start = 0
        last = 0
        temp_data = self.data

        start = self.find_str(temp_data, PARSE_DESCRIPTION_DIV_CONTAINER_FIRST, False)
        if start != -1:
            temp_data = temp_data[start:]
            last = self.find_str(temp_data, PARSE_DESCRIPTION_DIV_CONTAINER_LAST, True)
            temp_data = temp_data[:last]

            start_temp = self.find_str(temp_data, PARSE_DESCRIPTION_FIRST, False)
            while start_temp != -1:
                last_temp = self.find_str(temp_data, PARSE_DESCRIPTION_LAST, True)
                self.description = self.cleanhtml(temp_data[start_temp:last_temp]).strip()
                temp_data = temp_data[last_temp:]
                start_temp = self.find_str(temp_data, PARSE_DESCRIPTION_FIRST, False)


    '''
    Function 'find_recommendatiton' if recommendatiton is in string, find starting index and ending index of substring 
    with the control and put it into self.recommendatiton
    @params
    None
    @return
    None
    '''
    def find_recommendatiton(self):
        start = 0
        last = 0
        temp_data = self.data

        start = self.find_str(temp_data, PARSE_RECOMENDED_FIRST, False)
        if start != -1:
            temp_data = temp_data[start:]
            last = self.find_str(temp_data, PARSE_RECOMENDED_LAST, True)
            temp_data = temp_data[:last]

            start_temp = self.find_str(temp_data, PARSE_ITERATE_RECOMMENDED_FIRST, True)
            while start_temp != -1:
                last_temp = self.find_str(temp_data, PARSE_ITERATE_RECOMMENDED_LAST, True)
                self.recommendatiton.append(temp_data[start_temp:last_temp-len(PARSE_ITERATE_RECOMMENDED_LAST)])
                temp_data = temp_data[last_temp:]
                start_temp = self.find_str(temp_data, PARSE_ITERATE_RECOMMENDED_FIRST, True)


    '''
    Function 'find_genres' if genre is in string, find starting index and ending index of substring 
    with the control and put it into self.genres
    @params
    None
    @return
    None
    '''
    def find_genres(self):
        start = 0
        last = 0
        temp_data = self.data

        start = self.find_str(temp_data, PARSE_GENRES_FIRST, False)
        while start != -1:
            temp_data = temp_data[start:]
            last = self.find_str(temp_data, PARSE_GENRES_LAST, True)

            self.genres.add(self.cleanhtml(temp_data[:last]).strip())
            temp_data = temp_data[last:]
            start = self.find_str(temp_data, PARSE_GENRES_FIRST, False)


    '''
    Function 'cleanhtml' clean html string from tag
    @params
    raw_html: string which includes html tag
    @return
    cleantext: string which not include html tag
    '''
    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext


    '''
    Function 'normalization' includes all function of normalizing description
    @params
    None
    @return
    None
    '''
    def normalization(self):
        self.description = self.description.split()
        self.caseFolding()
        self.punctuationRemoval()
        self.shortTokenRemoval()


    '''
    Function 'punctuationRemoval' satisfies punctuation removal from description
    @params
    None
    @return
    None
    '''
    def punctuationRemoval(self):
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # map punctuation to space
        newTokens = [token.translate(translator) for token in self.description]  # Punctuation Removal
        str_tokens = " ".join(token for token in newTokens)  # Retokenize the tokens that include any whitespaces after punctuation removal.
        self.description = str_tokens.split()


    '''
    Function 'punctuationRemoval' satisfies case folding on description
    @params
    None
    @return
    None
    '''
    def caseFolding(self):
        self.description = [token.lower() for token in self.description]


    '''
    Function 'punctuationRemoval' satisfies short token (len<=2) removal from description
    @params
    None
    @return
    None
    '''
    def shortTokenRemoval(self):
        self.description = [token for token in self.description if len(token) > 2]

    '''
    Function 'prepare' satisfies preparition of book infromation to fill corpus
    @params
    None
    @return
    None
    '''
    def prepare(self):
        self.find_title()
        self.find_author()
        self.find_description()
        self.real_description = self.description
        self.find_recommendatiton()
        self.find_genres()
        self.normalization()
        self.fill_corpus_dict()


    '''
    Function 'fill_corpus_dict' satisfies filling dict for corpus
    @params
    None
    @return
    None
    '''
    def fill_corpus_dict(self):
        self.for_corpus["title"] = self.title
        self.for_corpus["recommendatiton"] = self.recommendatiton
        self.for_corpus["genres"] = self.genres
        self.for_corpus["author"] = self.author
        self.for_corpus["description"] = self.description


    '''
    Function '__str__' satisfies __str__ form of prep function.
    @params
    None
    @return
    None
    '''
    def __str__(self) -> str:
        print("-" * 40)
        print("GIVEN URL BOOK DATA")
        print("*" * 40)
        print("Title: {}".format(self.title))
        print("-" * 40)
        print("Author:" + ', '.join(author for author in self.author))
        print("-" * 40)
        print("Description: {}".format(self.real_description))
        print("-" * 40)
        print("Genres: " + ', '.join(genre for genre in self.genres))
        print("-" * 40)
        print("Recommendatiton: " + ', '.join(recommendatiton for recommendatiton in self.recommendatiton))
        print("*" * 40)
        

