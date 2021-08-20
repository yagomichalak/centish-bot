import json
from typing import Dict

class Centish:
    """ Class for the Centish language. """

    def __init__(self) -> None:
        self.words_path: str = './extra/language/words.json'


    async def get_words(self) -> Dict[str, Dict[str, str]]:
        """ Gets all words from the vocabulary list. """

        data = {}
        async with open(self.words_path, 'r', encoding="utf-8") as f:
            data = json.loads(f.read())
        return data