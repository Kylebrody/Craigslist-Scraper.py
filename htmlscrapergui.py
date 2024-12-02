import tkinter as tk
from tkinter import scrolledtext
from bs4 import BeautifulSoup
from urllib.request import urlopen
import webbrowser

child_soup = []
titles = []

def scrape_data():
    global child_soup, titles
    url = "https://oklahomacity.craigslist.org/search/vga#search=1~gallery~0~0"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    child_soup = soup.find_all('li', class_='cl-static-search-result')

    titles = []
    output_field.delete('1.0', tk.END)  

    for i in child_soup:
        title_tag = i.find('div', class_='title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            titles.append(title)
            output_field.insert(tk.END, title + '\n')

def open_link(event):
    webbrowser.open(event.widget.cget("text"))

def show_details():
    choice = detail_entry.get().strip()
    if choice:
        detail_field.delete('1.0', tk.END)  
        found = False
        for i in child_soup:
            title_tag = i.find('div', class_='title')
            price_tag = i.find('div', class_='price')
            location_tag = i.find('div', class_='location')
            link_tag = i.find('a', href=True)  

            if title_tag:
                title = title_tag.get_text(strip=True)
            
            price = price_tag.get_text(strip=True) if price_tag else "Price Not Listed"
            location = location_tag.get_text(strip=True) if location_tag else "Location Not Listed"
            link = link_tag['href'] if link_tag and link_tag['href'].startswith('http') else f"https://oklahomacity.craigslist.org{link_tag['href']}" if link_tag else "No Link Available"

            if choice.lower() in title.lower(): 
                found = True
                detail_field.insert(tk.END, f"Title: {title}\n")
                detail_field.insert(tk.END, f"Price: {price}\n")
                detail_field.insert(tk.END, f"Location: {location}\n")
                link_label = tk.Label(detail_field, text=link, fg="blue", cursor="hand2")
                detail_field.window_create(tk.END, window=link_label)
                link_label.bind("<Button-1>", open_link)
                detail_field.insert(tk.END, '\n' + '-' * 50 + '\n')

        if not found:
            detail_field.insert(tk.END, "No matching listing found.\n")
    else:
        detail_field.insert(tk.END, "Please enter a valid string.\n")

def save_to_file():
    if titles:
        with open("output.txt", "w") as file:
            for title in titles:
                file.write(title + '\n')
        output_field.insert(tk.END, "\nSaved to output.txt\n")
    else:
        output_field.insert(tk.END, "\nNo data to save!\n")

root = tk.Tk()
root.title("Craigslist Scraper")

scrape_button = tk.Button(root, text="Start Scrape", command=scrape_data)
scrape_button.pack(pady=5)

output_field = scrolledtext.ScrolledText(root, width=80, height=15)
output_field.pack(pady=5)

save_button = tk.Button(root, text="Save to File", command=save_to_file)
save_button.pack(pady=5)

detail_label = tk.Label(root, text="Search the list for details and a link:")
detail_label.pack(pady=5)
detail_entry = tk.Entry(root, width=50)
detail_entry.pack(pady=5)

detail_button = tk.Button(root, text="Find Details", command=show_details)
detail_button.pack(pady=5)

detail_field = scrolledtext.ScrolledText(root, width=80, height=10)
detail_field.pack(pady=5)

root.mainloop()