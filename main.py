import kick, asyncio, sys, random, string, re, nltk, pickle, better_profanity
from console import console

# !!!!!! email must be in "xxxxx@qwmail.xyz" format

print("\nKick.com account generater - https://github.com/Shiiivx - Discord: 2yv\n\n")


accCount = int(input("How many accounts do you want to create? "))
print("Select how you would like the usernames for the accounts")
print("[1] Realistic usernames")
print("[2] Random usernames")
print(f"[3] Choose a name and add numbers from 0 to {accCount} for each username")
usernamesType = int(input())
if usernamesType not in [1,2,3]: sys.exit(console.error("Invalid choice"))
print("Select how you would like the passwords for the accounts")
print("[1] Random password for each account")
print("[2] Specific password for all the accounts.")
passwordsType = int(input())
if passwordsType not in [1,2]: sys.exit(console.error("Invalid choice"))

def strongPassword(password):
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*()-=_+|;:",.<>?]', password):
        return False
    if len(password) < 8:
        return False
    return True

# followChannel = str(input("Do you want to follow a channel on each account created? If not, leave it empty. If yes, type the channel name: "))

if passwordsType == 2:
    password = input("Choose a password: ")
    if not strongPassword(password):
        sys.exit(console.error("Password is not strong enough. Please make sure your password includes at least one uppercase letter, one lowercase letter, one digit, and one symbol, and is at least 8 characters long."))
else:
    password = None


# verifyEmails = input("kick.com does not require a verified email, so would you like to create email verified accounts or not? [y/n]: ").lower()
# if verifyEmails not in ["y","n"]: sys.exit(console.error("Invalid choice"))

proxiesFile = input("Would you like to use proxies? If not, leave it empty. If yes, enter the proxies file: ")

print("How do you want to save the generated accounts?")
print("[1] JSON file with cookies")
print("[2] JSON file without cookies")
print("[3] Text file [email:password]")
saveAs = int(input())
if saveAs not in [1,2,3]: sys.exit(console.error("Invalid choice"))

def generate(username):
    if not password:
        pw = "".join(random.choice(string.ascii_letters + string.digits) for x in range(8)) + random.choice([char for char in """!@#$%^&*()-=_+|;:",.<>?'"""]) + random.choice(string.digits) # In case the random password is generated without a digit :)
    else: pw = password
    if proxiesFile:
        with open(proxiesFile, "r") as f:
            proxy = random.choice(f.readlines()).strip()
    else: proxy = ""
    asyncio.run(kick.kick(email=f"{username}@qwmail.xyz", password=pw, username=username, optionalRequests=False, debug=True, proxy=proxy, verifyEmails="y", saveAs=saveAs).create_account())



if usernamesType == 1:
    if not nltk.corpus.wordnet.synsets("cat"):
        console.info("Downloading WordNet dataset...")
        nltk.download("wordnet", download_dir="nltk_data")
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

    for acc in range(accCount):
        underScore = random.choices(["_", ""], [0.2, 0.8])[0]
        if random.choice([True, False]):
            randomUsername = f"{generate_word('adj')}{generate_word('noun')}{str(random.randint(0, 9999))}{underScore}"
        else:
            randomUsername = f"{generate_word('adj')}{generate_word('noun')}{underScore}{str(random.randint(0, 9999))}"
        generate(randomUsername)
    console.success("Done. Accounts have been generated")
elif usernamesType == 2:
    usernameLength = int(input("What length would you prefer for the random username? "))
    if usernameLength < 4:
        sys.exit(console.error("username must be at least 4 characters."))
    for acc in range(accCount):
        randomUsername = "".join(random.choice(string.ascii_lowercase + string.digits) for x in range(usernameLength))
        generate(randomUsername)
    console.success("Done. Accounts have been generated")
elif usernamesType == 2:
    username = input("Enter the username you want: ")
    for acc in range(accCount):
        if len(username) < 3: # Because there is numbers will be added to the username
            sys.exit(console.error("username must be at least 3 characters."))
        generate(f"{username}{acc}")
    console.success("Done. Accounts have been generated")
    pass
else:
    sys.exit(console.error("Invalid choice"))

