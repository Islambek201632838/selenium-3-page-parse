import json

class JsonStorage:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
