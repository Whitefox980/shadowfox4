# core/ai_mod_filter.py
class AIModuleFilter:
    def __init__(self, available_modules):
        self.available = [mod.name.upper() for mod in available_modules]

    def extract(self, ai_response):
        extracted = []
        for word in ai_response.replace(",", " ").split():
            clean_word = word.strip().upper()
            if clean_word in self.available and clean_word not in extracted:
                extracted.append(clean_word)
        return extracted
