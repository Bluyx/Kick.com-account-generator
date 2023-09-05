import httpx


def getMail(token, domain):
    req = httpx.get(f"http://api.kopeechka.store/mailbox-get-email?site=kick.com&mail_type={domain}&regex=&token={token}&soft=&investor=&type=&password=&subject=&api=2.0").json()
    if req["status"] == "OK":
        return req
    elif req["status"] == "ERROR":
        raise Exception(req["value"])

def getCode(token, id):
    req = httpx.get(f"https://api.kopeechka.store/mailbox-get-message?full=1&id={id}&token={token}&type=json&api=2.0").json()
    if req["status"] == "OK":
        return req["fullmessage"]
    elif req["value"] == "WAIT_LINK":
        return "No code"
    else: raise Exception(req["value"])




