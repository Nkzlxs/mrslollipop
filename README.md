# Discord bot for auto-updating information on COVID-19 Malaysia

[main.py](https://github.com/Nkzlxs/mrslollipop/blob/master/main.py) -> Code responsible for awaking the bot, read/update database and post some message to discord

[covid19_2.py](https://github.com/Nkzlxs/mrslollipop/blob/master/covid19_2.py) -> Code responsible for crawling the webpage [https://kpkesihatan.com/](https://kpkesihatan.com/") by using Python's ["requests"](https://requests.readthedocs.io/en/master/#) library.

[database_controller.py](https://github.com/Nkzlxs/mrslollipop/blob/master/database_controller.py) -> Code reponsible for reading/updating/comparing data on the server side "[AWS EC2 n2.micro](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&all-free-tier.q=ec2&all-free-tier.q_operator=AND)", interaction with the mysql database is done with the Python's library "[mysql-connector-python](https://pypi.org/project/mysql-connector-python/)"

[test.py](https://github.com/Nkzlxs/mrslollipop/blob/master/test.py) -> Just a test file for testing python's library function