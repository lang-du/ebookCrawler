import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': '939500',
    'host': '127.0.0.1',
    'database': 'book',
    'raise_on_warnings': True
}
query = ("select chapter_url from chapter "
         '''where chapter_url="%s"''')

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# url = {'chapter_url': 'http://www.xbiquge.la/15/15409/21216683.html'}

url = "http://www.xbiquge.la/15/15409/2121668.html"
print(query % (url))
cursor.execute(query % (url))
for urls in cursor:
    if urls:
        print(1111111111111111111111111)
    else:
        print(2222222222222222222222222)

cursor.close()
cnx.close()
