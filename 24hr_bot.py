import discord
import os
import json
from datetime import datetime, date, timedelta

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
                    elif x == 1:
                        """ Calculate your days/month/year of neet """
                        print(f"User input: {target}")
                        for argument in commands[x]["arguments"]:
                            print(f"User argument: {argument}")
                            if msg.find(argument, 0+len(target)+1) == 0+len(target)+1:
                                rm_len = len(target)+len(argument)+2
                                input_date = msg[rm_len:rm_len+len(msg)]
                                if len(input_date) == 8:
                                    year = int(input_date[0:4])
                                    month = int(input_date[4:6])
                                    day = int(input_date[6:8])
                                    try:
                                        neet_date = date(
                                            year=year, month=month, day=day)
                                        current_date = date.today()

                                        if current_date >= neet_date:
                                            time_delta = current_date - neet_date
                                            await message.channel.send(content=f"\nTime since you neet'd: {time_delta.days} day(s)")
                                        else:
                                            time_delta = neet_date - current_date
                                            await message.channel.send(content=f"\nTime till you become neet: {time_delta.days} day(s)")
                                    except ValueError:
                                        await message.channel.send(content="Date input error")
                                else:
                                    await message.channel.send(content="Date input error")
                                break

                    break
        print('Message from {0.author}: {0.content}'.format(message))

    async def send_infomation(self, message):
        content = None
        author = message.author
        account_created_unix = (
            author.id >> 22) + 1420070400000
        account_created_human = datetime.utcfromtimestamp(
            account_created_unix/1000).strftime('%Y-%m-%d %H:%M:%S - UTC')

        header = f"Your account is created on {account_created_human}\n"
        header += "Your last message(s):\n"
        content = ""
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
        embeds_list = []
        embeds_list.append(
            discord.Embed(
                title="Your Information",
                colour=0xFFEE11,
                description=header+content
            )
        )
        await message.channel.send(embed=embeds_list[0])


client = MyClient()
cred_file = open(os.getcwd()+"/credential.json")
credentials = json.load(cred_file)
cred_file.close()
client.run(credentials["DISCORD_BOT_ACCESS_TOKEN"])
