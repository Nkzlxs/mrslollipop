import discord
from covid19_2 import Covid19MY
from database_controller import db_controller

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

        """ Get information from web fetcher program"""
        latest_info = Covid19MY.main(self)

        """ Comparing with database """
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
                description=desc
            )
            embed_obj.set_image(url=latest_info['image_src'])
            a_channel = client.get_channel(694948853165850674)
            await a_channel.send(
                content="@everyone Hi",
                embed=embed_obj
            )
            await client.close()
        else:
            await client.close()


client = MyClient()
client.run('BOT TOKEN HERE!!')
