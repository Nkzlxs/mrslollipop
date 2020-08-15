import time
import os

def main():
    pro = int(time.time() * 1000)  # convert to milliseconds and Integer
    gmttime = time.gmtime(time.time())
    print(f"{gmttime.tm_year}年{gmttime.tm_mon}月{gmttime.tm_mday}日{gmttime.tm_hour}时{gmttime.tm_min}分{gmttime.tm_sec}秒")
    fileLocation = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "log.txt")
    print(fileLocation)


if __name__ == "__main__":
    main()

# try:
#     neet_date = date(
#         year=year, month=month, day=day)
#     current_date = date.today()

#     if current_date >= neet_date:
#         time_delta = current_date - neet_date
#         await message.channel.send(content=f"nTime since you neet'd: {time_delta.days} day(s)")
#     else:
#         time_delta = neet_date - current_date
#         await message.channel.send(content=f"\nTime till you become neet: {time_delta.days} day(s)")
# except ValueError:
#     await message.channel.send(content="Date input error")
