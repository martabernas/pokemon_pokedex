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
    images_urls = []

    for tag in soup.find_all(class_="ent-name"):
        names.append(tag.string)

    for tag in soup.find_all(string=re.compile("#")):
        numbers.append(int(tag[1:]))

    for name in names:
        pokemon_types = soup.find(string=name).find_parent().find_next_sibling("small").find_all(
            class_="itype")
        types_pl.append(
            [types_dict[pokemon_type.string.casefold()] for pokemon_type in pokemon_types])

    for tag in soup.find_all(class_="img-fixed img-sprite img-sprite-v6"):
        images_urls.append(tag["src"])

    return render_template("index.html", names=names, numbers=numbers, types=types_pl,
                           images=images_urls, zip=zip)

@app.route("/<name>")
def pokemon_info(name):
    name = name.capitalize()
    base_url = "https://pokemondb.net/"
    url = "https://pokemondb.net/pokedex/game/firered-leafgreen"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")

    new_url = base_url + soup.find(string=name).find_parent()['href']
    req = requests.get(new_url)
    soup = BeautifulSoup(req.content, "html.parser")
    img_src = soup.find(attrs={"data-title": f"{name} official artwork"})['href']

    features = []


    stats_row = soup.find("h2", string="Base stats").find_next_sibling().find_next("th")

    while stats_row.string is not None:
        features.append([stats_row.string, stats_row.find_next("td").string])
        stats_row = stats_row.find_next("th")


    return render_template("pokemon_info.html", image=img_src, features=features)

# if __name__ == "__main__":
#     pokemon_info("bulbasaur")