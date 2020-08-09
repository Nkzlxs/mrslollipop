from datetime import datetime

num = 670607102766612503
num_inbin = bin(num) #string
timestamp = num >> 22
account_creation_date = timestamp + 1420070400000
ts = account_creation_date / 1000
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S - %Z'))