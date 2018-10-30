import phoenixdb
import phoenixdb.cursor

try:
        database_url = 'http://18.188.70.4:8765/'
            conn = phoenixdb.connect(database_url, autocommit=True)

                cursor = conn.cursor()
                    cursor.execute("SELECT count(*) FROM \"sl_metadata\"")
                        #print(cursor.fetchone()['COUNT(1)'])

except Exception as e:
        print(e)
finally:
        conn.close()


