import time
from datetime import datetime as dt

hosts_temp = "hosts"
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"
website_list = ["facebook.com", "www.facebook.com", "www.gmail.com", "gmail.com"]
i = 0

while True:
    if  dt(dt.now().year, dt.now().month, dt.now().day, 10) < dt.now() < dt(dt.now().year, dt.now().month, dt.now().day, 3):
        print("Time constraint satisfied")
        with open(hosts_temp, 'r+') as file:
            content = file.read()
            for site in website_list:
                if site in content:
                    continue
                else:
                    file.write(redirect + " " + site + "\n")
    else:
        with open(hosts_temp, 'r+') as file:
            content = file.readlines()
            file.seek(0)
            file.truncate()
            for line in content:
                if not any(website in line for website in website_list):
                    file.write(line)
    time.sleep(5)
