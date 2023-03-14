from bs4 import BeautifulSoup, SoupStrainer
import requests
import math

def main():
    print("Poop Troop")

    numVersions = 0



    result = requests.get(f"https://www.cardmarket.com/en/Magic/Cards/Kykar-Winds-Fury/Versions")
    cardSoup = BeautifulSoup(result.text, 'html.parser', parse_only=SoupStrainer(id="ReprintSection"))
    for cardDiv in cardSoup.div.div.contents:
        print(cardDiv.a.find('h3').get_text())
        print(cardDiv.a.get('href'))


if __name__ == "__main__":
    main()

