from mail import getCode
from console import console
import time


# If you try to log into any account, you will probably be asked for a verification code. So here is the function :)

def getLoginCode(email): # Email format must be "xxx@qwmail.xyz"
    if "@qwmail.xyz" not in email: raise Exception("Invalid email. The email must be in the format of '@qwmail.xyz'")
    while True:
        code = getCode("Log In", email)
        if code == "No code" or code == "Error":
            print(":")
            pass
        else:
            break
        time.sleep(1)
    console.success(f"Got Login Verification code: {code}")
    return code

getLoginCode(input("Email: "))