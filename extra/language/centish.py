import json
from typing import Dict, List, Union, Any

class Centish:
    """ Class for the Centish language. """

    path: str = './extra/language/'
    
    # {"word": "", "translation": "", "types": [], "note": "", "examples": []}

    @classmethod
    async def get_words(cls) -> Dict[str, List[Dict[str, str]]]:
        """ Gets all words from the vocabulary list. """

        data = {}
        with open(f"{cls.path}words.json", 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
        return data

    @classmethod
    async def filter_words(cls, words: List[str], word_type: str) -> List[Dict[str, str]]:
        """ Filters a word list by a word type.
        :param words: The list of words to filter.
        :param word_type: The type of word to filter the list to. """

        return [w for w in words if word_type.title() in w['types']]

    @classmethod
    async def find_words(cls, search, words, multiple: bool = True
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """ Finds the word in the strings.
        :param search: The input search.
        :param words: The list of words from which to search.
        :param multiple: Whether to return multiple values. [Optional][Default = True] """

        words_found = []
        for word in words:
            searchable_columns = ' '.join([word['word'].lower(), word['translation'].lower()])
            idx = searchable_columns.find(search)
            if idx != -1:
                words_found.append(word)

        if multiple:
            return words_found if words_found else None
        else:
            return words_found[0] if words_found else None

    @classmethod
    async def get_tenses(cls) -> Dict[str, Union[str, None]]:
        """ Gets all tenses present in the Centish language. """

        data = {}
        with open(f"{cls.path}tenses.json", 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
        return data
