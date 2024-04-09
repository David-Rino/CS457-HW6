import psycopg
from datetime import datetime

class Tracker:
    def __init__(self, hostname, database, username, password, port_id):
        self.hostname = hostname
        self.database = database
        self.username = username
        self.password = password
        self.port_id = port_id

    def logFood(self, conn, log_id, user_id, fdc_id, date):

        try:
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO food_log (log_id, user_id, fdc_id, meal_time)
                VALUES ({log_id}, {user_id}, {fdc_id}, '{date}')
            """)
            conn.commit()
            cur.close()
            print(f"Food with fdc_id: {fdc_id} was logged on {date} with user of: {user_id} - Log ID: {log_id}")
        except Exception as error:
            print(error)

    def addUser(self, conn, user_id, firstName, lastName):

        try:
            cur = conn.cursor()
            cur.execute(f"""
                INSERT INTO users (user_id, first_name, last_name)
                VALUES ({user_id}, '{firstName}', '{lastName}')
            """)
            conn.commit()
            cur.close()
            print(f"User: {firstName} {lastName} has been added with the user ID: {user_id} ")
        except Exception as error:
            print(error)

    def viewNutrients(self, conn, user_id, date):

        try:
            cur = conn.cursor()
            cur.execute(f"""
                SELECT u.first_name, fl.meal_time, f.description, n.name, fn.amount, n.unit_name
                FROM food_log fl 
                JOIN users u ON fl.user_id = u.user_id
                JOIN food f ON fl.fdc_id = f.fdc_id
                JOIN food_nutrient fn ON fn.fdc_id = f.fdc_id
                JOIN nutrient n ON n.id = fn.nutrient_id
                WHERE fl.user_id = {user_id} and fl.meal_time = '{date}'
            """)
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print("First Name: " + row[0].rstrip() + " Meal Time: " + str(row[1]) + " Food Description: " + row[2].rstrip() + " Nutrient Name: " + row[3].rstrip() + " Amount: " + str(row[4]) + " " + row[5].rstrip() )
            cur.close()
        except Exception as error:
            print(error)

    def makeConn(self):
        conn = None
        try:
            conn = psycopg.connect(host=self.hostname, dbname=self.database, user=self.username, password=self.password, port=self.port_id)
        except Exception as error:
            print(error)

        return conn

    def closeConn(self, conn):
        conn.close()


def main():

    print("Welcome to Nutrient Tracker")
    tracker = Tracker('localhost', 'CS 457 Nutrients', 'postgres', 'Rd1258545', 5432 )

    while True:
        print("1. Log Food")
        print("2. View Nutrients")
        print("3. Add new User")
        print("0. Exit Program")
        choice = input("Please Select Choice: ")

        match choice:
            case '1':
                user_id = int(input("Enter userID: "))
                log_id = int(input("Enter logID (###): "))
                fdc_id = int(input("Enter the fdc_id of the food: "))
                date = input("Enter Date (YYYY-MM-DD): ")
                conn = tracker.makeConn()
                tracker.logFood(conn, log_id, user_id, fdc_id, date)
                tracker.closeConn(conn)
            case '2':
                user_id = int(input("Enter userID: "))
                date = input("Enter Date (YYYY-MM-DD): ")
                conn = tracker.makeConn()
                tracker.viewNutrients(conn, user_id, date)
                tracker.closeConn(conn)
            case '3':
                user_id = int(input("Enter new userID: "))
                firstName = input("Enter first name: ")
                lastName = input("Enter last name: ")
                conn = tracker.makeConn()
                tracker.addUser(conn, user_id, firstName, lastName)
                tracker.closeConn(conn)
            case '0':
                break

if __name__ == "__main__":
    main()

