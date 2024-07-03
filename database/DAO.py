from database.DB_connect import DBConnect
from model.Avvistamento import Avvistamento
from model.Stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllState():
        risultato = []
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM state')
        for row in cursor:
            risultato.append(Stato(row["id"], row["Name"], row["Capital"], row["Lat"],
                                   row["Lng"], row["Area"], row["Population"], row["Neighbors"]))
        cursor.close()
        conn.close()
        return risultato

    @staticmethod
    def getAllAvvistamento():
        risultato = []
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM sighting S ORDER BY S.datetime')
        for row in cursor:
            risultato.append(Avvistamento(row["id"], row["datetime"], row["city"], row["state"],
                                          row["country"], row["shape"], row["duration"], row["duration_hm"],
                                          row["comments"], row["date_posted"], row["latitude"], row["longitude"]))
        cursor.close()
        conn.close()
        return risultato
    @staticmethod
    def cercaArchi(shape, year):
        result = []
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT N.state1 as n1, N.state2 as n2, COUNT(*) as N
        FROM neighbor N, sighting S 
        WHERE (N.state1 = S.state OR N.state2 = S.state)
        AND S.shape = %s 
        AND YEAR(S.datetime) = %s
        GROUP BY N.state1, N.state2
        """
        cursor.execute(query, (shape, year))
        for row in cursor:
            result.append((row["n1"], row["n2"], row["N"]))
        cursor.close()
        conn.close()
        return result