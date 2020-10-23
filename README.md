# Top 500 Albums - RateYourMusic vs. RollingStone

RollingStone recently released their new "500 Greatest Albums of All Time List" - the first update to this list in over 15 years. I played around with the original dataset a while back so I figured it would be fun to try out the new list.

As a comparison, I looked at the top 500 albums on the popular site RateYourMusic.com. The top 500 albums, rather than being voted on directly, are the result of their ranking algorithm. Note that these charts change every week - so to be clear I downloaded the webpages I used to run analyses on October 15th, 2020.

I used a lot of packages to download and process this data. HTML parsing was done through `BeautifulSoup` and brute force regex. Manipulation of data was done through `numpy` & `pandas`. For plotting I used `matplotlib`, `seaborn`, and `PIL` to incorporate the album covers as images in the plots.

To compare the entries in the RollingStone list to those in the RYM list, I used the in-built `difflib` module in Python. I've never used this module before so hopefully I used it in the way it was intended. There is always the possibility that I made a mistake in comparing albums - there was a good amount of cleaning necessary and it is likely that I missed a shared album or counted one that I shouldn't have. Feel free to open an issue if you see something awry.

Also feel free to download the processed data in the `data/` folder. I included the primary genres, number of ratings, number of reviews, and average score of the RYM albums if you want to play around with those.

[RollingStone's list](https://www.rollingstone.com/music/music-lists/best-albums-of-all-time-1062063/)

[RYM's charts](https://rateyourmusic.com/charts/top/album/all-time)
