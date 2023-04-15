import requests
JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTIxMzQxOSwiaWF0IjoxNjgwNjA4NjE5LCJqdGkiOiJlMTA0NjAxNjk4Mzk0ODgzOThkNTNlODQyOGNjMjU4NCIsInVzZXJfaWQiOjF9.kRzhbKsKE0As1sF8hjQlDRG9V3BSzEkPXO1GgLP5f-k"
url = "http://127.0.0.1:8000/diary/"
headers = {
    'Authorization': f"Token {JWT}"
}
response = requests.post(url,headers=headers)
print(response.text)