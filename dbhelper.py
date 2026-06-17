import mysql.connector


class DB:

    def __init__(self):

        self.conn = None
        self.mycursor = None
        self.error = None

        try:
            self.conn = mysql.connector.connect(
                host='localhost',      # Change if needed
                user='root',
                password='',           # Add your password if required
                database='flights'
            )

            self.mycursor = self.conn.cursor()
            print("✅ Database connected successfully")

        except mysql.connector.Error as err:
            self.error = str(err)
            print(f"❌ Database connection failed: {err}")

    def is_connected(self):
        return self.conn is not None and self.conn.is_connected()

    def fetch_city_names(self):

        if not self.is_connected():
            return []

        query = """
            SELECT DISTINCT Destination AS city
            FROM flights

            UNION

            SELECT DISTINCT Source AS city
            FROM flights

            ORDER BY city
        """

        self.mycursor.execute(query)

        data = self.mycursor.fetchall()

        return [item[0] for item in data]

    def fetch_all_flights(self, source, destination):

        if not self.is_connected():
            return []

        query = """
            SELECT Airline, Route, Dep_Time, Duration, Price
            FROM flights
            WHERE Source = %s AND Destination = %s
        """

        self.mycursor.execute(query, (source, destination))

        return self.mycursor.fetchall()

    def fetch_airline_frequency(self):

        if not self.is_connected():
            return [], []

        query = """
            SELECT Airline, COUNT(*)
            FROM flights
            GROUP BY Airline
            ORDER BY COUNT(*) DESC
        """

        self.mycursor.execute(query)

        data = self.mycursor.fetchall()

        airline = [item[0] for item in data]
        frequency = [item[1] for item in data]

        return airline, frequency

    def busy_airport(self):

        if not self.is_connected():
            return [], []

        query = """
            SELECT airport, COUNT(*) AS total
            FROM (
                SELECT Source AS airport FROM flights
                UNION ALL
                SELECT Destination AS airport FROM flights
            ) t
            GROUP BY airport
            ORDER BY total DESC
        """

        self.mycursor.execute(query)

        data = self.mycursor.fetchall()

        city = [item[0] for item in data]
        frequency = [item[1] for item in data]

        return city, frequency

    def daily_frequency(self):

        if not self.is_connected():
            return [], []

        query = """
            SELECT Date_of_Journey, COUNT(*)
            FROM flights
            GROUP BY Date_of_Journey
            ORDER BY Date_of_Journey
        """

        self.mycursor.execute(query)

        data = self.mycursor.fetchall()

        date = [item[0] for item in data]
        frequency = [item[1] for item in data]

        return date, frequency
