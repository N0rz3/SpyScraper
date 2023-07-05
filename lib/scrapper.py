from lib.requests import Requests
import lib.formats
from lib.colors import *
from bs4 import BeautifulSoup
import re
import json
import whois
import random


with open("data.json", "r") as file:
    data = json.load(file)

with open("useragents.txt", "r") as user_file:
    user = user_file.read().split('\n')

async def checker() -> bool:
    if data["target_url"] == "":
        return False
    else:
        return True


async def extract_emails(url):
        try:
            headers = {
"User-Agent": f"{random.choice(user)}"
            }

            response = await Requests(url, headers=headers).sender()
            email_regex = lib.formats.EMAIL
            emails = re.findall(email_regex, response.text)

            return emails
        
        except:
            return()


async def extract_href(url):
        try:
            headers = {
"User-Agent": f"{random.choice(user)}"
            }

            response = await Requests(url, headers=headers).sender()
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')
            hrefs = [link.get('href') for link in links]
            return hrefs

        except:
            return()

async def author_infos(url: str):
        try:
            headers = {
"User-Agent": f"{random.choice(user)}"
            }

            response = await Requests(url, headers=headers).sender()

            soup = BeautifulSoup(response.text, 'html.parser')
            author_element = soup.find('meta', {'name': 'author'})
            if author_element:
                return author_element['content']
            else:
                return None
            
        except:
            return()

async def extract_phone(url: str) -> list:
    try:
        headers = {
"User-Agent": random.choice(user)
        }

        response = await Requests(url, headers=headers).sender()
        phone_regex = lib.formats.PHONE_NUMBER
        phone_numbers = re.findall(phone_regex, response.text)

        unique_numbers = set(phone_numbers)

        formatted_numbers = []
        for number in unique_numbers:
            formatted_number = "+" + str(number).replace(" ", "").replace(",", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "")
            formatted_numbers.append(formatted_number)

        return "\n".join(formatted_numbers) 

    except:
        return[]

async def cretaion_update(url: str):
    try:
        domain = url.replace("https://", "").replace("http://", "").replace("www.", "")

        w = whois.whois(domain)

        creation_date = w.creation_date
        expiration_date = w.expiration_date
        updated_date = w.updated_date

        return f"Creation date => {creation_date}", f"Update date => {updated_date}", f"Expiration date => {expiration_date}" 

    except:
        return()

async def servers_infos(url: str) -> list:
    try:
        domain = url.replace("https://", "").replace("http://", "").replace("www.", "")

        w = whois.whois(domain)
        names_serv = w.name_servers

        serv = []    
    
        for names in names_serv:
            serv.append(str(names).replace(",", "").replace("[", "").replace("]", "").replace("'", ""))
            
        return "\n".join(serv)

    except:
        return[]
    
async def extract_location(url: str):
    try:
        response = await Requests(url).sender()

        soup = BeautifulSoup(response.text, "html.parser")
        locations = []
        location_elements = soup.find_all('meta', attrs={'name': 'geo.position'})

        for element in location_elements:
            location = element.text.strip()
            locations.append(location)

        return locations
    
    except:
        return()



async def output():
        e = []
        hrefs = []

        max = 25
        href = 0

        url = data["target_url"]
        emails = await extract_emails(url)
        links = await extract_href(url)
        authors = await author_infos(url)
        phones = await extract_phone(url)
        cre_upd = await cretaion_update(url)
        serv = await servers_infos(url)
        loc = await extract_location(url)

        if authors != None:
            print("\n[🟢] 👑 Author(s):")
            print(f"- {authors}")
        else:
            print("[🔴] 👑 Author(s)")

        if cre_upd:
            print("\n[🟢] 📆 Date(s):")
            for cre in cre_upd:
                print(cre)
        else:
            print("\n[🔴] 📆 Date(s)")

        if emails:
            print("\n[🟢] 📫 Email:")
            for email in emails:
                    if email not in e:    
                                print(f"{email}")
                                e.append(email)
        else:
            print("\n[🔴] 📫 Email")

        if phones:
            print("\n[🟢] 📞 Phone(s) numbers:")
            print(phones)
        else:
            print("\n[🔴] 📞 Phone(s) numbers")

        if loc:
            print("\n[🟢] 🏘️ Location:")
            print(loc)
        else:
            print("\n[🔴] 🏘️ Location")

        if serv:
            print("\n[🟢] 🤖 Server(s):")
            print(serv)
        else:
            print("\n[🔴] 🤖 Server(s)")
        

        if links:
            print("\n[🟢] 👀 Href(s):")
            for link in links:
                href += 1
                hrefs.append(link)
            
            if href > max:
                with open("hrefs.txt", "w") as file:
                    for h in hrefs:
                        try:
                            file.write(h + "\n")
                        except:
                            pass

                    print(GREEN+"[+] 😌 All hrefs have been saved in the hrefs.txt file."+WHITE)

            else:
                for h in hrefs:
                    print(h)
        else:
            print("\n[🔴] 👀 Href(s)")

async def main():
    if await checker():
        await output()
    else:
        exit()
