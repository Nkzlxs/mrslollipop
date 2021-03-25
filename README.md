# Discord bot for Nkzlxs's Discord Server (Docker port branch)

## Docker Engine and Docker-compose are needed
`docker` [Link](https://docs.docker.com/engine/install/)

`docker-compose` [Link](https://docs.docker.com/compose/install/)

## Python Modules Requirements
Check [requirements.txt](./discord_bot/requirements.txt)

## Running the program
For infomation on running the program.
`python3 24hr_bot.py --help`

On server (This will run the program in an async loop)
`python3 24hr_bot.py --main`

To test a function
`python3 24hr_bot.py --test [available function]`

On Docker
`docker-compose up --build`

In Case of faulty installation
```
sudo docker container stop $(sudo docker container ps -a | awk '{print $1}')
sudo docker system prune -af
sudo docker-compose up --force-recreate --build -d
```

## Features
1. Auto-updating information on COVID-19 Malaysia
2. Bot commands (Slash commmand as Discord API v8)

## Usage
Make sure to have the appropriate permission for the bot, then on a specific channel, type `/anchor`, that channel will be "registered" for updates.

## File and folder explanation

- [covid19.py](./discord_bot/covid19.py) -> Code responsible for crawling the webpage [https://kpkesihatan.com/](https://kpkesihatan.com/") by using Python's ["requests"](https://requests.readthedocs.io/en/master/#) library.
- [database_controller.py](./discord_bot/database_controller.py) -> Code reponsible for reading/updating/comparing data on the server side "e.g. using free-tiered cloudcompute machine", interaction with the mysql database is done with the Python's library "[mysql-connector-python](https://pypi.org/project/mysql-connector-python/)"
- [bot.py](./discord_bot/bot.py) -> Code responsible for bot command and report of COVID-19 information
