import asyncio
import schedule
import time
import sched
import sys
import os

# print(sys.modules['google'])
print(__name__)
print(__loader__)
print(__package__)
print(__spec__)
# print(__path__)
print(__file__)
print(__cached__)
# print(os.path.getatime("~/python_code/"))
print(os.path.join("BRO/", "xd/xd/xd.nkz"))
print(os.path.split("abc/dc/sesfsef/aldfjjakldf/bro.txt"))


a_scheduler = sched.scheduler(time.time, time.sleep)


def print_time(a='something'):
    print("FUNCTION PRINTTIME", time.time(), a)


def printsometimes():
    print("CURRENT TIME", time.time())
    a_scheduler.enter(10, 1, print_time)
    a_scheduler.run()
    print("ENDING TIME", time.time())


# printsometimes()

trigger = False


def manager():
    print("YO MANager")
    global trigger
    trigger = not trigger


async def bro():
    await print("BRO@_@")
    global trigger
    trigger = not trigger

schedule.every(1).second.do(manager)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
#     # if trigger is True:
#     bro()


async def main():
    while True:
        await asyncio.sleep(2)

        print(asyncio.get_running_loop())

        print("RUNNING FOREVER?")
        print(loop_obj.time())
        print('hello')

# loop_obj = asyncio.new_event_loop()
# asyncio.set_event_loop(loop_obj)
loop_obj = asyncio.get_event_loop()
try:

    # loop_obj.call_soon(functools.partial(print, "Hello", flush=True))
    # loop_obj.run_until_complete(main())
    asyncio.ensure_future(main())
    loop_obj.run_forever()
except RuntimeError:
    print("RUNTIME ERROR ON GET RUNNING LOOP")
finally:
    pass
# asyncio.run(main())
