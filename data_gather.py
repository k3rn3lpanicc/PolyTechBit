from readline import insert_text
import sqlite3
from unicodedata import name
import requests
def get_name(code):
    url = f"https://samad.aut.ac.ir/messaging/searchUsers.rose?q={code}&receivers={code}&_=1662652152343"
    request_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en;q=0.9,fa-IR;q=0.8,fa;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Cookie': '969af8aywID_67c5c_data=%7B%22seschk%22%3A%227a3d85bbd671de78c26ed3b81c9e95a8%22%7D; HASH_969af8aywID_67c5c_data=0C093C5D38A30F0062E9CAF37A990C82A020FDB5; 969af8aywID_67c5c_mysid=1; HASH_969af8aywID_67c5c_mysid=9C42D581404D31E721F936995065138F04EC60AA; 969af8aywID_67c5c_mylang=fa; HASH_969af8aywID_67c5c_mylang=0351351D6DAA79321F9C764D1AA411B52AF6D296; JSESSIONID=F331CF4DD05999D46991E5ABE1023C9F; HASH_JSESSIONID=C45942E99FC41FAC0C8885CCA6E9AC0C93C62656',
        'Host': 'samad.aut.ac.ir',
        'Referer': 'https://samad.aut.ac.ir/messaging/list.rose',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    }
    r = requests.get(url , headers=request_headers)
    text = r.text
    text = text.replace("[" , "").replace("]" , "").replace("\"" , "")
    names = []
    for name in text.split(','):
        if name != "":
            names.append({"name" : name.split("(")[1].split(")")[0] , "code" : name.split("(")[0]})
    return names


def insert_names(names):
    conn = sqlite3.connect("usersdb.db")
    for ent in names:
        conn.execute("insert into students values(? , ? , ?)" , [ent['name'] , ent['code'] , ''])
    conn.commit()

