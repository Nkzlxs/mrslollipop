import discord
import os
import json
import asyncio
from datetime import datetime, date, timedelta
import time
import argparse

import covid19
from database_controller import db_controller_bot
from database_controller import db_controller
import random_ja
import random_en

from discord_slash import SlashCommand


registered_channels = []

def main():

    credentials = readCrediential()

    # client = discord.Client(
    #     intents=discord.Intents(
    #         guilds=True,
    #         members=True,
    #         messages=True
    #     )
    # )
    client = discord.Client(
        intents=discord.Intents.all()
    )

    @client.event
    async def on_ready():
        print('Logged on as {0}!'.format(client.user))
        await client.change_presence(
            activity=discord.Game(name="Online 4.0"),
        )

        client.loop.create_task(check_Covid19_routine(client))

    @client.event
    async def on_guild_join(guild):
        print(f"i joined {guild.name}")
        print(guild.id)
        d = ""
        async for m in guild.fetch_members(limit=1000):
            d += m.name + "\n"
        print(d)

    @client.event
    async def on_guild_remove(guild):
        print(f"i left {guild.name}")

    createSlashCommands(client)

    client.run(credentials['DISCORD_BOT_ACCESS_TOKEN'])


def createSlashCommands(client):
    slash = SlashCommand(
        client,
        sync_commands=True
    )

    @slash.slash(
        name="ping", 
        description="Check your ping with the bot"
    )
    async def _ping(ctx):
        await ctx.respond()
        await ctx.send(f"Pong! ({client.latency*1000}ms)")

    @slash.slash(
        name="anchor", 
        description="This command tells the bot where to post Covid-19 messages"
    )
    async def _anchor(ctx):
        await ctx.respond()
        await ctx.send("This channel: %s have been registered for information!"%ctx.channel.name)
        registered_channels.append(ctx.channel.id)

    @slash.slash(
        name="deanchor", 
        description="This command tells the bot to stop posting Covid-19 messages to this channel"
    )
    async def _deanchor(ctx):
        await ctx.respond()
        await ctx.send("This channel: %s have removed for information!"%ctx.channel.name)
        registered_channels.pop(registered_channels.index(ctx.channel.id))


async def check_Covid19_routine(client):

    while True:

        gmttime = time.gmtime(time.time())

        print(gmttime.tm_min,gmttime.tm_sec)
        if gmttime.tm_min % 30 == 0 and gmttime.tm_sec == 0:
            await update_covid19(client)

        await asyncio.sleep(1)

# async def update_covid19(client):
#     for _ in registered_channels:
#         a_channel = client.get_channel(_)
#         await a_channel.send(
#             content="test",
#         )

async def update_covid19(client):
    """ Get information from web fetcher program"""
    latest_info = covid19.main()

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
        desc += ":chart_with_upwards_trend:Confirmed Count: %d (%+d)\n" % (
            latest_info['new'], response['d_new'])
        desc += ":sparkling_heart:Cured Count: %d (%+d)\n" % (
            latest_info['cured'], response['d_cured'])
        desc += ":skull:Death Count: %d (%+d)\n" % (
            latest_info['death'], response['d_death'])
        desc += ":hospital:Active Count: %d (%+d)\n" % (
            response['c_active_cases'], response['d_active_cases'])

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

        for _ in registered_channels:
            a_channel = client.get_channel(_)
            await a_channel.send(
                content="Hi",
                embed=embed_obj
            )
    else:
        print(f"There's no update! {response['status']}")


def readCrediential():
    cred_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "credential.json")
    with open(cred_path, "r") as f:
        credentials = json.load(f)

    return credentials


tests = [

]


def argParsing():
    argparser = argparse.ArgumentParser(
        description="Covid19 reporter bot of Nkzlxs's Discord Server.")
    argparser.add_argument("--main", action="count",
                           help="Append this to command for running the main bot")

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
        if result.test in tests:
            globals()[result.test]()

    if(result.main == 1 and result.test == None):
        main()


if __name__ == "__main__":
    argParsing()
