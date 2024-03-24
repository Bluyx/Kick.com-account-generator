from datetime import datetime
from colorama import init, Fore 



init(autoreset=True)
r = Fore.RESET
lr = Fore.LIGHTRED_EX
g = Fore.GREEN
y = Fore.YELLOW

def currentTime(color):
    return datetime.now().time().strftime(f"{color}%H{r}:{color}%M{r}:{color}%S{r}")
def success(text):
    print(f"[{currentTime(g)}] {text}")
def info(text):
    print(f"[{currentTime(y)}] {text}")
def error(text):
    print(f"[{currentTime(lr)}] {text}")



