import requests
from pathlib import Path
import json

base_path = Path(__file__).parent.resolve()
image_path = base_path / "images"

def download_pokemon(name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}") 
    if response.status_code != 200:
        print("API called failed. Code: ", response.status_code)
        return
    
    json_response = json.loads(response.content)

    img_url = json_response['sprites']['front_default']
    response = requests.get(img_url)

    if response.status_code == 200:
        with open(f'{image_path}/{name}.png', 'wb') as file:
            file.write(response.content)
    else:
        print("Failed to download image")

download_pokemon("mewtwo")

print("Success")