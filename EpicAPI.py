from epicstore_api import EpicGamesStoreAPI, OfferData
games = EpicGamesStoreAPI().get_free_games()['data']['Catalog']['searchStore']['elements']

class Games():
    def __init__(self, allTheInfo):
        self.id = allTheInfo['id']
        self.title = allTheInfo['title']
        self.startDate = allTheInfo['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate']
        self.endDate = allTheInfo['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate']
        self.thumbnail = allTheInfo['keyImages'][0]['url']
        self.savings = allTheInfo['price']['totalPrice']['discount']
        self.savingsString = str("$"+str(self.savings)[:-2]+"."+str(self.savings)[-2:])
        self.url = ("https://www.epicgames.com/store/en-US/p/"+ str(allTheInfo['productSlug']))
        self.fancyEndDate = self.endDate[8:10] + "/" + self.endDate[5:7] + "/" + self.endDate[0:4]

    def __str__(self):
        string = ("Hey! "+ self.title+ " is free on the Epic Games Store until "+ self.fancyEndDate+ ". \nBe sure to get it now to save "+self.savingsString+ " \nClick here to go directly to the store <"+self.url+ ">\n"+ self.thumbnail)
        return(str(string))

def getGamesList():
    gameList = []
    for x in games:
        if x['promotions'] != None:
            if x['promotions']['promotionalOffers'] != []:
                gameList.append(Games(x))

    return(gameList)


if __name__ == "__main__":
    print (EpicGamesStoreAPI().get_free_games())
    newGames = getGamesList()
    for x in newGames:
        print(x)
        """
        print("Game id : ", x.id)
        print("Game title : ", x.title)
        print("Game startDate : ", x.startDate)
        print("Game endDate : ", x.endDate)
        print("Game thumbnail : ", x.thumbnail)
        print("Game savings : ", x.savings)
        print("Game url : ", x.url)
        print("\n")
        """
