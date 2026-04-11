import json

class Test:
    def __init__(self):
        self.file_path = "translation.json"
        self.position_items = self.load_position_items()
    def load_position_items(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                temp = json.load(f)
                #  = temp[0]['language']['position_items']

                position_items = {item["language"]: item["data"] for item in temp}['th']

        except FileNotFoundError:
            print("Error: translation.json not found.")
            self.position_items = []
        except Exception as e:
            print(f"An error occurred: {e}")
            self.position_items = []
        return position_items
    
test = Test()
a = test.position_items
print(a)
    

