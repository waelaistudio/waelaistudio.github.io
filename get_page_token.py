import requests

user_token = "EAAU2UrKai4cBSrVPXtOS5qdsxFVD0xeYRR8lxggzNNoKiealZCLsICy0fCVurlZBkqB509XhPZBhqZA44R0BZCovE7ZBJncDH7gxW8GiH7KN8CGUlXVpL3haNtZCGgbVS5D9rPMDYeOTiJPY5ZA4aLGiIEVhzHHLwNL14hsLRHIb1HK7KmlZCx9ZA7D87ILICKg3PH4HawONCZA6y9PtteFQwMAMwb2O5XhdJC2ZBWIZC8NMiKDQK"
page_id = "122109284229473889"

url = f"https://graph.facebook.com/v18.0/me/accounts?access_token={user_token}"
res = requests.get(url).json()

if "data" in res:
    for page in res["data"]:
        if page["id"] == page_id:
            print("PAGE_TOKEN:", page["access_token"])
else:
    print("خطأ في الاستجابة:", res)
