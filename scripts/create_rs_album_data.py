import glob
import re
from urllib.request import urlopen
import unicodedata

from bs4 import BeautifulSoup
import pandas as pd
import regex

def replace_unicode(text):
    """Replace pesky unicode identifiers."""
    unicode_dict = {
       r"\u201d": "\"",
       r"\u201c": "\"",
       r"\u2019": "'",
       r"\ufeff": "",
    }
    unicode_strings = re.findall(r"\\u[0-9a-z]{4}", text, flags=re.UNICODE)
    for u_string in unicode_strings:
        if u_string in unicode_dict.keys():
            text = text.replace(u_string, unicode_dict[u_string])
        else:
            # https://stackoverflow.com/questions/48006240/how-to-convert-unicode-string-into-normal-text-in-python
            u_char = u_string.encode("utf-8").decode("unicode-escape")
            text = text.replace(u_string, u_char)
    return text


def parse_album_entry(entry):
    position = int(re.search("positionDisplay\":(\d+)", entry).groups()[0])
    artist, album = re.search(
        "title\":\"(.*), '(.*)'\",\"subtitle",
        entry
    ).groups()
    if r"\u" in artist: artist = replace_unicode(artist)
    if r"\u" in album: album = replace_unicode(album)
    year = int(re.search("(\d+)\",\"slug", entry).groups()[0])

    this_album_dict = dict()
    this_album_dict["artist"] = artist.title()
    this_album_dict["name"] = album.title()
    this_album_dict["date"] = year
    return position, this_album_dict

if __name__  == "__main__":
    all_pages = glob.glob("pages/rs_top_500/*.html")
    all_albums_dict = dict()
    for i, page in enumerate(all_pages):
        with open(page, "r", encoding='utf-8-sig') as f:
            soup = BeautifulSoup(f, "html.parser")

        albums_string = soup.find_all("script", id="pmc-lists-front-js-extra")
        albums_string = albums_string[0].string
        pattern_to_search = "(\{\"ID\".*?\"enableAppleGA\":true\})"
        album_entries = re.findall(pattern_to_search, albums_string)
        for entry in album_entries:
            pos, this_album_dict = parse_album_entry(entry)
            all_albums_dict[pos] = this_album_dict

    df = pd.DataFrame.from_dict(all_albums_dict, orient="index")
    df.index.name = "position"
    df = df.sort_index()
    print(df.head())
    df.head(500).to_csv("data/rs_top_500_albums.tsv", sep="\t", index=True)
