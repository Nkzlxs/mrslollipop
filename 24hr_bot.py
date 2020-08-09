import discord
import os,json
from datetime import datetime

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        all_user = self.users
        # print(all_user)
        for a in all_user:
            if(a.bot == True):
                print(f"{a.name} is a bot, skipping")
            else:
                # print(f"Name:{a.name} Discriminator:{a.discriminator} ID:{a.id}")
                if(a.id == 520070392271077386 or a.id ==293181423060516864 or a.id == 498817814048538625):
                    # await a.send(
                    #     content="i luv you dont tell nkz"
                    # )
                    print(f"Name:{a.name} Discriminator:{a.discriminator} ID:{a.id}")
        # async for message in self.channel.history(limit=1,oldest_first=False):
        #     print(message.content)
        await self.change_presence(
            activity=discord.Game(name="Online3.0"),
            )
        


    async def on_message(self, message):
        commmands:{
            "say":["myinfo"],
            "add":["neet date"]
        }
        print(message.channel)
        if(message.author != self.user):
            msg = message.content
            for command in commmands.keys():
                print(command)
            pos = msg.find(prefix)
            content = None
            if pos == 0:
                if msg.find(commands[0],0+len(prefix)+1) == 0+len(prefix)+1:
                    
                    author = message.author
                    account_created_unix = (author.id >> 22) + 1420070400000
                    account_created_human = datetime.utcfromtimestamp(account_created_unix/1000).strftime('%Y-%m-%d %H:%M:%S - UTC')

                    header = f"Your account is created on {account_created_human}\n"
                    header += "Your last message(s):\n"
                    content = ""
                    for a_channel in self.get_all_channels():
                        
                        if a_channel.type == discord.ChannelType.text and a_channel.category != None:
                            print(a_channel.category)
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
                else:
                    content = msg[0+len(prefix)+1:len(msg)]
                    await message.channel.send(content=content)

        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
cred_file = open(os.getcwd()+"/credential.json")
credentials = json.load(cred_file)
client.run(credentials["DISCORD_BOT_ACCESS_TOKEN"])