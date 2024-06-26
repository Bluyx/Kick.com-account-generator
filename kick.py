import tls_client, random, json, websocket, time, os, time, bs4, sys, console, re
from t import get_T
from mail import createEmail, getVerification
from kopeechka import getMail, getCode
from tls_client import exceptions as tls_exceptions
from kasada import kasada, salamoonder
# from testing.k import kasada
# I know some requests are unnecessary, but there is a 'Set-Cookie' in each request response so i made them optional
class kick:
    def __init__(self, useKopeechka:bool, password, username, kopeechkaToken=None, domain=None, apiURL=None, customDomain=None, imap=None, optionalRequests=False, debug=True, follow="", proxies="", saveAs:int=1, timeout:int=10, delay:int=0):
        self.timeout = timeout
        self.delay = delay
        self.proxies = {}
        self.created = True
        self.saveAs = saveAs
        self.useKopeechka = useKopeechka
        self.imap = imap
        self.useSalamoonder = True
        if proxies:
            self.proxies = f"http://{random.choice(proxies).strip()}"
        self.debug = debug
        self.optionalRequests = optionalRequests # Todo
        self.follow = follow
        self.chromeVersion = "120"
        self.client = tls_client.Session(
            client_identifier=f"chrome{self.chromeVersion}",
            random_tls_extension_order=True,
            # ja3_string="771,4865-4867-4866-49195-49199-52393-52392-49196-49200-49162-49161-49171-49172-156-157-47-53,0-23-65281-10-11-16-5-34-51-43-13-28-65037,29-23-24-25-256-257,0"
            ja3_string=",".join(["771", "-".join([str(random.randint(50, 52392)) for _ in range(15)]), "-".join("45-16-23-65281-35-65037-51-10-43-13-17513-5-0-11-18-27".split("-")), "29-23-24,0"])
        )
        # self.client.proxies = self.proxies
        self.ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        home = self.client.get("https://kick.com/", headers={
            "authority": "kick.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8",
            "sec-ch-ua": f'"Not.A/Brand";v="8", "Chromium";v="{self.chromeVersion}", "Google Chrome";v="{self.chromeVersion}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": self.ua,
        }).text
        self.pjs = "https://kick.com" + bs4.BeautifulSoup(home, "html.parser").find_all("script", {"src": lambda s: s and s.endswith("p.js")})[0]["src"]
        checkUsername = self.client.post("https://kick.com/api/v1/signup/verify/username", headers={
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US",
            "referer": "https://kick.com/",
            "sec-ch-ua": f'"Not.A/Brand";v="8", "Chromium";v="{self.chromeVersion}", "Google Chrome";v="{self.chromeVersion}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-xsrf-token": self.client.cookies["XSRF-TOKEN"].replace("%3D", "="),
        }, data=json.dumps({"username":username})).text
        if "already been taken" in checkUsername:
            raise Exception(f"Username {username} already taken")
        if useKopeechka:
            getEmail = getMail(kopeechkaToken, domain)
            self.kopeechkaToken = kopeechkaToken
            self.email = getEmail["mail"]
            self.emailPassword = getEmail["password"]
            self.mId = getEmail["id"]
        else:
            self.email = createEmail(apiURL, f"{username}@{customDomain}", password)
            if self.email["message"] == "Email already registered":
                raise Exception("Email already registered")
            self.email = self.email["account"]
        console.success(f"Email created: {self.email}")
        self.password = password
        self.username = username
        self.username = username
        self.headers = {
            "authority": "kick.com",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US",
            "authorization": f"Bearer {self.client.cookies['XSRF-TOKEN'].replace('%3D', '=')}",
            "cookie": self.headersCookies(),
            "referer": "https://kick.com/",
            "sec-ch-ua": f'"Chromium";v="{self.chromeVersion}", "Not(A:Brand";v="{self.chromeVersion[1:]}", "Google Chrome";v="{self.chromeVersion}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-xsrf-token": self.client.cookies["XSRF-TOKEN"].replace("%3D", "="),
        }
    def debugger(self, text):
        if self.debug: console.info(text)
    def checkError(self, req):
        if req.status_code == 429:
            print(req.url)
            sys.exit(console.error("Your IP is banned for creating a lot of accounts on the same IP. Change your IP or use proxies."))
        if req.status_code not in [200, 204, 201]:
            self.created = False
            if "The username has already been taken" in req.text:
                console.error(f"Username {self.username} already taken. Changing username...")
                return req
            try: console.error(f"Error in {req.url} - {req.status_code} - {req.json()}")
            except: console.error(f"Error in {req.url} - {req.status_code} - {req.text}")
        return req
    def headersCookies(self):
        # return "; ".join(f"{key}={value}" for key, value in client.cookies.items())
        headersCookies = ""
        for name, value in self.client.cookies.items():
            headersCookies = headersCookies + f"{name}={value}; "
        return headersCookies[:-2]

    def updateHeaders(self):
        XSRF = self.client.cookies["XSRF-TOKEN"].replace("%3D", "=")
        self.headers["authorization"] = f"Bearer {XSRF}"
        self.headers["cookie"] = self.headersCookies()
        self.headers["x-xsrf-token"] = XSRF
    
    def create_account(self):
        self.updateHeaders()
        if self.optionalRequests:
            self.checkError(self.client.get("https://kick.com/api/v1/user", headers=self.headers))
            self.updateHeaders()
            self.checkError(self.client.get("https://kick.com/kick-token-provider", headers=self.headers))
            self.updateHeaders()
            self.checkError(self.client.get("https://kick.com/featured-livestreams/non-following", headers=self.headers))
        ws = websocket.create_connection("wss://ws-us2.pusher.com/app/eb1d5f283081a78b932c?protocol=7&client=js&version=7.6.0&flash=false", header={"User-Agent": self.ua})
        socket_id = json.loads(json.loads(ws.recv())["data"])["socket_id"]
        self.debugger(f"Got socket_id: {socket_id}")
        ws.close()
        self.updateHeaders()
        self.headers["x-socket-id"] = socket_id
        KTP = self.checkError(self.client.get("https://kick.com/kick-token-provider", headers=self.headers)).json()
        self.debugger(f"Got kick token")
        self.updateHeaders()
        self.headers["content-type"] = "application/json"
        self.headers["origin"] = "https://kick.com"
        if self.optionalRequests:
            self.checkError(self.client.post("https://kick.com/api/v1/signup/verify/email", headers=self.headers, data=json.dumps({"email":self.email})))
            self.updateHeaders()
            self.checkError(self.client.post("https://kick.com/api/v1/signup/verify/username", headers=self.headers, data={"username":self.username}))
            self.updateHeaders()

        console.info("Solving kasada...")
        if self.useSalamoonder:
            solveKasada = salamoonder(self.pjs)
        else:
            solveKasada = kasada(self.pjs, "/api/v1/signup/send/email")
        self.client.cookies.set("KP_UIDz-ssn", solveKasada["x-kpsdk-ct"])
        self.client.cookies.set("KP_UIDz", solveKasada["x-kpsdk-ct"])
        XSRF = self.client.cookies["XSRF-TOKEN"].replace("%3D", "=")
        payload = json.dumps({"email":self.email})
        # kasadaCookies = solveKasada["cookies"].split(";")
        # for kasadaCookie in kasadaCookies:
        #     self.client.cookies.set(kasadaCookie.split("=")[0], kasadaCookie.split("=")[1])
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {XSRF}',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Cookie': self.headersCookies(),
            'Origin': 'https://kick.com',
            'Referer': 'https://kick.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.ua,
            'X-Socket-ID': socket_id,
            'X-XSRF-TOKEN': XSRF,
            'accept-language': 'en-US',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-kpsdk-cd': solveKasada["x-kpsdk-cd"],
            'x-kpsdk-ct': solveKasada["x-kpsdk-ct"],
            'x-kpsdk-v': 'j-0.0.0',
        }
        try:
            sendCode = self.checkError(self.client.post('https://kick.com/api/v1/signup/send/email', headers=headers, data=payload, timeout_seconds=self.timeout, proxy=self.proxies))
            if "The browser is not supported" in sendCode.text:
                input()
        except tls_exceptions.TLSClientExeption as err:
            sys.exit(console.error("Probably dead proxy" + str(err)))
        self.updateHeaders()
        self.debugger("Waiting for verification code")
        while True:
            if self.useKopeechka:
                code = getCode(self.kopeechkaToken, self.mId)
                if code == "No code":
                    pass
                else:
                    code = bs4.BeautifulSoup(code, 'html.parser').find(string="Please enter the following code to complete sign up:").find_next('div').text.strip()
                    break
            else:
                apiURL = json.load(open("config.json"))["apiURL"]
                code = getVerification(apiURL=apiURL, email=self.email, password=self.password, sender="ALL", verification_location="subject", imap=self.imap)
                if code["message"] == "Message not found":
                    pass
                else: break
            time.sleep(2)
        console.success(f"Verification code received - {code}")

        self.headers['x-app-platform'] = 'iOS'
        self.headers['x-kpsdk-v'] = "j-0.0.0"
        self.headers['x-app-version'] = '39.1.18'
        data = json.dumps({"code":code,"email":self.email})
        self.checkError(self.client.post("https://kick.com/api/v1/signup/verify/code", headers=self.headers, data=data))
        console.success(f"Verified Account")
        self.updateHeaders()
        XSRF = self.client.cookies["XSRF-TOKEN"].replace("%3D", "=")
        data = {
            "agreed_to_terms": True,
            "isMobileRequest": True,
            "birthdate": f"{str(random.randint(1, 12)).zfill(2)}/{str(random.randint(1, 30)).zfill(2)}/{random.randint(1990, 2003)}",
            "email": self.email,
            "cf_captcha_token": "",
            "password": self.password,
            "password_confirmation": self.password,
            "username": self.username,
            "t": get_T(self.ua),
            KTP["nameFieldName"]: "",
            KTP["validFromFieldName"]: KTP["encryptedValidFrom"]
        }
        headers = {
            'content-length':str(len(payload)),
            'sec-ch-ua':f'"Chromium";v="{self.chromeVersion}", "Not(A:Brand";v="{self.chromeVersion[1:]}", "Google Chrome";v="{self.chromeVersion}"',
            'x-xsrf-token':XSRF,
            'accept-language':'en-US',
            'sec-ch-ua-mobile':'?0',
            'authorization':f'Bearer {XSRF}',
            'user-agent':self.ua,
            'content-type':'application/json',
            'x-socket-id':socket_id,
            'accept':'application/json, text/plain, */*',
            'sec-ch-ua-platform':'"Windows"',
            'origin':'https://kick.com',
            'sec-fetch-site':'same-origin',
            'sec-fetch-mode':'cors',
            'sec-fetch-dest':'empty',
            'referer':'https://kick.com/',
            'accept-encoding':'gzip, deflate, br, zstd',
            'cookie':self.headersCookies()
        }

        try:
            register = self.checkError(self.client.post("https://kick.com/register", headers=self.headers, data=json.dumps(data), proxy=self.proxies, timeout_seconds=self.timeout))
            if register.status_code != 200:
                if register.json()["errors"]["username"][0] == "The username has already been taken":
                    self.username = self.username.rstrip() + str(random.randint(100, 9999))
                    data["username"] = self.username
                    register = self.checkError(self.client.post("https://kick.com/register", headers=self.headers, data=json.dumps(data), proxy=self.proxies, timeout_seconds=self.timeout))
                    # if(register.status_code != 200):
                    #     input(register.json())
                    #     input(data)
                else:
                    input(register.json())
                    input(data)
            try:
                self.token = register.json()["token"]
            except:
                input*(register.json())
            self.created = True
            console.success(f"Account registered | Token: {self.token} | Username: {self.username}")
        except tls_exceptions.TLSClientExeption as err:
            sys.exit(console.error("Probably dead proxy" + str(err)))
        self.updateHeaders()
        self.headers["Authorization"] = f"Bearer {self.token}"
        self.checkError(self.client.get('https://kick.com/emotes/xqc', headers=self.headers)) # Unlock account
        self.updateHeaders()
        if self.created:
            if self.follow: # Todo
                for follow in self.follow:
                    if self.useSalamoonder:
                        solveKasada = salamoonder(self.pjs)
                    else:
                        solveKasada = kasada(self.pjs, f"/api/v2/channels/{follow}/follow")
                    headers = {
                        'Host': 'kick.com',
                        'x-kpsdk-cd': solveKasada["x-kpsdk-cd"],
                        'x-kpsdk-ct': solveKasada["x-kpsdk-ct"],
                        'Accept': 'application/json, text/plain, */*',
                        'x-xsrf-token': self.client.cookies["XSRF-TOKEN"].replace("%3D", "="),
                        'Authorization': f'Bearer {self.token}',
                        'Sec-Fetch-Site': 'cross-site',
                        'x-app-platform': 'iOS',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Sec-Fetch-Mode': 'cors',
                        'x-kpsdk-v': 'j-0.0.0',
                        'Origin': 'https://kick.com',
                        'User-Agent': self.ua,
                        'x-app-version': '39.1.18',
                        'Connection': 'keep-alive',
                        'Sec-Fetch-Dest': 'empty',
                        'Content-Type': 'application/json',
                        'cookie': self.headersCookies()
                    }
                    try:
                        self.checkError(self.client.post(f'https://kick.com/api/v2/channels/{follow}/follow', headers=headers, proxy=self.proxies, timeout_seconds=self.timeout))
                        console.success(f"Followed {follow}")
                    except tls_exceptions.TLSClientExeption as err:
                        sys.exit(console.error("Probably dead proxy" + str(err)))
            self.updateHeaders()
            account = {"cookies": {}}
            account["email"] = self.email
            account["password"] = self.password
            account["token"] = self.token
            if self.saveAs in [1,2]:
                if self.saveAs == 1:
                    for key, value in self.client.cookies.items():
                        account["cookies"][key] = value
                if not os.path.exists("accounts.json"):
                    with open("accounts.json", "w") as file:
                        file.write("[]")
                with open("accounts.json", "r") as file:
                    accounts = json.loads(file.read())
                    accounts.append(account)
                    with open("accounts.json", "w") as file:
                        file.write(json.dumps(accounts))
                console.success("Account saved in accounts.json")
            else:
                with open("accounts.txt", "a") as file:
                    file.write(f"{self.email}:{self.password}:{self.token}\n")
                console.success("Account saved in accounts.txt")
        if self.delay:
            console.info(f"Sleeping for {self.delay} (delay)")
            time.sleep(self.delay)
