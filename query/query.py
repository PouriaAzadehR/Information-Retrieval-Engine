from collections import defaultdict

from hazm import stopwords_list

from custom_data_structures import Posting, Position
from json_reading import reader
from tokening import token_producer
from refining import content_refinement
from displaying import display
from parsivar import *

def parser(query_split):
    one_word = []
    phrase_list = []
    i = 0
    while i < len(query_split):
        if query_split[i] == '"':
            phrase = []
            i += 1
            while query_split[i] != '"':
                phrase.append(query_split[i])
                i += 1
            phrase_list.append(phrase)

        else:
            if query_split[i] != '!':
                one_word.append(query_split[i])
        i += 1
    print(phrase_list)
    print(one_word)
    return phrase_list, one_word


def long_query(phrase):
    common_docs = set(index.get(phrase[0]).keys())
    for word in phrase:
        common_docs = common_docs.intersection(set(index.get(word).keys()))

    print(common_docs)
    res = []
    candidate = []
    for doc in common_docs:
        for word in phrase:
            candidate.append(index.get(word).get(doc))
        print(candidate)
        for i in range(len(candidate)):
            for j in range(len(candidate[i])):
                candidate[i][j] += len(candidate) - i - 1
        print(candidate)
        if len(set.intersection(*[set(list) for list in candidate])) != 0:
            res.append(doc)
        candidate = []

    print(res)
    return res


def one_word(query_split: list, word_list):
    for word in word_list:
        if word not in index.keys():
            return []
    common_docs = set(index.get(word_list[0]).keys())
    for word in word_list:
        if query_split[query_split.index(word) - 1] != '!':
            common_docs = common_docs.intersection(set(index.get(word).keys()))
        elif query_split[query_split.index(word) - 1] == '!':
            common_docs = common_docs.difference(set(index.get(word).keys()))
    return list(common_docs)


def not_found_exact_match(word_list,query_split):

    for word in word_list:
        if word not in index.keys():
            for word1 in word_list:
                if word1 in index.keys():
                    res = set(index.get(word1).keys())
                    return list(res)
            return []

    common_docs = set(index.get(word_list[0]).keys())
    for word in word_list:
        if query_split[query_split.index(word) - 1] == '!':
            common_docs = common_docs.difference(set(index.get(word).keys()))
        else:
            common_docs = common_docs | (set(index.get(word).keys()))
    return list(common_docs)


def decision_making():
    # query = '"خبرگزاری فارس" "فوتبال آسیا" گیتی'
    # query = 'ایران ! فوتبال'
    # query = 'فوتبال ! ایران'
    # query = 'باشگاه های فوتبال ! آسیا'
    # query = 'باشگاه های فوتبال آسیا'
    # query = '"خبرگزاری فارس"'
    # query = '"گزارش خبرگزاری فارس" فوتبال ایران'
    # query = '"گزارش خبرگزاری فارس" فوتبال ! ایران'
    query = 'مایکل ایران '


    query = content_refinement(query)
    query = token_producer(query)
    print(query)

    phrase_list, word_list = parser(query)
    res = []
    if len(phrase_list) == 0:
        res.append(one_word(query, word_list))
        res.append(not_found_exact_match(word_list,query))
        res_set = []
        for list_res in res:
            for doc_res in list_res:
                if doc_res not in res_set:
                    res_set.append(doc_res)
        return res_set
    else:
        for phrase in phrase_list:
            res.append(long_query(phrase))
        if len(word_list) != 0:
            res.append(one_word(query, word_list))
        res_set = set.intersection(*[set(list) for list in res])
        return res_set


res_doc = decision_making()

counter = 0

if len(res_doc)==0:
    print("nothing found. please refine your query")

for doc in res_doc:
    print(data.get(str(doc)).get('title'))
    counter+=1
    if counter == 5:
        break
