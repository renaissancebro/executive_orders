import requests
from bs4 import BeautifulSoup
# First call to fetch the latest Executive Order from the White House website


def fetch_latest():
    # Simulated data for testing purposes
    #  return {
    #     "title": "Simuled Executive Order for Testing",
    #     "date": "June 16, 2025",
    #     "url": "https://example.com/fake-eo"
    # }
#Full logic

    url = "https://www.whitehouse.gov/presidential-actions/executive-orders/"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Grab the first Executive Order entry
    article = soup.select_one(
        "ul > li.wp-block-post.category-executive-orders"
    )
    if not article:
        with open("debug.html", "w") as f:
            f.write(soup.prettify())
        raise Exception("❌ No matching article found.")

    title_el = article.select_one("h2 a")
    date_el = article.select_one("time")

    if not title_el or not date_el:
        raise Exception("❌ Missing title or date element.")

    return {
        "title": title_el.text.strip(),
        "date": date_el.text.strip(),
        "url": title_el["href"]
    }

def grab_meta_data():
    return fetch_latest()
