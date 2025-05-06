import re
import unicodedata
import pyarabic.araby as araby
from .config import DIACRITICS, LETTERS

def preprocess(text, remove_last_diacritic=True):

    text = str(text)

    text = araby.strip_tatweel(text)

    VALID_ARABIC_CHARS = LETTERS + DIACRITICS + [' ']

    text = ''.join(ch for ch in text if ch in VALID_ARABIC_CHARS)

    WHITESPACES_PATTERN = re.compile(r"\s+")
    text = WHITESPACES_PATTERN.sub(' ', text)

    SINGLE_LETTER_PATTERN = re.compile(r'\s[' + ''.join(LETTERS) + r']\s')
    text = SINGLE_LETTER_PATTERN.sub(' ', text)

    text = unicodedata.normalize("NFC", text)

    def remove_last_diacritic(text):
      while text and text[-1] in DIACRITICS:
        text = text[:-1]
      return text

    if remove_last_diacritic:
      text = remove_last_diacritic(text)

    return text
