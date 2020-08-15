import discord
import json
import os


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(
            activity=discord.Game(name="Online Tester 1.0"),
        )
        a_channel = self.get_channel(723550495662145567)
        bro = []
        for x in range(0, 4):
            bro.append(
                discord.Embed(
                    title=f"BroFist {x}",
                    description=f"{x}x{x}={x*x}",
                    color=0xFF00FF,
                )
            )
        a_channel.send(embeds=bro)


cred_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "credential.json")
cred_file = open(cred_file_path)
credentials = json.load(cred_file)
cred_file.close()
client = MyClient()
client.run(credentials["DISCORD_BOT_ACCESS_TOKEN"])