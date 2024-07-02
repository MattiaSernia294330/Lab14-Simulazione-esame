from database.DB_connect import DBConnect
from model.connessione import Connessione


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.Chromosome 
                from genes g 
                where g.Chromosome !=0"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["Chromosome"])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getArchi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g1.Chromosome  as c1 , g2.Chromosome as c2 , i.GeneID1 , i.GeneID2, i.Expression_Corr as esp
                from interactions i 
                join genes g1 on g1.GeneID = i.GeneID1 
                join genes g2 on g2.GeneID =i.GeneID2 
                where g1.Chromosome != g2.Chromosome and g1.Chromosome != 0 and g2.Chromosome !=0
                group by g1.Chromosome , g2.Chromosome , i.GeneID1 , i.GeneID2, i.Expression_Corr """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(row["c1"], row["c2"], row["GeneID1"],row["GeneID2"], row["esp"]))

        cursor.close()
        conn.close()
        return result