from mail import getVerification
from console import console
import time, json


# If you try to log into any account, you will be asked for a verification code. So here is the function
# if you used kopeechka.store then you can't get the login verification code

config = json.load(open("config.json"))

def getLoginCode(email, password):
    while True:
        code = getVerification(config["apiURL"], email, password, "ALL", "subject", config["imap"])
        if code == "No code" or code == "Error":
            print(":")
            pass
        else:
            break
        time.sleep(1)
    console.success(f"Got Login Verification code: {code}")
    return code

getLoginCode(input("Email: "), input("Password: "))