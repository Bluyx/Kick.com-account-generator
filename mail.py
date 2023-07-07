import httpx
from time import sleep


def getCode(email, password="Asdf@1234qkk"):
    getCode = httpx.post("http://mail.qwmail.xyz/get_code", data={'email': email, 'password': password})
    if getCode.status_code == 200:
        if getCode.json()['success']:
            return getCode.json()['code']
        elif not getCode.json()['success']:
            return "No code"
    else:
        print((f'Error: {getCode.status_code}'))
        return "Error"


def createEmail(username, password="Asdf@1234qkk"):
    createEmail = httpx.post("http://mail.qwmail.xyz/create_email", data={'username': username, 'password': password})
    if createEmail.status_code == 200:
        if createEmail.json()['message'] == "Account Created":
            return createEmail.json()['account']
        elif createEmail.json()['message'] == "Same name already exists":
            return "Email already registered"
    else:
        print((f'Error: {createEmail.status_code}'))
        return "Error"


