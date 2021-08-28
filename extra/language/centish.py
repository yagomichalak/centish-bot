import json
from typing import Dict, List

class Centish:
    """ Class for the Centish language. """

    words_path: str = './extra/language/words.json'
    
    # {"word": "", "translation": "", "types": [], "note": "", "examples": []}

    @classmethod
    async def get_words(cls) -> Dict[str, List[Dict[str, str]]]:
        """ Gets all words from the vocabulary list. """

        data = {}
        with open(str(cls.words_path), 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
        return data

    @classmethod
    async def filter_words(cls, words: List[str], word_type: str) -> List[Dict[str, str]]:
        """ Filters a word list by a word type.
        :param word_type: The type of word to filter the list to. """

        return [w for w in words if word_type.title() in w['types']]