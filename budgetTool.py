from bs4 import BeautifulSoup, SoupStrainer
import requests
import math
import fnmatch
#import re

def main():
    
    #Clear Output.txt
    f = open('output.txt','w')
    f.close()
    #Start the engine
    readWriteList()

def readWriteList():
    #Define newline for fstring
    nl = "\n"
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    for line in lines:
        f = open('output.txt', 'a')
        newline = f"{line.strip()}{getCardPrice(line.strip())}"
        print(f"Writing line: {newline}")
        f.write(f"{newline}{nl}")
        f.close()
    file.close()

def getCardPrice(card):
    listSets, listPrices = [], []
    cardFormatted = formatCard(card)
    result = requests.get(f"https://www.cardmarket.com/en/Magic/Cards/{cardFormatted}/Versions")
    cardsSoup = BeautifulSoup(result.text, 'html.parser', parse_only=SoupStrainer(id="ReprintSection"))
    for cardDiv in cardsSoup.div.div.contents:
        print(cardDiv.a.find('h3').get_text())
        listSets.append(cardDiv.a.find('h3').get_text())
        print(cardDiv.a.get('href'))
        cardResult = requests.get(f"https://www.cardmarket.com{cardDiv.a.get('href')}")
        cardSoup = BeautifulSoup(cardResult.text, 'html.parser', parse_only=SoupStrainer(id="tabContent-info")).find("dl")
        #print(cardSoup)
        cardDetailTable, cardDetailValue = cardSoup.find_all("dt"), cardSoup.find_all("dd")
        for x in enumerate(cardDetailTable):
            if fnmatch.filter(x[1], '*Price Trend*'):
                #print(cardDetailValue[x[0]].get_text())
                tempPrice = cardDetailValue[x[0]].get_text().replace(",",".")
                if tempPrice.count(".") > 1: tempPrice = tempPrice.replace('.', '', 1)
                listPrices.append(float(tempPrice.replace(" €", "")))

    cheapIndex = listPrices.index(min(listPrices))

    return(f"; {listSets[cheapIndex]}; {listPrices[cheapIndex]}")

    #for i in enumerate(listSets):
        #print(listSets[i[0]], listPrices[i[0]])

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

