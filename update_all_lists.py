import subprocess

commands = [
    ["python", "listscraper/__main__.py", "https://letterboxd.com/couchpotato00/watchlist/", "-on", "watchlist", "-op", ".", "-ofe", "csv", "--quiet"],
    ["python", "listscraper/__main__.py", "https://letterboxd.com/couchpotato00/list/favorites/", "-on", "favorites", "-op", ".", "-ofe", "csv", "--quiet"],
    ["python", "listscraper/__main__.py", "https://letterboxd.com/couchpotato00/list/movies-everyone-should-watch-at-least-once/", "-on", "letterboxd_everyone_should_watch", "-op", ".", "-ofe", "csv", "--quiet"]
]

for cmd in commands:
    subprocess.run(cmd)

print("\nScraping complete. Now converting CSVs to JSON...")
subprocess.run(["python", "ConvertToJson.py"])
import subprocess

commands = [
    ["python", "listscraper/scraper.py", "https://letterboxd.com/couchpotato00/watchlist/", "-on", "watchlist", "-op", ".", "-ofe", "csv", "--quiet"],
    ["python", "listscraper/scraper.py", "https://letterboxd.com/couchpotato00/list/favorites/", "-on", "favorites", "-op", ".", "-ofe", "csv", "--quiet"],
    ["python", "listscraper/scraper.py", "https://letterboxd.com/couchpotato00/list/movies-everyone-should-watch-at-least-once/", "-on", "letterboxd_everyone_should_watch", "-op", ".", "-ofe", "csv", "--quiet"]
]

for cmd in commands:
    subprocess.run(cmd)

print("\nScraping complete. Now converting CSVs to JSON...")
subprocess.run(["python", "ConvertToJson.py"])
