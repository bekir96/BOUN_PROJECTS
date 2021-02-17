import os
from utils import *
from vivification import AutoVivification
import math

dict_corpus = AutoVivification()
dict_vocab = AutoVivification()
dict_mi = AutoVivification()

dict_test = AutoVivification()
dict_test[LEGITIMATE] = list()
dict_test[SPAM] = list()
temp_test = AutoVivification()
content_dict = AutoVivification()
content_dict[LEGITIMATE] = list()
content_dict[SPAM] = list()

LEGITIMATE_WORD = 0
SPAM_WORD = 0
VOCAB = 0
P_CJ_LEGITIMATE = 0.0
P_CJ_SPAM = 0.0

TOTAL_VOCAB = set()

temp_1 = AutoVivification()
temp_2 = AutoVivification()


'''
    Function 'parse' parse the email content with split
    @params
    content: email content
    type: LEGITIMATE or SPAM
    filepath: email filepath name
    @return
    None: html content
'''
def parse(content: str, type, filepath: str):
    global dict_corpus
    content = content.split()
    None if REMOVE_STRING not in content else content.remove(REMOVE_STRING)
    dict_corpus[type][filepath]['words'] = content #if dict_corpus[type][filepath]['words'] is {} else dict_corpus[type][filepath]['words'].extend(content)


'''
    Function 'find_size' calculate LEGITIMATE_WORD, SPAM_WORD, VOCAB, P_CJ_LEGITIMATE, P_CJ_SPAM and fill the vocab and corpus dict
    @params
    None: 
    @return
    None:
'''
def find_size():
    global LEGITIMATE_WORD, SPAM_WORD, VOCAB, P_CJ_LEGITIMATE, P_CJ_SPAM, dict_corpus, dict_vocab, TOTAL_VOCAB
    dict_vocab[LEGITIMATE]['vocab'] = set()
    dict_vocab[SPAM]['vocab'] = set()

    count_legitimate = 0
    count_spam = 0

    for filepath in dict_corpus[LEGITIMATE]:
        count_legitimate+=len(dict_corpus[LEGITIMATE][filepath]['words'])
        dict_vocab[LEGITIMATE]['vocab'] |= {*dict_corpus[LEGITIMATE][filepath]['words']}

    LEGITIMATE_WORD = count_legitimate

    for filepath in dict_corpus[SPAM]:
        count_spam+=len(dict_corpus[SPAM][filepath]['words'])
        dict_vocab[SPAM]['vocab'] |= {*dict_corpus[SPAM][filepath]['words']}
        
    SPAM_WORD = count_spam
    TOTAL_VOCAB = {*dict_vocab[LEGITIMATE]['vocab']} | {*dict_vocab[SPAM]['vocab']}
    VOCAB = len(TOTAL_VOCAB)

    P_CJ_LEGITIMATE = len(dict_corpus[LEGITIMATE]) / (len(dict_corpus[LEGITIMATE]) + len(dict_corpus[SPAM]))
    P_CJ_SPAM = len(dict_corpus[SPAM]) / (len(dict_corpus[LEGITIMATE]) + len(dict_corpus[SPAM]))


'''
    Function 'find_spam_or_legitimate' basically find whether content spam or legitimate
    @params
    content: test mail content
    type: LEGITIMATE or SPAM
    @return
    None: 
'''
def find_spam_or_legitimate(content: str, type):
    global dict_test

    log_legitimate = math.log(P_CJ_LEGITIMATE)
    log_spam = math.log(P_CJ_SPAM)

    content = content.split()
    None if REMOVE_STRING not in content else content.remove(REMOVE_STRING)
    content_set = set(content)

    for vocab in content_set:
        if vocab in TOTAL_VOCAB:
            temp = find_occurences(vocab=vocab, type=LEGITIMATE)
            log_legitimate+=math.log((temp + ALPHA) / (LEGITIMATE_WORD + VOCAB * ALPHA)) * content.count(vocab) 

            temp = find_occurences(vocab=vocab, type=SPAM)
            log_spam+=math.log((temp + ALPHA) / (SPAM_WORD + VOCAB * ALPHA)) * content.count(vocab) 

    dict_test[type].append(LEGITIMATE if log_legitimate > log_spam else SPAM)


'''
    Function 'find_occurences' find occurences number and return it
    @params
    vocab: one specific word in vocab dict
    type: LEGITIMATE or SPAM
    @return
    occurences: occurences number of vocab
'''
def find_occurences(vocab: str, type):
    occurences = 0
    for filepath in dict_corpus[type]:
        occurences+=dict_corpus[type][filepath]['words'].count(vocab)
    return occurences


