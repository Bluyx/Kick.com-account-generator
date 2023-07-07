import tls_client, random, string, json, websocket, time, os, time
from t import get_T
from mail import createEmail, getCode
from console import console

# I know some requests are unnecessary, but there is a 'Set-Cookie' in each request response so i made them optional
# I haven't tested it with proxies, so I couldn't figure out which requests need proxies. Therefore, I simply used proxies in the register request :D

class kick:
    def __init__(self, email, password, username, optionalRequests, debug, follow="", proxy="", delay:int=0):
        self.delay = delay
        self.proxies = {}
        if proxy:
            self.proxies = {
                "proxy": {
                    "http": f"http://{proxy}",
                    "https": f"http://{proxy}"
                }
            }
        if "@qwmail.xyz" not in email: raise Exception("Invalid email. The email must be in the format of '@qwmail.xyz'")
        self.debug = debug
        self.optionalRequests = optionalRequests
        self.follow = follow
        self.client = tls_client.Session(client_identifier="chrome_114", ja3_string="".join(random.choice(string.digits + string.ascii_lowercase) for x in range(1000))) # Idk how but it worked :)
        self.client.get("https://kick.com/", headers={
            "authority": "kick.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        })
        checkUsername = self.client.post("https://kick.com/api/v1/signup/verify/username", headers={
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US",
            "referer": "https://kick.com/",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-xsrf-token": self.client.cookies["XSRF-TOKEN"].replace("%3D", "="),
        }, data=json.dumps({"username":"xQc"})).text
        if "already been taken" in checkUsername:
            input(checkUsername)
            raise Exception(f"Username {username} already taken")
        self.email = createEmail(email)
        if self.email == "Email already registered":
            raise Exception("Email already registered")
        self.debugger(f"Email created: {self.email}", "success")
        self.password = password
        self.username = username
        self.headers = {
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US",
            "authorization": f"Bearer {self.client.cookies['XSRF-TOKEN'].replace('%3D', '=')}",
            "cookie": self.headersCookies(),
            "referer": "https://kick.com/",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-xsrf-token": self.client.cookies["XSRF-TOKEN"].replace("%3D", "="),
        }
    def debugger(self, text, type):
        if self.debug: console.info(text)
    def checkError(self, req):
        if req.status_code not in [200, 204, 201]:
            try: console.error(f"Error in {req.url} - {req.status_code} - {req.json()}")
            except: console.error(f"Error in {req.url} - {req.status_code}")
        return req
    def headersCookies(self):
        # return "; ".join(f"{key}={value}" for key, value in client.cookies.items())
        headersCookies = ""
        for name, value in self.client.cookies.items():
            headersCookies = headersCookies + f"{name}={value}; "
        return headersCookies

    def updateHeaders(self):
        XSRFH = self.client.cookies["XSRF-TOKEN"].replace("%3D", "=")
        self.headers["authorization"] = f"Bearer {XSRFH}"
        self.headers["cookie"] = self.headersCookies()
        self.headers["x-xsrf-token"] = XSRFH
    
    async def create_account(self):
        self.updateHeaders()
        if self.optionalRequests:
            self.checkError(self.client.get("https://kick.com/api/v1/user", headers=self.headers))
            self.updateHeaders()
            self.checkError(self.client.get("https://kick.com/kick-token-provider", headers=self.headers))
            self.updateHeaders()
            self.checkError(self.client.get("https://kick.com/featured-livestreams/non-following", headers=self.headers))
        ws = websocket.create_connection("wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false", header={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"})
        socket_id = json.loads(json.loads(ws.recv())["data"])["socket_id"]
        self.debugger(f"Got socket_id: {socket_id}", "info")
        ws.close()
        self.updateHeaders()
        self.headers["x-socket-id"] = socket_id
        KTP = self.checkError(self.client.get("https://kick.com/kick-token-provider", headers=self.headers)).json()
        self.debugger(f"Got kick token", "info")
        self.updateHeaders()
        self.headers["content-type"] = "application/json"
        self.headers["origin"] = "https://kick.com"
        if self.optionalRequests:
            data = json.dumps({"email":self.email})
            self.checkError(self.client.post("https://kick.com/api/v1/signup/verify/email", headers=self.headers, data=data))
            self.updateHeaders()
            self.checkError(self.client.post("https://kick.com/api/v1/signup/verify/username", headers=self.headers, data={"username":self.username}))
            self.updateHeaders()

        data = json.dumps({"email":self.email})
        self.checkError(self.client.post("https://kick.com/api/v1/signup/send/email", headers=self.headers, data=data))
        self.updateHeaders()
        self.debugger("Waiting for verification code", "info")
        while True:
            code = getCode(self.email)
            if code == "No code" or code == "Error":
                pass
            else:
                break
            time.sleep(1)
        self.debugger(f"Verification code received - {code}", "success")
        data = json.dumps({"code":code,"email":self.email})
        self.checkError(self.client.post("https://kick.com/api/v1/signup/verify/code", headers=self.headers, data=data))
        self.updateHeaders()
        data = {
            "birthdate": f"{str(random.randint(1, 11)).zfill(2)}/{str(random.randint(1, 30)).zfill(2)}/{random.randint(1985, 2004)}", # Todo: DD/MM?
            "username": self.username,
            "email": self.email,
            "cf_captcha_token": "",
            "password": self.password,
            "password_confirmation": self.password,
            "agreed_to_terms": True,
            "newsletter_subscribed": False,
            "t": await get_T(),
            "enable_sms_promo": False,
            "enable_sms_security": False,
            KTP["nameFieldName"]: "",
            KTP["validFromFieldName"]: KTP["encryptedValidFrom"]
        }
        self.checkError(self.client.post("https://kick.com/register", headers=self.headers, data=json.dumps(data), proxy=self.proxies))
        self.updateHeaders()
        # userID = self.checkError(self.client.get("https://kick.com/api/v1/user", headers=self.headers)).json()["id"]
        console.success("Account created!")
        # if self.follow: # Todo
        account = {}
        account["email"] = self.email
        account["password"] = self.password
        for key, value in self.client.cookies.items():
            if len(key) > 35: # Todo
                account["uniqueToken"] = {"key": key, "value": value}
            else:
                account[key] = value
        if not os.path.exists("accounts.json"):
            with open("accounts.json", "w") as file:
                file.write("[]")
        with open("accounts.json", "r") as file:
            accounts = json.loads(file.read())

        accounts.append(account)
        with open("accounts.json", "w") as file:
            file.write(json.dumps(accounts))
        self.debugger("Account saved in accounts.json", "success")
        if self.delay:
            console.info(f"Sleeping for {self.delay} (delay)")
            time.sleep(self.delay)
