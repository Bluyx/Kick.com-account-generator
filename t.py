import time
import random
import base64
from datetime import datetime

canvaURL = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACWCAYAAABkW7XSAAAAAXNSR0IArs4c6QAABGJJREFUeF7t1AEJAAAMAsHZv/RyPNwSyDncOQIECEQEFskpJgECBM5geQICBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAAYPlBwgQyAgYrExVghIgYLD8AAECGQGDlalKUAIEDJYfIEAgI2CwMlUJSoCAwfIDBAhkBAxWpipBCRAwWH6AAIGMgMHKVCUoAQIGyw8QIJARMFiZqgQlQMBg+QECBDICBitTlaAECBgsP0CAQEbAYGWqEpQAgQdWMQCX4yW9owAAAABJRU5ErkJggg=="
def fakeMouseMovement():
    mouseMovements = []
    currentTime = time.time()
    for _ in range(10):
        if mouseMovements:
            lastMove = mouseMovements[-1]
            timeDiff = currentTime - lastMove['s']
            x_diff = random.randint(-100, 100)
            y_diff = random.randint(-100, 100)
            distance = (x_diff ** 2 + y_diff ** 2) ** 0.5
            speed = distance / timeDiff if timeDiff > 0 else 0
            if distance >= 10 and timeDiff >= 0.1:
                mouseMovements.append({
                    'x': lastMove['x'] + x_diff,
                    'y': lastMove['y'] + y_diff,
                    's': currentTime,
                    't': speed,
                })
        else:
            mouseMovements.append({
                'x': random.randint(0, 100),
                'y': random.randint(0, 100),
                's': currentTime,
                't': 0,
            })
        currentTime += random.uniform(0.05, 0.15)
    return '|'.join(f"{m['x']}.{m['y']}.{m['t']}.{m['s']}" for m in mouseMovements)

vendors = [
    'Google Inc.', 
    'Intel Open Source Technology Center', 
    'NVIDIA Corporation', 
    'ATI Technologies Inc.'
]
renderers = [
    'ANGLE (Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0)', 
    'ANGLE (NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0)', 
    'ANGLE (ATI Radeon HD 5700 Series Direct3D11 vs_5_0 ps_5_0)', 
    'Google SwiftShader'
]

screenWidth = random.choice(range(1024, 1920))
screenHeight = random.choice(range(768, 1080))
outerWidth = screenWidth
outerHeight = screenHeight
innerWidth = random.randint(int(screenWidth * 0.6), screenWidth)
innerHeight = random.randint(int(screenHeight * 0.6), screenHeight)
effectiveType = "4g"
downlink = round(random.uniform(2, 10), 2)
rtt = random.randint(50, 150)
def get_T(userAgent):
    w = f"{canvaURL}|{userAgent}|en|Win32|{int(-datetime.now().astimezone().utcoffset().total_seconds()/60)}|{screenWidth}x{screenHeight}|{fakeMouseMovement()}|false|false|false|1|true|{random.choice(vendors)}|{random.choice(renderers)}|{screenWidth}|{screenHeight}|{outerWidth}|{outerHeight}|{innerWidth}|{innerHeight}|1|true|0|Infinity|null|{effectiveType}|{downlink}|{rtt}|true|true|true"
    return base64.b64encode(w.encode('utf-8')).decode('utf-8')
