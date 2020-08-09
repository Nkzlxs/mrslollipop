import mysql.connector
import time
import json
import os


class db_controller:
    def __init__(self, cured=None, new=None, death=None):
        """ Setup the variables """
        self.latest_confirmedCount = new
        self.latest_curedCount = cured
        self.latest_deadCount = death
        self.latest_timestamp = int(time.time() * 1000)
        # hardcoded because Nkzlxs dont want to update database
        self.latest_countryID = 952007
        self.cred_file = open(os.getcwd()+"/credential.json")
        self.credentials = json.load(self.cred_file)
        self.cred_file.close()

    def fetch_sqldata_n_compare(self):
        # mydb = mysql.connector.connect(
        #     host=self.credentials["DATABASES"]["server"]["hostname"],
        #     user=self.credentials["DATABASES"]["server"]["user"],
        #     passwd=self.credentials["DATABASES"]["server"]["password"],
        #     database=self.credentials["DATABASES"]["server"]["database_name"]
        # )
        mydb = mysql.connector.connect(
            host=self.credentials["DATABASES"]["nkzlxs"]["hostname"],
            user=self.credentials["DATABASES"]["nkzlxs"]["user"],
            passwd=self.credentials["DATABASES"]["nkzlxs"]["password"],
            database=self.credentials["DATABASES"]["nkzlxs"]["database_name"]
        )
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM covid19")

        self.result_in_tuples = mycursor.fetchall()

        self.last_confirmedCount = self.result_in_tuples[len(
            self.result_in_tuples)-1][2]
        self.last_curedCount = self.result_in_tuples[len(
            self.result_in_tuples)-1][3]
        self.last_deadCount = self.result_in_tuples[len(
            self.result_in_tuples)-1][4]

        if(self.latest_confirmedCount == self.last_confirmedCount and self.latest_curedCount == self.last_curedCount and self.latest_deadCount == self.last_deadCount):
            """ If the latest data is same as the older data, return a status of "False" """
            return {"status": False}
            pass
        else:
            """ Else update the database and calculate the difference of the old and new ones """
            self.insert_to_sql()
            self.calculateDif()
            return {
                "status": True,
                "d_new": self.difinConfirmed,
                "d_cured": self.difinCured,
                "d_death": self.difinDead
            }

    def insert_to_sql(self):
        # mydb = mysql.connector.connect(
        #     host=self.credentials["DATABASES"]["server"]["hostname"],
        #     user=self.credentials["DATABASES"]["server"]["user"],
        #     passwd=self.credentials["DATABASES"]["server"]["password"],
        #     database=self.credentials["DATABASES"]["server"]["database_name"]
        # )
        mydb = mysql.connector.connect(
            host=self.credentials["DATABASES"]["nkzlxs"]["hostname"],
            user=self.credentials["DATABASES"]["nkzlxs"]["user"],
            passwd=self.credentials["DATABASES"]["nkzlxs"]["password"],
            database=self.credentials["DATABASES"]["nkzlxs"]["database_name"]
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO covid19 (countryID, confirmedCount, curedCount, deadCount, timeRecorded) VALUES (%s,%s,%s,%s,%s)"
        value = (self.latest_countryID, self.latest_confirmedCount,
                 self.latest_curedCount, self.latest_deadCount, self.latest_timestamp)

        mycursor.execute(sql, value)
        mydb.commit()

    def calculateDif(self):
        self.difinConfirmed = self.latest_confirmedCount - self.last_confirmedCount
        self.difinCured = self.latest_curedCount - self.last_curedCount
        self.difinDead = self.latest_deadCount - self.last_deadCount
