import re
import unicodedata
import pyarabic.araby as araby
from .config import DIACRITICS, LETTERS, NUMBERS, ENG_LETTERS, ENG_NUMBERS


def remove_last_diacritic(text):
  while text and text[-1] in DIACRITICS:
    text = text[:-1]
  return text

def preprocess_keep_periods_and_commas(text, is_remove_last_diacritic=True):

  text = str(text)

  text = text.strip()

  text = araby.strip_tatweel(text)

  # Replace question marks, exclamation, and others with Arabic period + space
  text = re.sub(r'[?؟!:]|[\n\t\r\f\v]+', '. ', text)

  text = text.replace("ٱ", "ا")
  
  # sukoon normalization
  text = re.sub(r"[\u0616-\u061A\u06E1]", "\u0652", text)

  VALID_ARABIC_CHARS = LETTERS + DIACRITICS + NUMBERS + ENG_LETTERS + ENG_NUMBERS + [' ', '.', '.', ',', '،']

  text = ''.join(ch if ch in VALID_ARABIC_CHARS else ' ' for ch in text)

  POETRY_THREE_DOT_PATTERN = re.compile(r'\.{3}|\.\s\.\s\.')
  text = POETRY_THREE_DOT_PATTERN.sub('', text)

  SINGLE_LETTER_PATTERN = re.compile(
      r'(?<=[\s,،.۔])[' + ''.join(LETTERS) + r'](?=[\s,،.۔]|$)|'
      r'^[' + ''.join(LETTERS) + r'](?=[\s,،.۔])'
  )
  text = SINGLE_LETTER_PATTERN.sub(' ', text)

  WHITESPACES_PATTERN = re.compile(r"\s+")
  text = WHITESPACES_PATTERN.sub(' ', text)

  text = unicodedata.normalize("NFC", text)

  if is_remove_last_diacritic:
    text = remove_last_diacritic(text)

  return text

def preprocess(text, is_remove_last_diacritic=True):

  text = str(text)

  text = text.strip()
  
  text = araby.strip_tatweel(text)

  text = re.sub(r'[?؟!:]|[\n\t\r\f\v]+', '. ', text)

  VALID_ARABIC_CHARS = LETTERS + DIACRITICS + NUMBERS + ENG_LETTERS + ENG_NUMBERS + [' ']

  text = ''.join(ch if ch in VALID_ARABIC_CHARS else ' ' for ch in text)

  SINGLE_LETTER_PATTERN = re.compile(r'\s[' + ''.join(LETTERS) + r']\s')
  text = SINGLE_LETTER_PATTERN.sub(' ', text)

  MULTIPLE_CHAR_PATTERN = re.compile(r"(\D)\1{2,}", re.DOTALL)
  text = MULTIPLE_CHAR_PATTERN.sub(r"\1\1", text)

  WHITESPACES_PATTERN = re.compile(r"\s+")
  text = WHITESPACES_PATTERN.sub(' ', text)

  text = unicodedata.normalize("NFC", text)

  if is_remove_last_diacritic:
    text = remove_last_diacritic(text)

  return text
