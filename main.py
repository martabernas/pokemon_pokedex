from bs4 import BeautifulSoup
import re
import requests


def main():

    url = "https://pokemondb.net/pokedex/game/firered-leafgreen"
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")
    names = []
    numbers = []
    for tag in soup.find_all(class_="ent-name"):
        names.append(tag.string)

    for tag in soup.find_all(string=re.compile("#")):
        numbers.append(int(tag[1:]))

    for number, name in zip(numbers, names):
        if int(number) <= 150:
            print(number, name)

    # for tag in soup.find_all(class_="infocard-lg-data text-muted"):
    #     for string in tag.stripped_strings:
    #         print(string)


if __name__ == '__main__':
    main()
