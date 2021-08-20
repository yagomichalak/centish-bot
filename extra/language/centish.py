import json
from typing import Dict

class Centish:
    """ Class for the Centish language. """

    words_path: str = './extra/language/words.json'
    
    # {"word": "", "translation": "", "types": [], "note": "", "examples": []}

    @classmethod
    async def get_words(cls) -> Dict[str, Dict[str, str]]:
        """ Gets all words from the vocabulary list. """

        data = {}
        with open(str(cls.words_path), 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
        return data