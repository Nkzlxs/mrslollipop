import discord
import os
import json
import asyncio

from datetime import datetime, date, timedelta
from database_controller import db_controller_bot

commands = [
    {"name": "say", "arguments": ["myinfo"]},
    {"name": "add", "arguments": ["neet date"]}
]


class MyClient(discord.Client):

    async def on_ready(self):
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
        channel_id = 723550495662145567
        target = self.get_channel(channel_id)
        await target.send(content=f"Current time: {currentTime}")


def main():
    cred_file = open(os.path.dirname(
        os.path.realpath(__file__))+"/credential.json")
    credentials = json.load(cred_file)
    cred_file.close()
    # await client.start(credentials["DISCORD_BOT_ACCESS_TOKEN"])
    client = MyClient()

    async def test():
        while True:
            await asyncio.sleep(60)
            await client.send_null(client.loop.time())
    client.loop.create_task(test())
    client.run(credentials["DISCORD_BOT_ACCESS_TOKEN"])


if __name__ == "__main__":
    main()
