import sys, random, string, re, nltk, pickle, better_profanity, json, console, concurrent.futures


print("\nKick.com account generater - https://github.com/Bluyx - Discord: 2yv\n\n")

def strongPassword(password):
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*()-=_+|;:",.?]', password):
        return False
    if len(password) < 8:
        return False
    return True
print("do you want to load settings from config or enter them manually?")
print("[1] Load settings from config")
print("[2] Enter settings manually")
config = json.load(open("config.json"))
settingsType = int(input())
if settingsType not in [1,2]: sys.exit(console.error("Invalid choice"))
if settingsType == 1:
    settings = config["settings"]
else:
    settings = {}
    accCount = int(input("How many accounts do you want to create? "))
    settings["AccountsCount"] = accCount
    print("Select how you would like the usernames for the accounts")
    print("[1] Realistic usernames")
    print("[2] Random usernames")
    print(f"[3] Choose a name and add numbers from 0 to {accCount} for each username")
    print("[4] Usernames from txt file")
    usernamesType = int(input())
    if usernamesType not in [1,2,3, 4]: sys.exit(console.error("Invalid choice"))
    if usernamesType == 4:
        usernamesTxt = input("Enter the txt file path: ")
        settings["usernamesTxt"] = usernamesTxt
    settings["usernamesType"] = usernamesType
    print("Select how you would like the passwords for the accounts")
    print("[1] Random password for each account")
    print("[2] Specific password for all the accounts.")
    passwordsType = int(input())
    if passwordsType not in [1,2]: sys.exit(console.error("Invalid choice"))
    followChannels = str(input("Do you want to follow a channel on each account created? If not, leave it empty. If yes, type the channel name: ")).split(" ")
    settings["follow"] = followChannels
    if passwordsType == 2:
        password = input("Choose a password: ")
        if not strongPassword(password):
            sys.exit(console.error("Password is not strong enough. Please make sure your password includes at least one uppercase letter, one lowercase letter, one digit, and one symbol, and is at least 8 characters long."))
    else:
        password = None
    settings["passwordsType"] = passwordsType
    settings["password"] = password
    salamoonder_apiKey = input("Enter your salamoonder.com api key: ")

    # Todo
    print("what emails do you want to use")
    print("[1] kopeechka")
    print("[2] custom domain (https://github.com/Bluyx/email-api)")
    emails = int(input())
    if emails == 1:
        useKopeechka = True
        config["kopeechka"]["kopeechkaToken"] = input("Enter your kopeechka.store api key: ")
    elif emails == 2:
        useKopeechka = False
        if not config["apiURL"] or not config["imap"] or not config["domain"]: sys.exit(console.error("edit the 'config.json' first"))
    else: sys.exit(console.error("Invalid choice"))
    settings["emailsType"] = emails

    proxiesFile = input("Would you like to use proxies? If not, leave it empty. If yes, enter the proxies file: ")
    settings["proxiesFile"] = proxiesFile
    print("How do you want to save the generated accounts?")
    print("[1] JSON file with cookies")
    print("[2] JSON file without cookies")
    print("[3] Text file [email:password:token]")
    saveAs = int(input())
    if saveAs not in [1,2,3]: sys.exit(console.error("Invalid choice"))
    print("How many threads do you want to use? ")
    threads = int(input())
    settings["threads"] = threads
    settings["saveAs"] = saveAs
    with open("config.json", "w") as f:
        json.dump({"settings": settings, "kopeechka": config["kopeechka"], "salamoonder_apiKey": salamoonder_apiKey, "apiURL": config["apiURL"], "imap": config["imap"], "domain": config["domain"]}, f, indent=4)
        print("Settings saved to config.json")
import kick
def generate(username):
    if settings["passwordsType"] == 1:
        pw = "".join(random.choice(string.ascii_letters + string.digits) for x in range(8)) + random.choice([char for char in """!@#$%^&*()-=_+|;:",.<>?'"""]) + random.choice(string.digits) # In case the random password is generated without a digit :)
    else: pw = settings["password"]
    if settings["proxiesFile"]:
        with open(settings["proxiesFile"], "r") as f:
            proxies = f.readlines()
    else: proxies = ""
    useKopeechka = True if settings["emailsType"] == 1 else False
    kick.kick(
        useKopeechka=useKopeechka,
        password=pw,
        username=username,
        kopeechkaToken=config["kopeechka"]["kopeechkaToken"],
        domain=random.choice(config["kopeechka"]["domains"]),
        apiURL=config["apiURL"],
        customDomain=config["domain"],
        imap=config["imap"],
        optionalRequests=False,
        debug=True,
        follow=settings["follow"],
        proxies=proxies,
        saveAs=settings["saveAs"]
        ).create_account()
def realisticUsername():
    try:
        nltk.corpus.wordnet.synsets("cat")
    except:
        console.info("Downloading WordNet dataset...")
        nltk.download("wordnet")
        console.success("WordNet dataset downloaded successfuly")
    def generate_word(pos):
        try:
            with open(f"{pos}_list.pkl", "rb") as file:
                words = pickle.load(file)
        except FileNotFoundError:
            pos_tag = getattr(nltk.corpus.wordnet, pos.upper())
            words = [word for word in nltk.corpus.wordnet.words() if nltk.corpus.wordnet.synsets(word, pos=pos_tag)]
            with open(f"{pos}_list.pkl", "wb") as file:
                pickle.dump(words, file)

        try:
            with open(f"{pos}_cache.pkl", "rb") as file:
                filtered_words = pickle.load(file)
        except FileNotFoundError:
            console.info("Collecting valid usernames. This might take a while, and it's only for one time")
            filtered_words = [
                word for word in words
                if len(word) <= 7 and not better_profanity.profanity.contains_profanity(word) and not bool(re.search(r"[^a-zA-Z0-9]", word))
            ]
            with open(f"{pos}_cache.pkl", "wb") as file:
                pickle.dump(filtered_words, file)
        if not filtered_words:
            raise ValueError("No random word found")

        return random.choice(filtered_words).capitalize()
    
    username = ""
    while len(username) > 25 or len(username) == 0:
        username = f'{generate_word(random.choice(["adj", "noun", "verb"]))}{random.choice(["_", ""])}{generate_word(random.choice(["adj", "noun", "verb"]))}{random.choice(["_", ""])}{str(random.randint(1, 99999))}'
    return username
def randomUsername():
        usernameLength = int(input("What length would you prefer for the random username? "))
        if usernameLength < 4:
            sys.exit(console.error("username must be at least 4 characters."))
        return "".join(random.choice(string.ascii_lowercase + string.digits) for x in range(usernameLength))
def customUsername():
    username = input("Enter the username you want: ")
    if len(username) < 3: # Because there is numbers will be added to the username
        sys.exit(console.error("username must be at least 3 characters."))
    return username
def genWithThreads():
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings["threads"]) as executor:
        futures = []
        for _ in range(settings["AccountsCount"]):
            if settings["usernamesType"] == 1:
                username = realisticUsername()
            elif settings["usernamesType"] == 2:
                username = randomUsername()
            elif settings["usernamesType"] == 3:
                username = customUsername()
            elif settings["usernamesType"] == 4:
                with open(settings["usernamesTxt"], "r") as f:
                    usernames = f.readlines()
                username = usernames[_]
            else:
                sys.exit(console.error("Invalid choice"))
            futures.append(executor.submit(generate, username))
        for future in concurrent.futures.as_completed(futures):
            future.result()

genWithThreads()
console.success("Done. Accounts have been generated")