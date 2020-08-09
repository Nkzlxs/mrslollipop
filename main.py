import discord
import json
import os
from covid19_2 import Covid19MY
from database_controller import db_controller

class MyClient(discord.Client):
    async def on_ready(self):
        """ Print to console saying "i am connected" """
        print('Logged on as {0}!'.format(self.user))

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
            desc += ":chart_with_upwards_trend:Confirmed Count: %d (+%d)\n"%(latest_info['new'],response['d_new'])
            desc += ":sparkling_heart:Cured Count: %d (+%d)\n"%(latest_info['cured'],response['d_cured'])
            desc += ":skull:Death Count: %d (+%d)\n"%(latest_info['death'],response['d_death'])

            title = "COVID-19 Status in\n马来西亚 Malaysia"
            embed_obj= discord.Embed(
                title=title,
                description=desc,
                url=latest_info['article_src']
            )
            embed_obj.set_image(url=latest_info['image_src'])
            embed_obj.set_footer(
                text="From Kpkesihatan"
            )
            a_channel = client.get_channel(694948853165850674)
            await a_channel.send(
                content="@everyone Hi",
                embed=embed_obj
            )
            await client.close()
        else:
            await client.close()


client = MyClient()
current_dir = os.getcwd()
cred_file = open(current_dir+"/credential.json")
credientials = json.load(cred_file)
cred_file.close()
client.run(credientials["DISCORD_BOT_ACCESS_TOKEN"])
