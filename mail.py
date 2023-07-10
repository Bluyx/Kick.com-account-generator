import httpx
from time import sleep



def getCode(subject, email, password="Asdf@1234qkk"): # No need to put the entire subject; just include any unique word in the subject. For example, in the case of signup, it would be "xxxxx - Sign Up Verification Code." So, you can set the subject as "Sign up," and it doesn't matter if it's in uppercase or lowercase
    getCode = httpx.post("http://mail.qwmail.xyz/get_code", data={"email": email, "password": password, "subject": subject})
    if getCode.status_code == 200:
        if getCode.json()["success"]:
            return getCode.json()["code"]
        elif getCode.json()["message"] == "message not found":
            return "No code"
    else:
        print((f"Error: {getCode.status_code}"))
        return "Error"


def createEmail(username, password="Asdf@1234qkk"):
    createEmail = httpx.post("http://mail.qwmail.xyz/create_email", data={"username": username, "password": password})
    if createEmail.status_code == 200:
        if createEmail.json()["message"] == "Account Created":
            return createEmail.json()["account"]
        elif createEmail.json()["message"] == "Same name already exists":
            return "Email already registered"
    else:
        print((f"Error: {createEmail.status_code}"))
        return "Error"


