import requests
import time
import json

import os


class randomGifEN:
    def __init__(self):
        """ Zeroth, Get credentials """
        cred_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "credential.json")
        cred_file = open(cred_path)
        self.credentials = json.load(cred_file)
        cred_file.close()

        """ Set url variable """
        self.DISCORD_URL = self.credentials["DISCORD_WEBHOOK"]["RANDOMGIF_EN"]

        """Get qualified random word"""
        self.targetWord = self.getRandomWord()
        fileLocation = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "log_en.txt")
        fileLog = open(fileLocation, 'a')
        currentTime = time.strftime("%c %H:%M:%S %Z")
        fileLog.write("%s\n%s\n" % (currentTime, self.targetWord['word']))
        # print(self.targetWord)

        """Search it in tenor gif api"""
        result = self.searchInTenor()

        """Post to discord channel #random-gifs"""
        if result is True:
            fileLog.write("Result is not empty\n")
            self.postToDiscord()
        else:
            fileLog.write("Result is empty\n")
            self.postToDiscord_empty()
        fileLog.close()
        pass

    def getRandomWord(self):
        self.ROOT_WORDAPI_URL = "https://wordsapiv1.p.rapidapi.com/words/"
        self.myHeader = {
            "X-RapidAPI-Host": self.credentials["RAPID_API"]["X-RapidAPI-Host"],
            "X-RapidAPI-Key": self.credentials["RAPID_API"]["X-RapidAPI-Key"]
        }

        """
        1) get a random word (A)
        2) by that random word, search for it , find the 
        highest frequency of word that related to (A) 
        and assign it to (B) to eliminate gif not found
        """
        targetWord = {}
        tries = 0
        while True:
            queryString = {"random": "true"}
            response = requests.get(url=self.ROOT_WORDAPI_URL,
                                    headers=self.myHeader, params=queryString)
            print(response.url)
            response_injson = response.json()

            # print(response_injson)
            points = 0
            targetWord = {}
            try:
                targetWord['word'] = response_injson['word']
                points += 1
            except:
                pass
                # print("No word found!")
            try:
                targetWord['frequency'] = response_injson['results'][0]['frequency']
                points += 1
            except:
                pass
                # print("No frequency found in result!")
            try:
                targetWord['frequency'] = response_injson['frequency']
                points += 1

            except:
                pass
                # print("No frequency found!")
            try:
                targetWord['definition'] = response_injson['results'][0]['definition']
                points += 1
            except:
                pass
                # print("No definition found!")
            try:
                targetWord['synonyms'] = response_injson['results'][0]['synonyms']
                points += 1
            except:
                pass
                # print("No synonyms found!")

            if points == 4:
                print("Nice full matched")
                targetWord['tries'] = tries
                # print(targetWord)
                break
            elif points == 3:
                print("Nice 3 matched")
                targetWord['tries'] = tries
                # print(targetWord)
                break
            else:
                tries += 1
                print("Bad not full matched")

        return targetWord

    def searchInTenor(self):
        self.ROOT_TENORSEARCH_URL = "https://api.tenor.com/v1/search"
        queryString = {
            "key": "7HUWO82A8EI5",
            "q": self.targetWord['word'],
            "limit": 5,
            "media_filter": "minimal",
            "ar_range": "standard"
        }
        # queryString = {
        #     "key": "7HUWO82A8EI5",
        #     "q": "stuff",
        #     "limit": 5,
        #     "media_filter": "minimal"
        # }
        response = requests.get(
            url=self.ROOT_TENORSEARCH_URL, params=queryString)
        print(response.url)
        response_injson = response.json()

        if len(response_injson['results']) == 0:
            return False

        else:
            self.tenorObjectUrls = []
            for obj in response_injson['results']:
                self.tenorObjectUrls.append(obj['media'][0]['gif']['url'])
            return True

    def postToDiscord(self):
        myHeader = {
            "Content-Type": "application/json"
        }

        colorVariant = [
            0xff0000,
            0x00ff00,
            0x0000ff,
            0xff00ff,
            0x00ffff,
        ]

        myEmbeds = []
        counter = 0
        for url in self.tenorObjectUrls:
            myEmbeds.append({
                "title": "Gif No."+str(counter+1),
                "color": colorVariant[counter],
                "image": {
                    "url": url
                }
            })
            counter += 1
        msg_content = ""
        for key in self.targetWord.keys():
            # print(key)
            if key == 'word':
                msg_content += "\nSearch query: \"%s\"" % self.targetWord[key]
            if key == 'frequency':
                msg_content += "\nUsage frequency: %s" % self.targetWord[key]
            if key == 'definition':
                msg_content += "\nDefinition: \"%s\"" % self.targetWord[key]
            if key == 'tries':
                msg_content += "\nDictionary trialNerror: %s times" % self.targetWord[key]
            if key == 'synonyms':
                msg_content += "\nSynonyms:\n"
                counter2 = 1
                for word in self.targetWord[key]:
                    msg_content += "(%d) %s\n" % (counter2, word)
                    counter2 += 1

        myEmbeds.append({
            "title": msg_content,
            "color": 0xffffff,
        })

        queryJson = {
            "content": "@everyone Greetings, here is random %d gifs of today!" % counter,
            "username": "Lollipop Gif",
            "embeds": myEmbeds
        }
        response = requests.post(url=self.DISCORD_URL,
                                 headers=myHeader, json=queryJson)
        print(response.url)
        pass

    def postToDiscord_empty(self):
        myHeader = {
            "Content-Type": "application/json"
        }

        msg_content = "Greetings, today we ran out of luck! *There are no gifs* :cry:"
        for key in self.targetWord.keys():
            # print(key)
            if key == 'word':
                msg_content += "\nSearch query: \"%s\"" % self.targetWord[key]
            if key == 'frequency':
                msg_content += "\nUsage frequency: %s" % self.targetWord[key]
            if key == 'definition':
                msg_content += "\nDefinition: \"%s\"" % self.targetWord[key]
            if key == 'tries':
                msg_content += "\nDictionary trialNerror: %s times" % self.targetWord[key]
            if key == 'synonyms':
                msg_content += "\nSynonyms:\n"
                counter2 = 1
                for word in self.targetWord[key]:
                    msg_content += "(%d) %s\n" % (counter2, word)
                    counter2 += 1

        myEmbeds = []
        myEmbeds.append({
            "title": msg_content,
            "color": 0xf88f88,
        })

        queryJson = {
            "content": "@everyone Greetings",
            "username": "Lollipop Gif",
            "embeds": myEmbeds
        }
        response = requests.post(url=self.DISCORD_URL,
                                 headers=myHeader, json=queryJson)
        print("Tenor Result Empty")
        print(response.url)


if __name__ == "__main__":
    testThing = randomGifEN()
