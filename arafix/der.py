from .config import DIACRITICS, ARAB_CHARS_NO_SPACE

def der(original_content, predicted_content, case_ending=True):

    SKIP_CASE_ENDING_VALUE = -1

    ################ HELPING FUNCTIONS #############################

    def extract_stack(stack, correct_reversed=True):
        if not stack:
            return ""

        char_haraqat = []
        while stack:
            char_haraqat.append(stack.pop())

        full_haraqah = "".join(char_haraqat)
        reversed_full_haraqah = "".join(reversed(char_haraqat))

        if full_haraqah in DIACRITICS:
            return full_haraqah
        elif reversed_full_haraqah in DIACRITICS and correct_reversed:
            return reversed_full_haraqah
        else:
            return ""

        ####################################

    def extract_haraqat(text, correct_reversed=True):
        if len(text.strip()) == 0:
            return text, [" "] * len(text), [""] * len(text)

        stack = []
        haraqat_list = []
        txt_list = []

        for char in text:
            if char not in DIACRITICS:
                stack_content = extract_stack(stack, correct_reversed=correct_reversed)
                haraqat_list.append(stack_content)
                txt_list.append(char)
                stack = []
            else:
                stack.append(char)

        if haraqat_list:
            del haraqat_list[0]
        haraqat_list.append(extract_stack(stack, correct_reversed))

        return text, txt_list, haraqat_list

        ####################################

    def get_case_ending_indices_from_un_diacritized_txt(text):
        text = text + [" "]
        indices = []
        for i in range(len(text)):
            if i > 0 and text[i] not in ARAB_CHARS_NO_SPACE and text[i - 1] in ARAB_CHARS_NO_SPACE:
                indices.append(i - 1)
        return indices

    ####################################################################

    _, original_text, original_haraqat = extract_haraqat(original_content, correct_reversed=False)
    _, predicted_text, predicted_haraqat = extract_haraqat(predicted_content, correct_reversed=False)

    if not case_ending:
        indices = get_case_ending_indices_from_un_diacritized_txt(original_text)
        for i in indices:
            original_haraqat[i] = SKIP_CASE_ENDING_VALUE

    equal = 0
    not_equal = 0

    for i, (original_char, predicted_char) in enumerate(zip(original_haraqat, predicted_haraqat)):
        if not case_ending and original_char == SKIP_CASE_ENDING_VALUE:
            continue
        if original_char == predicted_char:
            equal += 1
        else:
            not_equal += 1

    return round(not_equal / max(1, (equal + not_equal)), 2)
