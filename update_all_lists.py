from listscraper.instance_class import ScrapeInstance
import subprocess

# List of Letterboxd URLs and their matching CSV names
lists = {
    "https://letterboxd.com/couchpotato00/watchlist/": "watchlist",
    "https://letterboxd.com/couchpotato00/list/favorites/": "favorites",
    "https://letterboxd.com/couchpotato00/list/movies-everyone-should-watch-at-least-once/": "letterboxd_everyone_should_watch"
}

# Scrape each list into its matching CSV
for url, output_name in lists.items():
    print(f"\nScraping {output_name}...")
    ScrapeInstance(
        inputURLs=[url],
        pages="*",
        output_name=output_name,
        output_path=".",                 # Save in root
        output_file_extension=".csv",
        infile=None,
        concat=False,
        quiet=True,
        threads=4
    )

# Now run your existing converters to generate the .jsons
print("\nRunning TMDB conversion scripts...")
subprocess.run(["python", "WatchListAndLikes.py"])
subprocess.run(["python", "Lists.py"])
