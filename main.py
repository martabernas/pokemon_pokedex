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
    html_string = ""
    for tag in soup.find_all(class_="ent-name"):
        names.append(tag.string)

    for tag in soup.find_all(string=re.compile("#")):
        numbers.append(int(tag[1:]))

    for number, name in zip(numbers, names):
        if int(number) <= 150:
            html_string = html_string + f"{number} {name}<br>"
            print(number, name)

    return html_string



if __name__ == '__main__':
    main()
