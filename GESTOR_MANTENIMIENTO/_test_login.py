import re
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

r = opener.open("http://127.0.0.1:8000/cuentas/login/")
html = r.read().decode()
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html).group(1)

data = urllib.parse.urlencode(
    {"username": "admin", "password": "Holcim2026*", "csrfmiddlewaretoken": csrf}
).encode()
req = urllib.request.Request(
    "http://127.0.0.1:8000/cuentas/login/",
    data=data,
    headers={"Referer": "http://127.0.0.1:8000/cuentas/login/"},
)
r2 = opener.open(req)
print("login status:", r2.status, r2.geturl())

r3 = opener.open("http://127.0.0.1:8000/")
html3 = r3.read().decode()
print("dashboard status:", r3.status, r3.geturl(), len(html3))
print("Dashboard" in html3)

