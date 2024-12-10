import requests

def get_example_usage(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            example = data[0]['meanings'][0]['definitions'][0].get('example', 'Пример недоступен.')
            return example
        else:
            return 'Example not found.'
    except Exception as e:
        return 'Error fetching example.'