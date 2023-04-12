from bs4 import BeautifulSoup, SoupStrainer
import requests, math, fnmatch, sys

def main():
    #Clear Output.txt
    f = open('output.txt','w')
    f.close()
    #Start the engine
    readWriteList()
    sys.stdout.write("\n")

def readWriteList():
    #Define newline for fstring
    nl = "\n"
    #Init total price
    total = 0.0

    #Get cards from input.txt
    with open('input.txt', 'r') as file:
        lines = file.readlines()
    
    #Write data to output.txt loop
    for line in enumerate(lines):

        sys.stdout.write('\r')
        sys.stdout.write(f"{line[0]+1}/{len(lines)}")
        sys.stdout.flush()

        f = open('output.txt', 'a')
        tempData = line[1].strip()

        #Check if row starts with a digit, use string after starting number and space as card name
        if tempData[:1].isdigit():
            tempData = tempData.split(" ",1)[1]

        #Get card data to write in line
        newline = f"{getCardPrice(tempData)}"
        rowdata = newline.split("; ")
        total += float(rowdata[2])
        #print(f"Total = {total}")
        #print(f"Writing line: {newline}")
        f.write(f"{newline}{nl}")
    f.write(f"************** Total cost: {total} *********************")
    f.close()
    
    file.close()

def getCardPrice(card):
    listSets, listPrices = [], []
    cardFormatted = formatCard(card)
    result = requests.get(f"https://www.cardmarket.com/en/Magic/Cards/{cardFormatted}/Versions")
    cardsSoup = BeautifulSoup(result.text, 'html.parser', parse_only=SoupStrainer(id="ReprintSection"))
    try:
        for cardDiv in cardsSoup.div.div.contents:
            #print(cardDiv.a.find('h3').get_text())
            listSets.append(cardDiv.a.find('h3').get_text())
            #print(cardDiv.a.get('href'))
            cardResult = requests.get(f"https://www.cardmarket.com{cardDiv.a.get('href')}")
            cardSoup = BeautifulSoup(cardResult.text, 'html.parser', parse_only=SoupStrainer(id="tabContent-info")).find("dl")
            cardDetailTable, cardDetailValue = cardSoup.find_all("dt"), cardSoup.find_all("dd")
            for x in enumerate(cardDetailTable):
                if fnmatch.filter(x[1], '*Price Trend*'):
                    tempPrice = cardDetailValue[x[0]].get_text().replace(",",".")
                    if tempPrice.count(".") > 1: tempPrice = tempPrice.replace('.', '', 1)
                    listPrices.append(float(tempPrice.replace(" €", "")))
    except AttributeError:
        #print("Formatted card name did not return a card. Searching for another format...")
        
        #Set the search URL
        searchPrefix = "https://www.cardmarket.com/en/Magic/Products/Search?searchString="
        searchString = card.replace(" ","+")

        #Get the seach result and parse
        result = requests.get(f"{searchPrefix}{searchString}")
        searchSoup = BeautifulSoup(result.text, 'html.parser').findAll('div',{"class": "flex-column"})
        
        #If search did not return any results, return card with error to be written to output.txt
        if not searchSoup:
            #print("Card not found. Returning error card with price of 0.0 to output")
            return(f"{card}*CARD-NOT-FOUND; {card}*VERSIONS-NOT-FOUND; 0.0")
        else:
            #Get formatted card name from first card url if any found
            #print(searchSoup[1].a.get('href'))
            #return("; POO IN THE LOO; 0.0")
            result = requests.get(f"https://www.cardmarket.com/{searchSoup[1].a.get('href')}")
            formatSoup = BeautifulSoup(result.text, 'html.parser').find_all("a", string="Show Offers")
            #print(formatSoup[0].get('href').split('/')[4])

            return(getCardPrice(formatSoup[0].get('href').split('/')[4]))
    cheapIndex = listPrices.index(min(listPrices))

    return(f"{card}; {listSets[cheapIndex]}; {listPrices[cheapIndex]}")

#TODO use regex instead of multiples of replace
def formatCard(card):
    #print(f"original card name: {card}")
    #formatted = card.replace('-', '') #Remove dashes
    formatted = card.replace(" ", "-") #Replace spaces with dashes
    formatted = formatted.replace(",","") #Remove commas
    formatted = formatted.replace("'","") #Remove apostrophe
    #print(f"formatted card name: {formatted}")
    return formatted

if __name__ == "__main__":
    main()

