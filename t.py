import asyncio, base64, json
from pyppeteer import launch, errors


xWe = "!kickCE0105"
async def get_T(userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"):
    s = {}
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    s["t"] = await page.evaluate("new Date().getTimezoneOffset();")
    s["canva"] = await page.evaluate(f'const canvas = document.createElement("canvas"); const nx = canvas.getContext("2d"); nx && nx.fillText("{xWe}", 0, 0); canvas.toDataURL();')
    s["r"] = await page.evaluate("`${window.screen.width}x ${window.screen.height}`")
    s["connection"] = await page.evaluate("const H = navigator.connection || navigator.mozConnection || navigator.webkitConnection; const j = {type: H ? H.type : null, effectiveType: H ? H.effectiveType : null, downlink: H ? H.downlink : null, rtt: H ? H.rtt : null}; j;")
    PWe = """
    const t = document.createElement("canvas")
    const e = t.getContext("webgl") || t.getContext("experimental-webgl");
    const n = e.getExtension("WEBGL_debug_renderer_info");
    const i = e.getParameter(n.UNMASKED_VENDOR_WEBGL);
    const r = e.getParameter(n.UNMASKED_RENDERER_WEBGL);
    const res = {vendor: i, renderer: r};
    res
    """
    s["PWe"] = await page.evaluate(PWe)
    s["screen"] = await page.evaluate("let screen = {w: window.screen.width, C: window.screen.height, I: window.outerWidth, k: window.outerHeight, P: window.innerWidth, D: window.innerHeight}; screen;")
    batteryScript = """
    () => {
        return navigator.getBattery().then(t => {
            return { level: t.level, charging: t.charging, chargingTime: t.chargingTime, dischargingTime: t.dischargingTime };
        });
    }    """
    s["battery"] = await page.evaluate(batteryScript)
    await browser.close()
    t = f"{s['canva']}|{userAgent}|en-US|Win32|{s['t']}|{s['r']}||false|false|false|0|false|{s['PWe']['vendor']}|{s['PWe']['renderer']}|{s['screen']['w']}|{s['screen']['C']}|{s['screen']['I']}|{s['screen']['k']}|{s['screen']['P']}|{s['screen']['D']}|{s['battery']['level']}|{s['battery']['charging']}|{s['battery']['chargingTime']}|{s['battery']['dischargingTime']}|undefined|{s['connection']['effectiveType']}|{s['connection']['downlink']}|{s['connection']['rtt']}|true|true|true"

    return base64.b64encode(t.encode('utf-8')).decode('utf-8')
    
