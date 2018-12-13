import pymysql
from wsgiref.simple_server import make_server
# from wsgiref.simple_server import make_server
#
#
# def findgood():
#     connection=pymysql.connect(host="localhost",port=3306,users="root",password="hy18738991502",database="shopping")
#
#     cursor=connection.cursor()
#     cursor.execute("select username from customer where userid > 0")
#
#     for i in cursor.fetchall():
#         print(list(i)[0])
#     cursor.close()
#     connection.close()
#
#
#
#
# findgood()


from wsgiref.simple_server import make_server
# goodman=["hy"+str(i) for i in range(100)]
#
# badman=["wf"+str(i) for i in range(100)]
#
# doubtman=["hl"+str(i) for i in range(100)]


def finddoubt():
    sum=""
    connection=pymysql.connect(host="localhost",port=3306,user="root",password="hy18738991502",database="shopping")

    cursor=connection.cursor()
    cursor.execute("select username from customer where userid > 0")

    for i in cursor.fetchall():
       sum+=list(i)[0]+"<br>"
    cursor.close()
    connection.close()

    return [sum.encode()]

def findgood():
    sum = ""
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="hy18738991502",
                                 database="shopping")

    cursor = connection.cursor()
    cursor.execute("select username from customer where userid > 0")

    for i in cursor.fetchall():
        sum += list(i)[0]+"<br>"
    cursor.close()
    connection.close()

    return [sum.encode()]

def findbad():
    sum = ""
    connection = pymysql.connect(host="localhost", port=3306, user="root", password="hy18738991502",
                                 database="shopping")

    cursor = connection.cursor()
    cursor.execute("select username from customer where userid > 0")

    for i in cursor.fetchall():
        sum += list(i)[0]+"<br>"
    cursor.close()
    connection.close()

    return [sum.encode()]


def app(env,response):

    response("200 ok", [("Content-type","text/html;charset=utf-8")])

    if env["PATH_INFO"][1:]=="findall":
        return finddoubt()
    elif env["PATH_INFO"][1:]=="findgood":
        return findgood()
    elif env["PATH_INFO"][1:]=="findbad":
        return  findbad()
    else:
        return ["<span style='background:red'>需求：相传明洪武年间，东西两厂各持牛耳把持天下，尤以东厂厂公手中一本<a href='www.baidu.com'>无常薄</a>最是恐怖，只要上了无常薄的人，不论是王公大臣，还是塞外王侯，都是阎王叫你三更死，绝不留人到五更</span>".encode()]





start=make_server("",8000,app)

print("服务器已经启动")

start.serve_forever()