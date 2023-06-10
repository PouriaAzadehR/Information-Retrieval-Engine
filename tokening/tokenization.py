from hazm import *
from parsivar import *


def token_producer(refined_doc_content):
    tokenizeObject = Tokenizer()
    stemObject = FindStems()
    tokens = [stemObject.convert_to_stem(term) for term
              in tokenizeObject.tokenize_words(refined_doc_content) if term not in stopwords_list()]
    return tokens


