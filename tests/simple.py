import requests
import json

payload = {
    'content': "old_test",
    'state': 'old'
}
r = requests.delete('http://127.0.0.1:5000/api/v1.0/todo/16')

print(r.status_code)
print(r.text)
