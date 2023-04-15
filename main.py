from bs4 import BeautifulSoup
import re
import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main():
    url = "https://pokemondb.net/pokedex/game/firered-leafgreen"
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")
    names = []
    numbers = []
    types_pl = []
    html_string = ""
    types_dict = {"normal": "normalny", "fighting": "walczący", "flying": "latający",
                  "poison": "trujący", "ground": "ziemny", "rock": "kamienny", "bug": "robak",
                  "ghost": "duch", "steel": "stalowy", "fire": "ognisty", "water": "wodny",
                  "grass": "trawiasty", "electric": "elektryczny", "psychic": "psychiczny",
                  "ice": "lodowy", "dragon": "smok", "dark": "mroczny"}

    for tag in soup.find_all(class_="ent-name"):
        names.append(tag.string)

    for tag in soup.find_all(string=re.compile("#")):
        numbers.append(int(tag[1:]))

    for name in names:
        pokemon_types = soup.find(string=name).find_parent().find_next_sibling("small").find_all(
            class_="itype")
        types_pl.append(
            [types_dict[pokemon_type.string.casefold()] for pokemon_type in pokemon_types])

    return render_template("index.html", names=names, numbers=numbers, types=types_pl, zip=zip)
