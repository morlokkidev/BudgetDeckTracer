from bs4 import BeautifulSoup, SoupStrainer
import requests
import math
#import re

def main():
    card = "Kykar, Wind's fury"
    print(f"Lets get some info on {card}")
    getCardPrice(card)

def getCardPrice(card):
    cardFormatted = formatCard(card)
    result = requests.get(f"https://www.cardmarket.com/en/Magic/Cards/{cardFormatted}/Versions")
    cardSoup = BeautifulSoup(result.text, 'html.parser', parse_only=SoupStrainer(id="ReprintSection"))
    for cardDiv in cardSoup.div.div.contents:
        print(cardDiv.a.find('h3').get_text())
        print(cardDiv.a.get('href'))

#TODO use regex instead of multiples of replace
def formatCard(card):
    print(f"original card name: {card}")
    formatted = card.replace(" ", "-")
    formatted = formatted.replace(",","")
    formatted = formatted.replace("'","")
    print(f"formatted card name: {formatted}")
    return formatted

if __name__ == "__main__":
    main()

