import json
import os
import requests
from bs4 import BeautifulSoup

def fetch_contributions():
    # The URL fragment the profile page uses
    username = "gutantah"
    url = f"https://github.com/users/{username}/contributions"
    
    print(f"Fetching data from {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    days = []
    # Parse the day cells from the HTML
    for cell in soup.find_all("td", class_="ContributionCalendar-day"):
        date = cell.get("data-date")
        level = cell.get("data-level", "0")
        if date:
            days.append({"date": date, "level": int(level)})
            
    data = {"days": days}
    
    # Write to data/contributions.json
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(data, f)
        
    print("Success! Data written to data/contributions.json")

if __name__ == "__main__":
    fetch_contributions()