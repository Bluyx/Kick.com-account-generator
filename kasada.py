import httpx, json, time

apiKey = json.load(open("config.json"))["salamoonder_apiKey"]

def kasada(pjs):
    headers = {
        "Host": "salamoonder.com",
        "Content-Type": "application/json"
    }
    taskId = httpx.post("https://salamoonder.com/api/createTask",headers=headers, data=json.dumps({
        "api_key": apiKey,
        "task": {
            "type": "KasadaCaptchaSolver",
            "pjs": pjs
        }
    }), timeout=50000).json()["taskId"]
    while True:
        res = httpx.post("https://salamoonder.com/api/getTaskResult", headers=headers, data=json.dumps({"api_key": apiKey, "taskId": taskId}), timeout=50000).json()
        if res["status"] == "ready":
            return res["solution"]
        time.sleep(1)

# Using https://github.com/0x6a69616e/kpsdk-solver (doesn't work)

# def kasada(pjs, path="/api/v1/signup/send/email"):
#     return requests.get("https://k.qwmail.xyz/solve", headers={'Content-Type': 'application/json'}, data=json.dumps({"pjs": pjs, "path": path}), timeout=15000, allow_redirects=True).json()

