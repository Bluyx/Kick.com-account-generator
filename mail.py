import httpx

# change 'http://127.0.0.1:3333' to 

def createEmail(apiURL, email, password): # you better keep the passwords of all the accounts here same to access them later easily
    # apiURL: your API URL you have set up (https://github.com/Bluyx/email-api)
    # email: the email you want to create
    # password: the password for the email
    return httpx.post(f"{apiURL}/create_email", data={"email": email, "password": password}).json()

def getVerification(apiURL, email, password, sender, verification_location, imap):
    # apiURL: your API URL you have set up (https://github.com/Bluyx/email-api)
    # email: the email used in createEmail
    # password: the password used in createEmail
    # sender: the email that sent the verification message, for example "noreply@email.kick.com" (you can set it to "ALL")
    # verification_location: the location of the verification ["subject", "body"]
    # imap: your imap domain, for example "mail.example.com"
    return httpx.post(f"{apiURL}/get_verification", data = {
        "email": email,
        "password": password,
        "sender": sender,
        "verification_location": verification_location,
        "imap": imap
    }).json()




