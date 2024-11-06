import json

def write_to_json(filename, data, indent=None):
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)
    print(f"Data exported to {filename} successfully.")