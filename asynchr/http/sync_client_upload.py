import requests

with open('mid.bin', 'rb') as f:
    requests.post('http://localhost:4001/images', files={'mid.bin': f})