'''
    Function 'traverse_vocab' traverse all vocab
    @params
    None:
    @return
    None:
'''
def traverse_vocab():
    global dict_mi
    for vocab in TOTAL_VOCAB:
        mi_value = find_mi(vocab=vocab)
        dict_mi[vocab] = mi_value


'''
    Function 'find_mi' find mi value
    @params
    vocab: one specific word in vocab dict
    @return
    calculate_mi(): function to calculate mi value
'''
def find_mi(vocab: str):
    n11 = 0
    n01 = 0
    n10 = 0
    n00 = 0

    for filepath in dict_corpus[LEGITIMATE]:
        if vocab in dict_corpus[LEGITIMATE][filepath]['words']:   n11+=1
        else:   n01+=1

    for filepath in dict_corpus[SPAM]:
        if vocab in dict_corpus[SPAM][filepath]['words']:   n10+=1
        else:   n00+=1

    return calculate_mi(n11=n11, n01=n01, n10=n10, n00=n00)

'''
    Function 'calculate_mi' helper function mi value.
    @params
    n11: exists and class exists
    n01: not exists and class exists
    n10: exists and not class exists
    n00: not exists and not class exists
    @return
    int: mi value
'''
def calculate_mi(n11: int, n01: int, n10: int, n00: int):
    total = n11 + n01 + n10 + n00
    temp_1 = math.log((total * n11 / ((n11 + n10) * (n11 + n01))), 2) if n11 != 0 else 0
    temp_2 = math.log((total * n01 / ((n01 + n00) * (n11 + n01))), 2) if n01 != 0 else 0
    temp_3 = math.log((total * n10 / ((n11 + n10) * (n10 + n00))), 2) if n10 != 0 else 0
    temp_4 = math.log((total * n00 / ((n01 + n00) * (n10 + n00))), 2) if n00 != 0 else 0

    return  n11/total * temp_1 \
                +   n01/total * temp_2 \
                    +   n10/total * temp_3 \
                        +   n00/total * temp_4

'''
    Function 'calculate_measure_values' calculates precision, recall and f_measure value
    @params
    type: LEGITIMATE or SPAM
    test: dict to be tested
    control: to control print output
    @return
    precision: 
    recall:
    f_measure:
'''
def calculate_measure_values(type, test: AutoVivification(), control: bool):
    tp = test[type].count(type)
    fp = test[LEGITIMATE if type == SPAM else SPAM].count(type)
    fn = test[type].count(LEGITIMATE if type == SPAM else SPAM)
    tn = test[LEGITIMATE if type == SPAM else SPAM].count(LEGITIMATE if type == SPAM else SPAM)
    
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f_measure = 2 * precision * recall / (precision + recall)
    if control:
        print('tp: {}, fp: {}, fn: {}, tn: {}'.format(tp, fp, fn, tn))
        print('Performance values for class {}:'.format('legitimate' if type == LEGITIMATE else 'spam'))
        print('-' * 30)
        print('PRECISION: {}'.format(precision))
        print('RECALL: {}'.format(recall))
        print('F-measure: {}'.format(f_measure))
        print('-' * 30)
    return precision, recall, f_measure

'''
    Function 'shuffle' shuffle without mutual information dict and with mutual information dict
    @params
    None: 
    @return
    None: 
'''
def shuffle():
    global temp_1, temp_2
    rand_number = 0
    for i in range(0, len(temp_1)):
        rand_number = 0 if rand_number != 0 else 1
        if rand_number != 0:
            temp_1[LEGITIMATE][i], temp_2[LEGITIMATE][i] = temp_2[LEGITIMATE][i], temp_1[LEGITIMATE][i] 
            temp_1[SPAM][i], temp_2[SPAM][i] = temp_2[SPAM][i], temp_1[SPAM][i]

'''
    Function 'randomization_test' find randomization test probability and print it.
    @params
    macro_average_1: without mutual information macro_average
    macro_average_2: with mutual information macro_average
    @return
    None:
'''
def randomization_test(macro_average_1: int, macro_average_2: int):
    global temp_1, temp_2
    counter = 0
    diff = abs(macro_average_1 - macro_average_2)
    
    for i in range(0, R):
        temp_1 = temp_test
        temp_2 = dict_test
        shuffle()
        _, _, f_temp_1 = calculate_measure_values(LEGITIMATE, temp_1, False)
        _, _, f_temp_2 = calculate_measure_values(SPAM, temp_1, False)
        _, _, f_temp_3 = calculate_measure_values(LEGITIMATE, temp_2, False)
        _, _, f_temp_4 = calculate_measure_values(SPAM, temp_2, False)

        temp_average_1 = (f_temp_1 + f_temp_2) / 2
        temp_average_2 = (f_temp_3 + f_temp_4) / 2
        diff_temp = abs(temp_average_1 - temp_average_2)
        if diff_temp >= diff:
            counter+=1

    print(counter)
    print(R)
    p_value = (counter+1)/(R+1)
    print('Approximate Randomization Test Result: {}'.format(p_value))
    
