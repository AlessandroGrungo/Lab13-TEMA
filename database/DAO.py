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
    def getAllConfine():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select n.state1 as s1, n.state2 as s2
        from neighbor n 
        group by n.state1, n.state2
        """

        cursor.execute(query)

        for row in cursor:
            result.append((row['s1'], row['s2']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def gettAllEdge( year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
select n.state1 as s1, n.state2 as s2, count(*) as N
from sighting s, neighbor n 
where (s.state = n.state1 or s.state = n.state2)
and n.state1 < n.state2
and year(s.datetime) = %s 
and s.shape = %s
group by n.state1, n.state2
        """

        cursor.execute(query, (year, shape,))

        for row in cursor:
            result.append((row['s1'], row['s2'], row['N']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdge2( year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
select upper(s1.state) as s1ID, upper(s2.state) as s2ID
from sighting s1, sighting s2
where s1.state < s2.state
and date(s1.datetime) = date(s2.datetime)
and year(s1.datetime) = %s
and s1.shape = s2.shape
and s1.shape = %s
"""

        cursor.execute(query, (year, shape,))

        for row in cursor:
            result.append((row['s1ID'], row['s2ID']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges5(min, max):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
select upper(s1.state) as s1ID, upper(s2.state) as s2ID, count(s1.id) as p
from sighting s1, sighting s2
where year(s1.datetime) >= %s
and year(s1.datetime) <= %s
and year(s2.datetime) >= %s
and year(s2.datetime) <= %s
and s1.state < s2.state
and s1.shape = s2.shape
group by s1.state, s2.state
"""

        cursor.execute(query, (min, max, min, max))

        for row in cursor:
            result.append((row['s1ID'], row['s2ID'], row['p']))

        cursor.close()
        conn.close()
        return result
