import psycopg

class Tracker:
    def __init__(self, name):
        self.user_id = '0'
        self.name = name

        def logFood(self, conn, cur):
            food = "test"
            date = 123455


def main():
    hostname = 'localhost'
    database = 'CS 457 Nutrients'
    username = 'postgres'
    pwd = 'Rd1258545'
    port_id = 5432
    conn = None
    cur = None

    try:
        conn = psycopg.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id)
        cur = conn.cursor()

    except Exception as error:
        print(error)
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    main()

