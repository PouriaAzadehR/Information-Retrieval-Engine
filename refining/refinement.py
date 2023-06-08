from parsivar import *


def content_refinement(news_content):
    normalized_content = news_content.replace('انتهای پیام/', '')
    normalizeObject = Normalizer()
    normalized_content = normalizeObject.normalize(normalized_content)
    normalized_content = normalized_content.replace('،', '')
    normalized_content = normalized_content.replace('.', '')
    normalized_content = normalized_content.replace(':', '')
    normalized_content = normalized_content.replace('(', '')
    normalized_content = normalized_content.replace(')', '')
    return normalized_content
