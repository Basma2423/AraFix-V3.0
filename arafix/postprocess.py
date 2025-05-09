from .config import DIACRITICS

def reverse_shadda(text):
    SHADDA = 'ّ'
    text_list = list(text)
    for i, ch in enumerate(text_list[1:]):
        if text_list[i] == SHADDA and text_list[i-1] in DIACRITICS:
            text_list[i], text_list[i-1] = text_list[i-1], text_list[i]
    return ''.join(text_list)

def postprocess(text):

    text = str(text)
    text = reverse_shadda(text)

    return text