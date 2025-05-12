class AIModuleFilter:
    def __init__(self, available_modules):
        self.available = {mod.name.upper(): mod for mod in available_modules}

    def extract(self, selected_names):
        selected = []
        for name in selected_names:
            mod = self.available.get(name.strip().upper())
            if mod:
                selected.append(mod)
        return selected
