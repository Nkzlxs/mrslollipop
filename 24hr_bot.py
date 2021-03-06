import discord
import os
import json
import asyncio
from datetime import datetime, date, timedelta
import time
import argparse

from covid19_2 import Covid19MY
from database_controller import db_controller_bot
from database_controller import db_controller
import random_ja
import random_en

commands = [
    {"name": "say", "arguments": ["myinfo"]},
    {"name": "add", "arguments": ["neet date"]}
]

tests = [
    "testCovid19"
]


class MyClient(discord.Client):

    async def on_ready(self):
        self.tgChannel = 694948853165850674

        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(
            activity=discord.Game(name="Online3.0"),
        )

    async def on_message(self, message):
        print(message.channel)
        if(message.author != self.user):
            msg = message.content
            for x in range(0, len(commands)):
                target = commands[x]["name"]
                pos = msg.find(target)
                if pos == 0:
                    if x == 0:
                        """ Say x reply x and find your status in this server """
                        print(f"User input: {target}")
                        for argument in commands[x]["arguments"]:
                            print(f"User argument: {argument}")
                            if msg.find(argument, 0+len(target)+1) == 0+len(target)+1:
                                await self.send_infomation(message)
                                break
                            else:
                                content = msg[len(
                                    target)+1:len(target)+1+len(msg)]
                                await message.channel.send(content=content)
                                break
                    elif x == 1:
                        """ Save your date when started neet """
                        print(f"User input: {target}")
                        for argument in commands[x]["arguments"]:
                            print(f"User argument: {argument}")
                            if msg.find(argument, 0+len(target)+1) == 0+len(target)+1:
                                rm_len = len(target)+len(argument)+2
                                input_date = msg[rm_len:rm_len+len(msg)]
                                try:
                                    year = int(input_date[0:4])
                                    month = int(input_date[4:6])
                                    day = int(input_date[6:8])
                                    neet_date = date(
                                        year=year, month=month, day=day)
                                    db = db_controller_bot()
                                    response = db.updateDatabase(
                                        userID=message.author.id, neetDate=neet_date)
                                    await message.channel.send(content=f"Data {response['status']}")
                                except ValueError:
                                    await message.channel.send(content="Date input error")
                                break
                    break
        print('Message from {0.author}: {0.content}'.format(message))

    async def send_infomation(self, message):

        async with message.channel.typing():
            content = ""
            author = message.author
            user_id = author.id

            """ Account age """
            account_created_unix = (
                author.id >> 22) + 1420070400000
            account_created_human = datetime.utcfromtimestamp(
                account_created_unix/1000).strftime('%Y-%m-%d %H:%M:%S - UTC')

            header = f"Your account is created on {account_created_human}\n"

            """ Last message history """
            header += "Your last message(s):\n"
            for a_channel in self.get_all_channels():
                if a_channel.type == discord.ChannelType.text and a_channel.category != None:
                    # print(f"{a_channel.name} < {a_channel.category}")
                    try:
                        msg = await a_channel.history(limit=1).flatten()
                        for msg_obj in msg:
                            if msg_obj.author == author:
                                content += a_channel.mention
                                content += msg_obj.content[0:20]
                                content += " ..."
                                content += "\n"
                    except:
                        pass

            """ N-E-E-T Content """
            check_db = db_controller_bot()
            response = check_db.checkRecordState(userID=user_id)
            if response['status'] == "got_result":
                print(response['neet_date'][0])
                try:
                    neet_date = response["neet_date"][0]
                    current_date = date.today()

                    if current_date >= neet_date:
                        time_delta = current_date - neet_date
                        content += f"\nTime since you neet'd: {time_delta.days} day(s)\n"
                    else:
                        time_delta = neet_date - current_date
                        content += f"\nTime till you become neet: {time_delta.days} day(s)\n"
                except ValueError:
                    await message.channel.send(content="Output error")

            """ Message making stage """
            embeds_list = []
            embeds_list.append(
                discord.Embed(
                    title="Your Information",
                    colour=0xFFEE11,
                    description=header+content
                )
            )

            await message.channel.send(embed=embeds_list[0])

    async def send_null(self, currentTime=None):
        # channel_id = 723550495662145567
        channel_id = 739949693982998568
        target = self.get_channel(channel_id)
        await target.send(content=currentTime)

    async def update_covid19(self):
        """ Get information from web fetcher program"""
        latest_info = Covid19MY.main(self)

        """ Process the fetched infomation with the database """
        a_db = db_controller(
            cured=latest_info['cured'],
            new=latest_info['new'],
            death=latest_info['death']
        )
        response = a_db.fetch_sqldata_n_compare()

        """ Decide to post or not """
        if response['status'] is True:
            """ Modify the description """
            desc = ""
            desc += ":chart_with_upwards_trend:Confirmed Count: %d (%+d)\n" % (latest_info['new'], response['d_new'])
            desc += ":sparkling_heart:Cured Count: %d (%+d)\n" % (latest_info['cured'], response['d_cured'])
            desc += ":skull:Death Count: %d (%+d)\n" % (latest_info['death'], response['d_death'])
            desc += ":hospital:Active Count: %d (%+d)\n" % (response['c_active_cases'],response['d_active_cases'])

            title = "COVID-19 Status in\n马来西亚 Malaysia"
            embed_obj = discord.Embed(
                title=title,
                description=desc,
                url=latest_info['article_src']
            )
            embed_obj.set_image(url=latest_info['image_src'])
            embed_obj.set_footer(
                text="From Kpkesihatan"
            )
            a_channel = self.get_channel(self.tgChannel)
            await a_channel.send(
                content="@everyone Hi",
                embed=embed_obj
            )
        else:
            print(f"There's no update! {response['status']}")

    async def update_randomgif_en(self):
        gif_en = random_en.randomGifEN()

    async def update_randomgif_ja(self):
        gif_ja = random_ja.randomGifJA()

