# Discord bot for Nkzlxs's Discord Server (Docker port branch)

## Python Modules Requirements
Check [requirements.txt](./discord_bot/requirements.txt)

## Running the program
For infomation on running the program.

    python3 24hr_bot.py --help

On server

    python3 24hr_bot.py --main

To test a function

    python3 24hr_bot.py --test [available function]

On Docker
```
docker-compose up --build
```

## Features
1. Auto-updating information on COVID-19 Malaysia
2. Bot commands
3. Random GIF(s) generator
   1. English Keyword
   2. Japanese Keyword
   
## Current available commands:

    say {text} - return any value in {text}
    say myinfo
        return your last message in all the channels in the server,
               the date of your account creation,
               the day(s) since you become a NEET.

    add neet date {YYYYMMDD}- record your date of becoming a NEET

## File and folder explanation

- [covid19_2.py](https://github.com/Nkzlxs/mrslollipop/blob/master/covid19_2.py) -> Code responsible for crawling the webpage [https://kpkesihatan.com/](https://kpkesihatan.com/") by using Python's ["requests"](https://requests.readthedocs.io/en/master/#) library.
- [database_controller.py](https://github.com/Nkzlxs/mrslollipop/blob/master/database_controller.py) -> Code reponsible for reading/updating/comparing data on the server side "[AWS EC2 n2.micro](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&all-free-tier.q=ec2&all-free-tier.q_operator=AND)", interaction with the mysql database is done with the Python's library "[mysql-connector-python](https://pypi.org/project/mysql-connector-python/)"
- [24hr_bot.py](https://github.com/Nkzlxs/mrslollipop/blob/master/24hr_bot.py) -> Code responsible for bot command and report of COVID-19 information and awake random GIF(s) generator
- [oauth2_simplified.py](https://github.com/Nkzlxs/mrslollipop/blob/master/oauth2_simplified.py) -> Code responsible for generating oauth2 access token for gmail's IMAP connection
- [random_en.py](https://github.com/Nkzlxs/mrslollipop/blob/master/random_en.py) -> Code responsible for finding keywords throught a Dictionary API and fetch some related GIF(s) from tenor and post it to discord.
- [random_ja.py](https://github.com/Nkzlxs/mrslollipop/blob/master/random_ja.py) -> Code responsible for fetching a daily received email from FeedBlitz for a Japanese word as a keyword and fetch related GIF(s) from tenor and post it to discord

