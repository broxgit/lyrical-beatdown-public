import string
from collections import Counter

# https://machinelearningmastery.com/clean-text-machine-learning-python/
from utils.misc_utils import merge_dict


def without_stop_words(lyrics):
    stripped = with_stop_words(lyrics)

    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]

    stop_words = ['i', 'you', 'the', 'a', 'for', 'in', 'is', 'it', 'to', 'im', 'if', 'be', 'of', 'are', 'on', 'so']

    all_stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
                      "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its",
                      "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
                      "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has",
                      "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or",
                      "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between",
                      "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
                      "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there",
                      "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other",
                      "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
                      "can", "will", "just", "dont", "should", "now"]
    # print(stop_words)

    return [w for w in words if not w in all_stop_words]


def with_stop_words(lyrics):
    words = lyrics.split()
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    lower = [w.lower() for w in stripped]

    return lower


def count_words_simple(lyrics):
    # get simple word count, including stop words
    simple = with_stop_words(lyrics)

    count = Counter(simple)
    return count


def count_words_complex(lyrics):
    # get complex word count, excluding stop words
    complex = without_stop_words(lyrics)

    count = Counter(complex)
    return count
