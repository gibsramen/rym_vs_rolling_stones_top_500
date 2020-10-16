import glob
import re

from bs4 import BeautifulSoup as bs
import pandas as pd


def parse_stats(text):
    """Extracts stats from BeautifulSoup output."""
    matches = re.search("([\d\.]+)\D+([\d,]+)\D+([\d,]+)", text).groups()
    convert_to_numeric = lambda x: float(x.replace(",", ""))
    rating, num_ratings, num_reviews = map(convert_to_numeric, matches)
    return rating, num_ratings, num_reviews


def extract_albums_from_html(soup, start_pos=0):
    """Get all album information from html.

    Parameters:

        soup (BeautifulSoup): BeatifulSoup of RYM page
        start_pos (int): offset for storing position

    Returns:

        album_dict (dict): dictionary containing the following information

            - position
            - RYM album id
            - artist
            - name
            - release date
            - primary genres
            - average rating
            - number of ratings
            - number of reviews
    """
    chart_entries = soup.select("td div:is(.chart_main, .chart_stats)")

    # this selection allows both album info and stats to be extracted at once
    # even numbered entries are album info and odd numbered entries are stats
    album_entries = chart_entries[::2]
    stats_entries = chart_entries[1::2]
    z = zip(album_entries, stats_entries)

    album_dict = dict()
    for i, (album_entry, stats_entry) in enumerate(z, start=1):
        position = i + start_pos
        album_id = album_entry.find("a", class_="album")["title"]
        album_artist = album_entry.find("a", class_="artist").text
        album_name = album_entry.find("a", class_="album").text
        album_date = album_entry.find("div", class_="chart_year").text.strip()
        album_genres = [x.text for x in album_entry.find_all("a", class_="genre")]
        
        this_album_dict = dict()
        this_album_dict["album_id"] = album_id
        this_album_dict["artist"] = album_artist
        this_album_dict["name"] = album_name
        this_album_dict["date"] = album_date
        this_album_dict["genres"] = album_genres

        stats_text = stats_entry.select_one("a").text
        rating, num_ratings, num_reviews = parse_stats(stats_text)

        this_album_dict["rating"] = rating
        this_album_dict["num_ratings"] = num_ratings
        this_album_dict["num_reviews"] = num_reviews

        album_dict[position] = this_album_dict

    return album_dict


if __name__ == "__main__":
    all_pages = glob.glob("pages/*.html")
    all_albums_dict = dict()
    for i, page in enumerate(all_pages):
        with open(page, "r") as f:
            soup = bs(f, "html.parser")
        all_albums_dict.update(extract_albums_from_html(soup, 40*i))

    df = pd.DataFrame.from_dict(all_albums_dict, orient="index")
    df.index.name = "position"
    print(df.head())
    df.head(500).to_csv("data/rym_top_500_albums.tsv", sep="\t", index=True)
