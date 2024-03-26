import httpx, json, time, sys, console

apiKey = json.load(open("config.json"))["salamoonder_apiKey"]

def salamoonder(pjs):
    headers = {
        "Host": "salamoonder.com",
        "Content-Type": "application/json"
    }

    createTask = httpx.post("https://salamoonder.com/api/createTask",headers=headers, data=json.dumps({
        "api_key": apiKey,
        "task": {
            "type": "KasadaCaptchaSolver",
            "pjs": pjs
        }
    }), timeout=50000)
    if "1 second" in createTask.text:
        time.sleep(1)
        return kasada(pjs)
    if createTask.json()["error_description"] == "Invalid API key.":
        sys.exit(console.error("Invalid salamoonder.com api key"))
    taskId = createTask.json()["taskId"]
    if not taskId:
        sys.exit(console.error("Failed to create task"))
    while True:
        res = httpx.post("https://salamoonder.com/api/getTaskResult", headers=headers, data=json.dumps({"api_key": apiKey, "taskId": taskId}), timeout=50000).json()
        if res["status"] == "ready":
            if "This website is not officially supported by Salamoonder" in res["solution"]["error"]:
                sys.exit(console.error("Kick.com is disabled by Salamoonder, wait for an update."))
            return res["solution"]
        time.sleep(1)

# Using https://github.com/0x6a69616e/kpsdk-solver (doesn't work)

def kasada(pjs, path="/api/v1/signup/send/email"):
    return httpx.post("http://127.0.0.1:3033/solve", headers={'Content-Type': 'application/json'}, json={"pjs": pjs, "path": path}, timeout=15000, follow_redirects=True).json()

print(kasada("https://kick.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/p.js"))