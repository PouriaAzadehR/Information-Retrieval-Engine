from collections import defaultdict

from hazm import stopwords_list

from custom_data_structures import Posting, Position
from json_reading import reader
from tokening import token_producer
from refining import content_refinement
from displaying import display
from parsivar import *


def token_producer(refined_doc_content):
    tokenizeObject = Tokenizer()
    stemObject = FindStems()
    tokens = [stemObject.convert_to_stem(term) for term
              in tokenizeObject.tokenize_words(refined_doc_content) if term not in stopwords_list()]
    return tokens


def position_of_each_token_per_doc(news_content, doc_id):
    normalized_content = news_content.replace('انتهای پیام/', '')
    normalizeObject = Normalizer()
    normalized_content = normalizeObject.normalize(normalized_content)
    normalized_content = normalized_content.replace('،', '')
    normalized_content = normalized_content.replace('.', '')
    normalized_content = normalized_content.replace(':', '')
    normalized_content = normalized_content.replace('(', '')
    normalized_content = normalized_content.replace(')', '')
    dict_term_position = defaultdict(lambda: Position(doc_id))
    tokens = token_producer(normalized_content)
    for position, token in enumerate(tokens): dict_term_position[token].append(position)
    return dict_term_position


def create_index(docs):
    index = {}
    print('creating invert index ...')
    for doc_id, doc in enumerate(docs):
        dict_term_position = position_of_each_token_per_doc(docs[doc].get('content'), doc_id, )
        for term, position in dict_term_position.items():
            if term not in index.keys():
                postingdict = Posting(term)
                index[term] = postingdict
            else:
                postingdict = index[term]

            postingdict[doc_id] = position
        if doc_id == 100:
            break
    return index


data = reader('../data/IR_data_news_12k.json')


def display(index):
    for term, posting in index.items():
        print(f"term: {term}\n frequency in all docs: {posting.freq}")
        for doc_id, position in posting.items():
            print(f"\t term : {term} is founded in doc with id {doc_id}"
                  f" about {position.freq} times at positions {position}")
        print()
        print()


display(create_index(data))
