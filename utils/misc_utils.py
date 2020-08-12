import logging
import string
import time
import unicodedata

from logger import logger

LOGGER = logger.setup_logger('root', logging.DEBUG)


def merge_dict(dict1, dict2):
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = value + dict1[key]
    return dict3


def sanitize_lyrics(lyrics):
    lyrics_list = lyrics.split()
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in lyrics_list]
    return ' '.join(stripped)


def check_for_excluded(song_title):
    import re
    start = time.time()

    if re.search(r'\(*(demo)\)* *(version)*\)*$', song_title.lower()):
        return True

    if re.search(r'\(*(acoustic)\)* *(version)*\)*$', song_title.lower()):
        return True

    if re.search(r'\(*(live)\)* *(version)*\)*$', song_title.lower()):
        return True

    if re.search(r'\(*(remix)\)* *(version)*\)*$', song_title.lower()):
        return True

    if re.search(r'\(*(commentary)\)* *(version)*\)*$', song_title.lower()):
        return True

    end = time.time()

    elapsed = end - start


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def remove_punc(text):
    exclude = set(string.punctuation)
    exclude.add('’')
    exclude.add('\'')
    exclude.add('“')
    exclude.add('…')
    exclude.add('‐')

    return ''.join(ch for ch in text if ch not in exclude).lower()


def clean_text(text):
    return text.lower().rstrip().lstrip()


def str2hex(string_value):
    """
    Converts a string value to a byte representation in hex
    :param string_value: value to convert
    :return: hex value of string
    """
    hstr = '{0:x}'.format(int(string_value))
    return hstr


def byte_list(uni_string):
    """
    Converts a string to a byte array
    :param uni_string: string to convert
    :return: byte array representation of string
    """
    value2 = uni_string.encode('utf-8', 'replace')
    byte_list = []
    for x in value2:
        byte_list.append(x)
    return byte_list


def byte_array_to_hex(byte_array):
    """
    Converts a byte array to a hex value
    :param byte_array: byte array to convert
    :return: hex representation of the byte array
    """
    hex_string = ""
    for x in byte_array:
        truncated_byte = int(x)
        if x > 255:
            truncated_byte = x - 256
        byte_value = hex(truncated_byte)[2:].upper()
        if len(byte_value) == 1:
            byte_value = "0" + byte_value
        hex_string += byte_value

    return hex_string


def byte_array_to_hex_array(byte_array):
    """
    Converts a byte array to a hex value
    :param byte_array: byte array to convert
    :return: hex representation of the byte array
    """
    hex_string = []
    for x in byte_array:
        truncated_byte = int(x)
        if x > 255:
            truncated_byte = x - 256
        byte_value = hex(truncated_byte)[2:].upper()
        if len(byte_value) == 1:
            byte_value = "0" + byte_value
        hex_string.append("0x" + byte_value)

    return hex_string


def normalize_unicode(string):
    return (string.encode('ascii', 'ignore')).decode('utf-8')


def compare_strings(s1, s2, relaxed=False, log_failure=False, strip_spaces=False, very_relaxed=False):
    if not s1:
        if s2:
            logger.error(LOGGER, 's1 was type None when trying to compare to s2: {}'.format(s2))
        return False

    if not s2:
        if s1:
            logger.error(LOGGER, 's2: was type None when trying to compare to s1: {}'.format(s1))
        return False

    # simply check if strings match
    if s1 == s2:
        return True

    # check if lower-cased, whitespace-stripped strings match each other
    clean_s1 = clean_text(s1)
    clean_s2 = clean_text(s2)

    if clean_s1 == clean_s2:
        return True

    # check if lower-cased, whitespace-stripped, and removing punctuation for each string results in a match
    super_clean_s1 = remove_punc(clean_s1)
    super_clean_s2 = remove_punc(clean_s2)

    if super_clean_s1 == super_clean_s2:
        return True

    normal_s1 = normalize_unicode(clean_s1)
    normal_s2 = normalize_unicode(clean_s2)

    if normal_s1 == normal_s2:
        return True

    # check if strings match without any spaces
    if strip_spaces:
        if super_clean_s1.replace(' ', '') == super_clean_s2.replace(' ', ''):
            return True

    # check of ASCII code points match
    # mismatched_chars = []
    c1 = None
    c2 = None
    if len(s1) == len(s2):
        c1 = s1
        c2 = s2
    elif len(clean_s1) == len(clean_s2):
        c1 = clean_s1
        c2 = clean_s2
    elif len(super_clean_s1) == len(super_clean_s2):
        c1 = super_clean_s1
        c2 = super_clean_s2
    if c1 and c2:
        chars_match = True
        if isinstance(c1, str) and isinstance(c2, str):
            for x in range(0, len(c1)):
                if ord(c1[x]) != ord(c2[x]):
                    chars_match = False
                    # mismatched_chars.append('{} != {}'.format(ord(s1[x]), ord(s2[x])))
                    # print('{} != {}'.format(ord(c1[x]), ord(c2[x])))
                    # break
            if chars_match:
                return True

    if relaxed:
        if super_clean_s1.startswith(super_clean_s2):
            return True

        if super_clean_s2.startswith(super_clean_s1):
            return True

    if very_relaxed:
        # check if either unclean texts contain the other
        if s1 in s2:
            return True
        if s2 in s1:
            return True

        # check if either clean texts contain the other
        if clean_s1 in clean_s2:
            return True
        if clean_s2 in clean_s1:
            return True

        # check if either super clean texts contain the other
        if super_clean_s1 in super_clean_s2:
            return True
        if super_clean_s2 in super_clean_s1:
            return True

    if log_failure:
        logger.debug(LOGGER, '{} does not match {}'.format(s1, s2))

    return False


def prcnt(x, y):
    return round(x / y * 100, 2)
    # return '{0:.2f}%'.format((x / y * 100))


if __name__ == '__main__':
    n1 = normalize_unicode('​​blink-182')
    n2 = normalize_unicode('blink-182')
    logger.debug(LOGGER, '{} -- {}'.format(len(n1), len(n2)))
