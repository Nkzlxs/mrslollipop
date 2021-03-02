import time
import os
import sys
import mysql.connector
import json

def main(input_cmd):
    cred_file = open(os.path.dirname(os.path.realpath(__file__))+"/credential.json")
    credentials = json.load(cred_file)
    cred_file.close()

    counter = 0

    connection_type = credentials['CURRENT_EXECUTIONER']
    mydb = None
    while True:
        try:
            mydb = mysql.connector.connect(
                host=credentials["DATABASES"][connection_type]["hostname"],
                user=credentials["DATABASES"][connection_type]["user"],
                passwd=credentials["DATABASES"][connection_type]["password"],
                database=credentials["DATABASES"][connection_type]["database_name"]
            )
            print(input_cmd[1])
            return
        except:
            time.sleep(1)
            counter += 1
            print(counter,"Waiting MySql to be online")


if __name__ == '__main__':
    main(sys.argv)
    os.system(sys.argv[1])
