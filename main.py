from bs4 import BeautifulSoup
import re


def main():
    with open("pokemon_database.html", encoding="utf8") as fp:
        soup = BeautifulSoup(fp, "html.parser")
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
