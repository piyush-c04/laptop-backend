import requests

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
res = requests.post("http://localhost:8000/auth/logout", headers=headers)
print(res.status_code, res.json())