import psycopg2
import requests
from config import host, user, password, db_name

t = ['Moscow', 'London']

def get_weather():
    weather_list = []
    for city in t:
        res = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&limit=5&lang=ru&appid=4e81203892d1cdd3af3d87b9edc5a224&units=metric')
        weather_list.append((res.json()['name'], res.json()['main']['temp']))
    return weather_list

try:
    conn = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password
    )
    conn.autocommit = True
    cur = conn.cursor()

    # cur.execute("""
    #     CREATE TABLE data_db2 (
    #         id SERIAL PRIMARY KEY,
    #         city VARCHAR(255) NOT NULL,
    #         temp INT
    #     )
    #     """)

    sql="INSERT INTO data_db (city, temp) VALUES(%s, %s)"

    cur.executemany(sql,get_weather())

except Exception:
    print('Errorrrr!!!!')
finally:
    if conn:
        cur.close()
        conn.close()
        print('connect close')

# cur=conn.cursor()
# cur.execute('SELECT version()')
# print(cur.fetchall())
# w = get_weather()
# print(w)
# for i in w:
#     print(i)
# print(get_weather())