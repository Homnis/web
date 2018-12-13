import pymysql
from wsgiref.simple_server import make_server


def finddoubt():
    sum = ""
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="shopping")

    cursor = connection.cursor()
    params = []
    cursor.execute("select userName from customer", params)

    for i in cursor.fetchall():
        # print(i[0])
        # print("end")
        sum += i[0]+"<br>"
    cursor.close()
    connection.close()

    return [sum.encode()]


def findgood():
    sum = ""
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="123456",
                                 database="shopping")

    cursor = connection.cursor()
    params = []
    cursor.execute("select userName from customer", params)

    for i in cursor.fetchall():
        sum += i[0] + "<br>"
    cursor.close()
    connection.close()

    return [sum.encode()]


def findbad():
    sum = ""
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="123456",
                                 database="shopping")

    cursor = connection.cursor()
    params = []
    cursor.execute("select userName from customer", params)

    for i in cursor.fetchall():
        sum += i[0]+"<br>"
    cursor.close()
    connection.close()

    return [sum.encode()]


def app(env, response):

    response("200 ok", [("Content-type", "text/html;charset=utf-8")])

    if env["PATH_INFO"][1:] == "findall":
        return finddoubt()
    elif env["PATH_INFO"][1:] == "findgood":
        return findgood()
    elif env["PATH_INFO"][1:] == "findbad":
        return findbad()


start = make_server("", 8090, app)

print("服务器已经启动")

start.serve_forever()