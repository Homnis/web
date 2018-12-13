import json




a={'confirm': 5}
b=json.dumps(a)
html_message = '请点击下面的链接激活您的帐号<br/><a href="http://127.0.0.1:8000/users/active/%s">请点击我</a>' % ( b)
print(html_message)