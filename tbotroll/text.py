import requests
a = requests.get('https://reqres.in/api/users/2')
print(a.status_code)