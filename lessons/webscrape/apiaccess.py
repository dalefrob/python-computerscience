import requests
from pathlib import Path
import json

base_path = Path(__file__).parent.resolve()
image_path = base_path / "images"
data_path = base_path / "data"

def download_pokemon(name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}") 
    if response.status_code != 200:
        print("API called failed. Code: ", response.status_code)
        return
    
    json_response = json.loads(response.content) 
    # data
    pretty_json = json.dumps(json_response, indent=4)

    with open(f'{data_path}/{name}.json', 'w', encoding="utf8") as file:
        file.write(pretty_json)
   
    # image
    img_url = json_response['sprites']['front_default']
    response = requests.get(img_url)

    if response.status_code == 200:
        with open(f'{image_path}/{name}.png', 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download image")

download_pokemon("pikachu")

print("Success")