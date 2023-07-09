import kick, asyncio, sys, random, string, re


print("\nKick.com account generater - https://github.com/Shiiivx - Discord: 2yv\n\n")


accCount = int(input("How many accounts do you want to create? "))
print("Select how you would like the usernames for the accounts")
print("[1] Random usernames")
print(f"[2] Choose a name and add numbers from 0 to {accCount} for each username")
usernamesType = int(input())
if usernamesType not in [1,2]: sys.exit("Invalid choice")
print("Select how you would like the passwords for the accounts")
print("[1] Random password for each account")
print("[2] Specific password for all the accounts.")
passwordsType = int(input())
if passwordsType not in [1,2]: sys.exit("Invalid choice")

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

if passwordsType == 1:
    password = None
    pass
elif passwordsType == 2:
    password = input("Choose a password: ")
    if not strongPassword(password):
        sys.exit("Password is not strong enough. Please make sure your password includes at least one uppercase letter, one lowercase letter, one digit, and one symbol, and is at least 8 characters long.")
else:
    sys.exit("Invalid choice")



proxiesFile = input("Would you like to use proxies? If not, leave it empty. If yes, enter the proxies file [IP:PORT]: ")


def generate(username):
    if not password:
        pw = "".join(random.choice(string.ascii_letters + string.digits) for x in range(8)) + random.choice([char for char in """!@#$%^&*()-=_+|;:",.<>?'"""]) + random.choice(string.digits) # In case the random password is generated without a digit :)
    else: pw = password
    if proxiesFile:
        with open(proxiesFile, "r") as f:
            proxy = random.choice(f.readlines()).strip()
    else: proxy = ""
    asyncio.run(kick.kick(email=f"{username}@qwmail.xyz", password=pw, username=username, optionalRequests=False, debug=True, proxy=proxy).create_account())



if usernamesType == 1:
    usernameLength = int(input("What length would you prefer for the random username? "))
    if usernameLength < 4:
        sys.exit("username must be at least 4 characters.")
    for acc in range(accCount):
        randomUsername = "".join(random.choice(string.ascii_lowercase + string.digits) for x in range(usernameLength))
        generate(randomUsername)
    print("Done :)")
elif usernamesType == 2:
    username = input("Enter the username you want: ")
    for acc in range(accCount):
        if len(username) < 3: # Because there is numbers will be added to the username
            sys.exit("username must be at least 3 characters.")
        generate(f"{username}{acc}")
    print("Done :)")
    pass
else:
    sys.exit("Invalid choice")