def argParsing():
    argparser = argparse.ArgumentParser(description="Covid19 and Random Gif reporter bot of Nkzlxs's Discord Server.")
    argparser.add_argument("--main",action="count",help="Append this to command for running the main bot")

    available_function = ""
    for f in tests:
        available_function += str(f) + ","
    available_function = available_function.strip(",")
    
    argparser.add_argument(
        "--test",
        action="store",
        metavar="TEST-FUNCTION",
        help=f"Append this to command for testing; Choice: [{available_function}]",
        choices=tests
        )
    result = argparser.parse_args()
    if(result.main == None):
        if result.test == "testCovid19":
            testCovid19()
    if(result.main == 1 and result.test == None):
        main()


def main():
    cred_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "credential.json")
    cred_file = open(cred_path)
    credentials = json.load(cred_file)
    cred_file.close()
    client = MyClient()

    async def clock():
        oneway = True
        covid_minute = [0, 30]
        gif_hr = [12]

        while True:
            await asyncio.sleep(1)
            gmttime = time.gmtime(time.time())
            if oneway == True:
                if (gmttime.tm_min == covid_minute[0] or gmttime.tm_min == covid_minute[1]):
                    # await client.send_null(f"It's {gmttime.tm_min}m, i will only say this once!\n Now updating covid19")
                    await client.update_covid19()
                    oneway = False
                if gmttime.tm_hour == gif_hr[0]:
                    await client.update_randomgif_en()
                    await client.update_randomgif_ja()
                    oneway = False
            elif (gmttime.tm_min != covid_minute[0] and gmttime.tm_min != covid_minute[1]) and (gmttime.tm_hour != gif_hr[0]):
                oneway = True
    client.loop.create_task(clock())
    client.run(credentials["DISCORD_BOT_ACCESS_TOKEN"])

def testCovid19():
    cred_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "credential.json")
    cred_file = open(cred_path)
    credentials = json.load(cred_file)
    cred_file.close()
    client = MyClient()
    async def test():
        await asyncio.sleep(25) # Wait for the main program run first
        gate = False
        client.tgChannel = 723550495662145567
        if gate is False:
            await client.update_covid19()
            gate = not gate
            exit("Test done?")
    client.loop.create_task(test())
    client.run(credentials["DISCORD_BOT_ACCESS_TOKEN"])

    
    
    

if __name__ == "__main__":
    argParsing()
