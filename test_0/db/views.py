from django.http import HttpResponse
from . import models


def index(request):
    print("首页被访问了……")
    return HttpResponse("<h1>数据库项目首页面</h1>"
                        "<br/><a href='/db/add'>向表中添加数据</a>"
                        "<br/><a href='/db/showAllToDelete'>删除表中数据</a>"
                        "<br/><a href='/db/showAllToChange'>修改表中数据</a>"
                        "<br/><a href='/db/howToSearch'>搜索表中数据</a>")


def add(request):
    return HttpResponse("""
    <form action='/db/doAdd/' method='get'>
        用户名称： <input type='text' name='name'><br>
        年龄： <input type='text' name='age'><br>
        性别： <input type='text' name='gender'><br>
        住址： <input type='text' name='address'><br>
        
        <button>注册</button>
    </form>
   """)


def doAdd(request):
    # 首先需要接受页面的参数
    name = request.GET["name"]
    age = int(request.GET["age"])
    gender = request.GET["gender"]
    address = request.GET["address"]
    if len(address) == 0:
        try:

            user = models.User(name=name, age=age, gender=gender)
            user.save()

            return HttpResponse("恭喜您，注册成功！！")
        except:
            return HttpResponse("注册失败，请重新注册")
    # 数据校验
    else:
        try:

            user = models.User(name=name, age=age, gender=gender, address=address)
            user.save()

            return HttpResponse("恭喜您，注册成功！！")
        except:
            return HttpResponse("注册失败，请重新注册")


def showAllToDelete(request):
    allUsers = models.User.objects.all()
    res = "<form action='/db/delete/' method='get'><select name='dbs'>"

    for u in allUsers:
        res += "<option value={id}>{name}</option>".format(id=u.id, name=u.name)

    res = res + "</select><button>删除</button></form>"
    return HttpResponse(res)


def delete(request):
    id = request.GET["dbs"]
    # 获得该ID的对象
    user = models.User.objects.get(pk=id)
    user.delete()
    # print(request.GET['dbs'])
    return HttpResponse("<h1>删除成功</h1><a href='/db/index/'>返回主页面</a>")


def showAllToChange(request):
    allUsers = models.User.objects.all()
    res = "<form action='/db/showUserToChange/' method='get'><select name='dbs'>"

    for u in allUsers:
        res += "<option value={id}>{name}</option>".format(id=u.id, name=u.name)

    res = res + "</select><button>确定</button></form>"
    return HttpResponse(res)


def showUserToChange(request):
    id = request.GET["dbs"]
    # 获得该ID的对象
    user = models.User.objects.get(pk=id)
    table = '''
        <table border="1">
            <caption>{name}</caption>
            <tr>
              <td>name</td>
              <td>age</td>
              <td>gender</td>
            </tr>
            <tr>
              <td>{name}</td>
              <td>{age}</td>
              <td>{gender}</td>
            </tr>
        </table>
    '''.format(name=user.name, age=user.age, gender=user.gender)
    select = "<form action='/db/change/' method='get'><select name='changeWhat'>" \
             "<option value=name>name</option>" \
             "<option value=age>age</option>" \
             "<option value=gender>gender</option>" \
             "<option value=address>address</option></select>" \
             "修改为：<input type='text' name='result'>" \
             "<br/><button type='submit' name='id' value='{id}'>确定</button></form>".format(id=id)
    return HttpResponse(table + select)


def change(request):
    id = request.GET["id"]
    changeWhat = request.GET["changeWhat"]
    result = request.GET["result"]
    user = models.User.objects.get(pk=id)
    try:
        if changeWhat == "name":
            user.name = result
        elif changeWhat == "gender":
            user.gender = result
        elif changeWhat == "age":
            user.age = int(result)
        elif changeWhat == "address":
            user.age = result
        user.save()
        return HttpResponse("修改成功")
    except:
        return HttpResponse("修改失败")


def howToSearch(request):
    select = "<form action='/db/search/' method='get'><select name='searchWhat'>" \
             "<option value=name>name</option>" \
             "<option value=age>age</option>" \
             "<option value=gender>gender</option>" \
             "<option value=id>id</option></select>" \
             "：<input type='text' name='inside'>" \
             "<button>搜索</button></form>"
    return HttpResponse(select)


def search(request):
    # 共有四项可查:id/name/age/gender
    searchWhat = request.GET["searchWhat"]
    inside = request.GET["inside"]
    try:
        if searchWhat == "name":
            users = models.User.objects.filter(name__contains=inside)
        elif searchWhat == "gender":
            users = models.User.objects.filter(gender=inside)
        elif searchWhat == "age":
            users = models.User.objects.filter(age=int(inside))
        elif searchWhat == "id":
            users = models.User.objects.filter(id=int(inside))

        table = "<table border='1'><caption>查询结果</caption>" \
                "<tr><td>id</td><td>name</td><td>age</td><td>gender</td><td>address</td></tr>"
        res = ""
        # users是一个queryset类，里面是User对象
        if len(users)!=0:
            for i in users:
                res+="<tr><td>{id}</td><td>{name}</td><td>{age}</td><td>{gender}</td><td>{address}</td>" \
                     "</tr>".format(id=i.id,name=i.name,age=i.age,gender=i.gender,address=i.address)
            res=res+"</tabel>"
            return HttpResponse(table+res)
        else:
            return HttpResponse("没有相关数据")
    except:
        return HttpResponse("查询失败")