def open_file(filepath):
    with open(file=filepath, mode='r') as f:
        return f.read()

'''
    Function 'traverse_train' traverse train file in directory and pass its content to parse function.
    @params
    directory: train directory
    type: LEGITIMATE or SPAM
    @return
    None:
'''
def traverse_train(directory, type):
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath != directory + '/.DS_Store':
                try:
                    content = open_file(filepath=filepath)
                    parse(content=content, type=type, filepath=filepath)
                except:
                    continue

'''
    Function 'traverse_test' traverse test file in directory and pass its content to parse function.
    @params
    directory: test directory
    type: LEGITIMATE or SPAM
    @return
    None:
'''
def traverse_test(directory, type):
    global content_dict
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath != directory + '/.DS_Store':
                try:
                    content = open_file(filepath=filepath)
                    content_dict[type].append(content)
                    find_spam_or_legitimate(content=content, type=type)
                except:
                    continue


if __name__=="__main__":
    traverse_train(directory=DIRECTORY_TRAIN_LEGITIMATE, type=LEGITIMATE)
    traverse_train(directory=DIRECTORY_TRAIN_SPAM, type=SPAM)
    find_size()
    traverse_test(directory=DIRECTORY_TEST_LEGITIMATE, type=LEGITIMATE)
    traverse_test(directory=DIRECTORY_TEST_SPAM, type=SPAM)


    '''
        Output of NO MUTUAL INFORMATION START
    '''
    print('*' * 30)
    print('NO MUTUAL INFORMATION')
    print('*' * 30)
    print('Vocabulary size: {}'.format(len(TOTAL_VOCAB)))
    print('-' * 30)
    l_precision, l_recall, l_f = calculate_measure_values(type=LEGITIMATE, test=dict_test, control=True)
    s_precision, s_recall, s_f = calculate_measure_values(type=SPAM, test=dict_test, control=True)
    macro_average_1 = (l_f + s_f)/2
    print('MACRO AVERAGED PRECISION: {}'.format((l_precision + s_precision)/2))
    print('MACRO AVERAGED RECALL: {}'.format((l_recall + s_recall)/2))
    print('MACRO AVERAGED F-MEASURE: {}'.format((l_f + s_f)/2))
    print('-' * 30)
    '''
        Output of NO MUTUAL INFORMATION FINISH
    '''

    temp_test = dict_test.copy()
    dict_test.clear()
    dict_test[LEGITIMATE] = list()
    dict_test[SPAM] = list()

    traverse_vocab()
    dict_mi = {key: dict_mi[key] for key in sorted(dict_mi, key=dict_mi.get, reverse=True)[:DISCRIMINATION_NUMBER]}
    
    TOTAL_VOCAB = set(dict_mi.keys())
    VOCAB = DISCRIMINATION_NUMBER

    count_legitimate = 0
    count_spam = 0
    for vocab in TOTAL_VOCAB:
        for filepath in dict_corpus[LEGITIMATE]:
            count_legitimate+=dict_corpus[LEGITIMATE][filepath]['words'].count(vocab)
        
        for filepath in dict_corpus[SPAM]:
            count_spam+=dict_corpus[SPAM][filepath]['words'].count(vocab)

    LEGITIMATE_WORD = count_legitimate
    SPAM_WORD = count_spam
    for content in content_dict[LEGITIMATE]:
        find_spam_or_legitimate(content=content, type=LEGITIMATE)
    
    for content in content_dict[SPAM]:
        find_spam_or_legitimate(content=content, type=SPAM)

    '''
        Output of WITH MUTUAL INFORMATION START
    '''
    print('*' * 30)
    print('WITH MUTUAL INFORMATION')
    print('*' * 30)
    print('Most 100 discriminating words: ')
    print(dict_mi.keys())
    print('-' * 30)
    print('Vocabulary size: {}'.format(len(TOTAL_VOCAB)))
    print('-' * 30)
    l_precision, l_recall, l_f = calculate_measure_values(type=LEGITIMATE, test=dict_test, control=True)
    s_precision, s_recall, s_f = calculate_measure_values(type=SPAM, test=dict_test, control=True)
    macro_average_2 = (l_f + s_f)/2
    print('MACRO AVERAGED PRECISION: {}'.format((l_precision + s_precision)/2))
    print('MACRO AVERAGED RECALL: {}'.format((l_recall + s_recall)/2))
    print('MACRO AVERAGED F-MEASURE: {}'.format((l_f + s_f)/2))
    print('-' * 30)
    '''
        Output of WITH MUTUAL INFORMATION FINISH
    '''

    randomization_test(macro_average_1=macro_average_1, macro_average_2=macro_average_2)
