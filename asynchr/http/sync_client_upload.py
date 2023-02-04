import requests

with open('mid.bin', 'rb') as f:
    requests.post('http://localhost:4001/images', files={'images/mid.bin': f})
