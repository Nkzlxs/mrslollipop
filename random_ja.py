#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imaplib
import base64
import oauth2

import time
import requests
import json

import os


class randomGifJA:
    def __init__(self):
        """ Zeroth, Read newest json file """
        cred_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "credential.json")
        cred_file = open(cred_path)
        self.credentials = json.load(cred_file)
        cred_file.close()

        """First, get a new token"""
        refreshToken = oauth2.RefreshToken(
            client_id=self.credentials["GOOGLE_CREDENTIAL"]["installed"]["client_id"],
            client_secret=self.credentials["GOOGLE_CREDENTIAL"]["installed"]["client_secret"],
            refresh_token=self.credentials["GOOGLE_CREDENTIAL"]["installed"]["refresh_token"])

        """Then, based on that token, generate a new auth string"""
        someString = oauth2.GenerateOAuth2String(
            username=self.credentials["GOOGLE_CREDENTIAL"]["EMAIL_USERNAME"], access_token=refreshToken['access_token'], base64_encode=False)

        """
        Last, setup an authorized IMAP connection using te auth string generated
        It will determine IMAP'd email detected update or not
        and process email to memory
        """
        IMAPupdate = self.customIMAPConnection(auth_string=someString)

        """Action to do when there's update/ no update detected in email"""
        self.updateLog(IMAPupdate)
        if IMAPupdate is True:
            isTenorGifAvailable = self.searchInTenor()
            if isTenorGifAvailable is True:
                self.postToDiscord()
            else:
                self.postToDiscord_empty()

    def customIMAPConnection(self, auth_string):
        # Setup an imap connection to imap.gmail.com using the authentication string
        # generated from Google's OAuth2.0 python library
        imap_connection = imaplib.IMAP4_SSL(host="imap.gmail.com")
        # imap_connection.debug = 4
        imap_connection.authenticate(
            mechanism="XOAUTH2", authobject=lambda x: auth_string)
        imap_connection.select("TestFromIMAP")
        search_result = imap_connection.search(None, 'ALL')
        print(search_result)
        mail_list_number = search_result[1][0].split(' ')
        print(mail_list_number)

        """Write down the latest mail number"""
        fileLocation = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "recentMail.txt")
        record_file = open(fileLocation, "r")
        latest_recorded_no = record_file.read()
        record_file.close()
        print("What i read is %d" % int(latest_recorded_no))
        if int(latest_recorded_no) == int(mail_list_number[len(mail_list_number)-1]):
            print("No recent update")
            # No recent update on mail
            return False
        else:
            print("There's update")
            # There's update on mail

            # Update the latest recording
            modify_record_file = open(fileLocation, "w")
            modify_record_file.write(
                "%s" % mail_list_number[len(mail_list_number)-1])
            modify_record_file.close()

            """Fetch body messages here!!"""
            # Fetch the latest mail BODY[1] PS: idk why fetching body[1] works
            typ, fetch_data = imap_connection.fetch(
                mail_list_number[len(mail_list_number)-1], "(BODY[1])")
            # print(fetch_data[0][1])

            # decode the fetched base64 encoding
            decoded_string = base64.decodestring(fetch_data[0][1])
            # print(decoded_string)

            # List of field i wanted to select
            selected_words = [
                "Japanese Word of the Day",
                "Part of speech:",
                "Example sentence:",
                "Sentence meaning:",
                "Romaji word:",
                "Romaji sentence:"
            ]
            the_keys = [
                'wordoftheday',
                'part',
                's_exam',
                's_meaning',
                'romajiword',
                'romajisentence'
            ]

            self.word_array = {}
            max_length = 300
            pointer = 0
            # Getting the values after the field above
            for p in range(0, len(selected_words)):
                some_string = ""
                # The first p have special implementation
                # stop fetching value when it hits "T"
                if p == 0:
                    startP = decoded_string.find(selected_words[p])
                    endP = decoded_string.find(selected_words[p+1])
                    # print(selected_words[p+1])
                    # print("%d -> %d"%(startP, endP))
                    for i in range(startP+len(selected_words[p]), endP):
                        # Special case, break loop when reaching the first 'T' in To: xxx@domain.com
                        # if decoded_string[i] == 'T':
                        # break
                        if decoded_string[i] == '-':
                            break
                        else:
                            some_string += decoded_string[i]
                # The last p have special implementation
                # stop fetching value when it hits period (.)
                # then adding a period to the value manually
                elif p == len(selected_words)-1:
                    startP = decoded_string.find(selected_words[p])
                    for i in range(startP+len(selected_words[p]), startP + max_length):
                        if decoded_string[i] == '.':
                            some_string += '.'
                            break
                        elif decoded_string[i] == '!':
                            some_string += '!'
                            break
                        else:
                            some_string += decoded_string[i]
                # The p in between 0 and the last one, requires no special implementation
                # stop fetching value when it hits the next field first character
                else:
                    startP = decoded_string.find(selected_words[p])
                    endP = decoded_string.find(selected_words[p+1])
                    for i in range(startP+len(selected_words[p]), endP):
                        some_string += decoded_string[i]
                self.word_array[the_keys[pointer]] = some_string.replace(
                    '\r\n', " ").replace('\t', "")
                pointer += 1
            # print(self.word_array)
            return True

    def searchInTenor(self):
        self.ROOT_TENORSEARCH_URL = "https://api.tenor.com/v1/random"

        # Split the wordoftheday and get it's first element
        # which is in Japanese
        temp = self.word_array['wordoftheday'].split(': ')
        queryString = {
            "key": "7HUWO82A8EI5",
            "q": temp[0],
            "limit": 5,
            "locale": "ja",
            "media_filter": "minimal",
            "ar_range": "standard"
        }
        response = requests.get(
            url=self.ROOT_TENORSEARCH_URL, params=queryString)
        print(response.url)
        print(response.status_code)
        response_injson = response.json()

        if len(response_injson['results']) == 0:
            return False
        else:
            self.tenorObjectUrls = []
            for obj in response_injson['results']:
                self.tenorObjectUrls.append(obj['media'][0]['gif']['url'])
            return True

    def postToDiscord(self):
        """Post to discord stating we found gif"""
        print("Gif found")

        self.DISCORD_URL = "https://discord.com/api/webhooks/715951509438857246/KoBCJhnC3hb1-TFSQh-uYM3YM7Eet3JKFvxEJ2UH6gG90ULIy8AhdtbakK0IEwhqpLhV"
        my_header = {"Content-Type": "application/json"}
        myEmbeds = []

        # Color for the embeds
        colorVariant = [
            0xff1234,
            0x12ff34,
            0x1234ff,
            0xff12ff,
            0x12ffff,
        ]

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

        # Make a ordered textbox
        order = [
            "wordoftheday",
            "romajiword",
            "part",
            "s_exam",
            "romajisentence",
            "s_meaning"
        ]
        msg_content = ""
        for key in order:
            if key == 'wordoftheday':
                temp = self.word_array["wordoftheday"].split(": ")
                msg_content += "\nSearch query: \"%s\"" % temp[0]
                msg_content += "\nEnglish Meaning: \"%s\"" % temp[1]
            if key == 'romajiword':
                msg_content += "\nWord Pronunciation: \"%s\"" % self.word_array[key]
            if key == 'part':
                msg_content += "\nPart of speech: \"%s\"" % self.word_array[key]
            if key == 's_exam':
                msg_content += "\nExample sentence: \"%s\"" % self.word_array[key]
            if key == 'romajisentence':
                msg_content += "\nSentence Pronunciation: \"%s\"" % self.word_array[key]
            if key == 's_meaning':
                msg_content += "\nSentence meaning: \"%s\"" % self.word_array[key]

        # print(msg_content)
        myEmbeds.append({
            "title": "Hi, we found %d gifs today!\n" % (counter),
            "description": msg_content,
            "color": 0x234234
        })
        queryJson = {
            "content": "@everyone　こんにちは、みんな",
            "username": "Lollipop Gif",
            "embeds": myEmbeds
        }

        response = requests.post(url=self.DISCORD_URL,
                                 headers=my_header, json=queryJson)
        print(response.url)
        print(response.status_code)

    def postToDiscord_empty(self):
        """Post to discord stating we can't find any gif"""
        print("empty")

        self.DISCORD_URL = "https://discord.com/api/webhooks/715951509438857246/KoBCJhnC3hb1-TFSQh-uYM3YM7Eet3JKFvxEJ2UH6gG90ULIy8AhdtbakK0IEwhqpLhV"
        my_header = {"Content-Type": "application/json"}
        myEmbeds = []

        # Make a ordered textbox
        order = [
            "wordoftheday",
            "romajiword",
            "part",
            "s_exam",
            "romajisentence",
            "s_meaning"
        ]
        msg_content = ""
        msg_content += "We have no luck today :crying_cat_face: <- Needed to translate to japanese!\n"
        for key in order:
            if key == 'wordoftheday':
                temp = self.word_array["wordoftheday"].split(": ")
                msg_content += "\nSearch query: \"%s\"" % temp[0]
                msg_content += "\nEnglish Meaning: \"%s\"" % temp[1]
            if key == 'romajiword':
                msg_content += "\nWord Pronunciation: \"%s\"" % self.word_array[key]
            if key == 'part':
                msg_content += "\nPart of speech: \"%s\"" % self.word_array[key]
            if key == 's_exam':
                msg_content += "\nExample sentence: \"%s\"" % self.word_array[key]
            if key == 'romajisentence':
                msg_content += "\nSentence Pronunciation: \"%s\"" % self.word_array[key]
            if key == 's_meaning':
                msg_content += "\nSentence meaning: \"%s\"" % self.word_array[key]

        myEmbeds.append({
            "title": "We found no gif today!",
            "description": msg_content,
            "color": 0x234234
        })
        queryJson = {
            "content": "@everyone　こんにちは、みんな",
            "username": "Lollipop Gif",
            "embeds": myEmbeds
        }
        response = requests.post(url=self.DISCORD_URL,
                                 headers=my_header, json=queryJson)
        print(response.url)
        print(response.status_code)

    def testRespondingDiscord(self):
        """Post to discord stating we can't find any gif"""
        print("test to discord")

        self.DISCORD_URL = "https://discord.com/api/webhooks/715951509438857246/KoBCJhnC3hb1-TFSQh-uYM3YM7Eet3JKFvxEJ2UH6gG90ULIy8AhdtbakK0IEwhqpLhV"
        my_header = {"Content-Type": "application/json"}
        myEmbeds = []

        # Make a ordered textbox
        order = "testing"
        msg_content = ""
        for alphabet in order:
            msg_content += alphabet
        myEmbeds.append({
            "title": msg_content,
            "color": 0xabffba
        }
        )
        queryJson = {
            "content": "Testing Discord Functionality",
            "username": "Test Bot",
            "embeds": myEmbeds
        }
        response = requests.post(url=self.DISCORD_URL,
                                 headers=my_header, json=queryJson)
        print(response.url)

    def updateLog(self, flag):
        fileLocation = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "log_ja.txt")
        log_file = open(fileLocation, "a")
        if flag is True:
            currentTime = time.strftime("%c %H:%M:%S %Z")
            log_file.write("%s\n%s\n" %
                           (currentTime, "There's update on mail"))
            log_file.write("Search Query: %s" %
                           self.word_array['wordoftheday'])
        else:
            currentTime = time.strftime("%c %H:%M:%S %Z")
            log_file.write("%s\n%s\n" %
                           (currentTime, "No recent update on mail"))
        log_file.close()


def testing():
    """ Zeroth, read the newest Credential json file """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    jsonfile_path = dir_path + "/newestCredential.json"
    json_read = open(jsonfile_path)
    json_string = json_read.read()
    json_object = json.loads(json_string)
    json_read.close()

    """First, get a new token"""
    refreshToken = oauth2.RefreshToken(
        client_id=json_object['client_id'],
        client_secret=json_object['client_secret'],
        refresh_token=json_object['refresh_token'])
    print(refreshToken)
    """Then, based on that token, generate a new auth string"""
    someString = oauth2.GenerateOAuth2String(
        username="nkzlxs@gmail.com", access_token=refreshToken['access_token'], base64_encode=False)

    print(someString)


if __name__ == "__main__":
    a_jagif = randomGifJA()
    # testing()