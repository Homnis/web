import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
a=os.path.join(BASE_DIR, 'static')
print(a)
print(os.path.join(os.path.join(BASE_DIR, 'static/')))
print(os.path.join(BASE_DIR, 'templates'))