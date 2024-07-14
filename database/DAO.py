from database.DB_connect import DBConnect
from model.State import State
from model.Sighting import Sighting
class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from state s  """

        cursor.execute(query)

        for row in cursor:
            result.append(State(row["id"], row["Name"], row["Capital"], row["Lat"], row["Lng"], row["Area"], row["Population"], row["Neighbors"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllSighting():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from sighting s order by `datetime` asc """

        cursor.execute(query)

        for row in cursor:
            result.append(Sighting(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def cercaArchi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        # ARCO TRA 2 STATI CONFINANTI,
        # PESO = NUMERO DI AVVISTAMENTI CON FORMA S E ANNO Y NEI 2 STATI

        query = """select * from neighbor n"""

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getStatesByYandS(y,c):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
        select s.* 
        from state s, sighting st
        where year(st.datetime) = %s
        and s.id = st.state
        and st.shape = %s
        """

        cursor.execute(query, (y, c))

        for row in cursor:
            result.append(State(row["id"], row["Name"], row["Capital"], row["Lat"], row["Lng"], row["Area"], row["Population"], row["Neighbors"]))

        cursor.close()
        conn.close()
        return result