from bs4 import BeautifulSoup
import re
import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    url = "https://pokemondb.net/pokedex/game/firered-leafgreen"
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")
    names = []
    numbers = []
    types_eng = []
    html_string = ""
    types_dict = {"normal": "normalny", "fighting": "walczący", "flying": "latający",
                  "poison": "trujący", "ground": "ziemny", "rock": "kamienny", "bug": "robaczy",
                  "ghost": "duchowy", "steel": "stalowy", "fire": "ognisty", "water": "wodny",
                  "grass": "trawiasty", "electric": "elektryczny", "psychic": "psychiczny",
                  "ice": "lodowy", "dragon": "smoczy", "dark": "mroczny"}

    for tag in soup.find_all(class_="ent-name"):
        names.append(tag.string)

    for tag in soup.find_all(string=re.compile("#")):
        numbers.append(int(tag[1:]))

    for name in names:
        pokemon_types = soup.find(string=name).find_parent().find_next_sibling("small").find_all(
            class_="itype")
        types_eng.append(
            [types_dict[pokemon_type.string.casefold()] for pokemon_type in pokemon_types])

    for number, name, type_ in zip(numbers, names, types_eng):
        html_string += f"{number} {name} {type_} <br>"
        print(number, name, type_)

    return html_string


if __name__ == '__main__':
    main()
