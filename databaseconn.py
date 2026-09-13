import psycopg2
from fingerprint import hashes
conn=psycopg2.connect(host="localhost", database="SHAZAM", user="postgres", password="12345678", port="5432")
cursor=conn.cursor()

for filename,combinations in hashes().items():
    cursor.execute("INSERT INTO songs (filename) VALUES (%s) RETURNING id", (filename,))
    song_id = cursor.fetchone()[0]
    bulkData = []
    for hash, time in combinations:
        bulkData.append(( hash, song_id, time*45))
    cursor.executemany("INSERT INTO fingerprints (hash, song_id, time_offset_ms) VALUES (%s, %s, %s)", bulkData)
conn.commit()
cursor.close()
conn.close()