class AIModuleFilter:
    def __init__(self, all_modules, suggestions):
        self.all_modules = all_modules
        self.suggestions = [s.lower() for s in suggestions]

    def extract_suggested(self):
        selected = []
        for module in self.all_modules:
            if any(suggestion in module.name.lower() for suggestion in self.suggestions):
                selected.append(module)
        return selected
