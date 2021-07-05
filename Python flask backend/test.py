from flask.wrappers import Response
import requests
BASE = "http://127.0.0.1:5000/"
response = requests.get(
    BASE + "/user/king", data={"gender": "male", "age": "14", "name":"king","id":"56"})
print(response.json())  
