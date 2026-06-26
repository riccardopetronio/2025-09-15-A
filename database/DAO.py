from database.DB_connect import DBConnect
from model.piloti import Pilota


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPiloti(annoIn, annoFine):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select d.*
                from results r, drivers d, races r2 
                where d.driverId = r.driverId and r.`position` is not null 
                and r.raceId = r2.raceId and YEAR(r2.`date`)>= %s and YEAR(r2.`date`)<= %s
                group by d.driverId"""

        cursor.execute(query, (annoIn, annoFine))

        for row in cursor:
            results.append(Pilota(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getConnessioni(annoIn, annoFine):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as d1, r2.driverId as d2, count(*) as peso
                from results r1, results r2, races ra
                where r1.raceId = r2.raceId
                  and r1.constructorId = r2.constructorId
                  and r1.driverId < r2.driverId
                  and r1.`position` is not null
                  and r2.`position` is not null
                  and r1.raceId = ra.raceId
                  and YEAR(ra.`date`) >= %s and YEAR(ra.`date`) <= %s
                group by r1.driverId, r2.driverId"""

        cursor.execute(query, (annoIn, annoFine))

        for row in cursor:
            results.append((row["d1"], row["d2"], row["peso"]))

        cursor.close()
        conn.close()
        return results

