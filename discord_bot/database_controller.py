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
        
        self.latest_countryID = 952007 # hardcoded because Nkzlxs dont want to update database
        
        self.latest_active_cases = (new - cured - death)

        """ Get credentials """
        self.cred_file = open(os.path.dirname(os.path.realpath(__file__))+"/credential.json")
        self.credentials = json.load(self.cred_file)
        self.cred_file.close()

    def fetch_sqldata_n_compare(self):
        mydb = self.connectDatabase(connection_type=self.credentials['CURRENT_EXECUTIONER'])

        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM covid19")

        self.result_in_tuples = mycursor.fetchall()

        self.last_confirmedCount = self.result_in_tuples[len(self.result_in_tuples)-1][2]
        self.last_curedCount = self.result_in_tuples[len(self.result_in_tuples)-1][3]
        self.last_deadCount = self.result_in_tuples[len(self.result_in_tuples)-1][4]
        self.last_active_cases = self.result_in_tuples[len(self.result_in_tuples)-1][6]

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
                "d_death": self.difinDead,
                "c_active_cases":self.latest_active_cases,
                "d_active_cases":self.difinActive
            }

    def insert_to_sql(self):
        mydb = self.connectDatabase(connection_type=self.credentials['CURRENT_EXECUTIONER'])

        mycursor = mydb.cursor()
        sql = "INSERT INTO covid19 (countryID, confirmedCount, curedCount, deadCount, timeRecorded, active_cases) VALUES (%s,%s,%s,%s,%s,%s)"
        value = (
            self.latest_countryID, 
            self.latest_confirmedCount,
            self.latest_curedCount,
            self.latest_deadCount,
            self.latest_timestamp,
            self.latest_active_cases
            )

        mycursor.execute(sql, value)
        mydb.commit()

    def calculateDif(self):
        self.difinConfirmed = self.latest_confirmedCount - self.last_confirmedCount
        self.difinCured = self.latest_curedCount - self.last_curedCount
        self.difinDead = self.latest_deadCount - self.last_deadCount

        try:
            self.difinActive = self.latest_active_cases - self.last_active_cases
        except TypeError:
            self.difinActive = 0

    def connectDatabase(self, connection_type=None):
        mydb = None
        mydb = mysql.connector.connect(
            host=self.credentials["DATABASES"][connection_type]["hostname"],
            user=self.credentials["DATABASES"][connection_type]["user"],
            passwd=self.credentials["DATABASES"][connection_type]["password"],
            database=self.credentials["DATABASES"][connection_type]["database_name"]
        )
        return mydb


class db_controller_bot:
    def __init__(self):
        """ Get credentials """
        self.cred_file = open(os.path.dirname(os.path.realpath(__file__))+"/credential.json")
        self.credentials = json.load(self.cred_file)
        self.cred_file.close()
        pass

    def connectDatabase(self, connection_type=None):
        mydb = None
        mydb = mysql.connector.connect(
            host=self.credentials["DATABASES"][connection_type]["hostname"],
            user=self.credentials["DATABASES"][connection_type]["user"],
            passwd=self.credentials["DATABASES"][connection_type]["password"],
            database=self.credentials["DATABASES"][connection_type]["database_name"]
        )
        return mydb

    def checkRecordState(self, userID=None):
        mydb = self.connectDatabase(connection_type=self.credentials['CURRENT_EXECUTIONER'])
        db_cursor = mydb.cursor()
        query = (
            f"SELECT neet_date FROM user_info WHERE user_id = {userID}"
        )
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        mydb.close()
        if len(result) == 0:
            return {"status": "no_result"}
        else:
            return {
                "status": "got_result",
                "neet_date": result[0]
            }

    def updateDatabase(self, userID, neetDate):
        response = self.checkRecordState(userID=userID)
        if response["status"] == "no_result":
            """ Insert new data into database """
            mydb = self.connectDatabase(connection_type=self.credentials['CURRENT_EXECUTIONER'])
            db_cursor = mydb.cursor()
            query = (
                f"INSERT INTO user_info (user_id,neet_date) VALUE ({userID},'{neetDate}')"
            )
            db_cursor.execute(query)
            mydb.commit()
            mydb.close()
            return {"status": "creation done"}
        elif response["status"] == "got_result":
            """ Update the existing database """
            mydb = self.connectDatabase(connection_type=self.credentials['CURRENT_EXECUTIONER'])
            db_cursor = mydb.cursor()
            query = (
                f"UPDATE user_info SET neet_date = ('{neetDate}') WHERE user_id = ({userID})"
            )
            db_cursor.execute(query)
            mydb.commit()
            mydb.close()
            return {"status": "update done"}
