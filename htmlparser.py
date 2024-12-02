from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

url = "https://oklahomacity.craigslist.org/search/vga#search=1~gallery~0~0"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

child_soup = soup.find_all('li', class_='cl-static-search-result')  

titles = []
for i in child_soup:
    title_tag = i.find('div', class_='title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        titles.append(title)
        print(title)  

choice = input("Save in a text file? Enter y or n: ")
if choice == "y":
    with open("output.txt", "w") as file:
        for title in titles:
            file.write(title + '\n')

choice = input("To see price and location details, enter an exact string from the list. Enter n to exit: ")

if choice != 'n':
    found = False
    for i in child_soup:
        title_tag = i.find('div', class_='title')
        price_tag = i.find('div', class_='price')
        location_tag = i.find('div', class_='location')

        if title_tag:
            title = title_tag.get_text(strip=True)
        
        if price_tag:
            price = price_tag.get_text(strip=True)
        else:
            price = "Price Not Listed"
        
        if location_tag:
            location = location_tag.get_text(strip=True)
        else:
            location = "Location Not Listed"
        
        if choice.lower() in title.lower():  
            found = True
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Location: {location}")
            print('-' * 50)

    if not found:
        print("No matching listing found.")