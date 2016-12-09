import os.path

from bs4 import BeautifulSoup
import requests

# Location of file to store latest known page number
LAST_KNOWN_PAGE_FILE = "/tmp/rotation_checker_latest"
# URL of forum thread where latest rotations are posted
ROTATION_FORUM_THREAD = "https://us.battle.net/forums/en/heroes/topic/17936383460"

def write_last_known_page(page_num):
    with open(LAST_KNOWN_PAGE_FILE, "w") as f:
        f.write(str(page_num))

def read_last_known_page():
    try:
        with open(LAST_KNOWN_PAGE_FILE, "r") as f:
            return int(f.read())
    except OSError:
        return 0

def is_404(html):
    return "Page Not Found" in html

def load_page(page_num):
    return requests.get(
            ROTATION_FORUM_THREAD,
            params={"page": page_num}
            )

def load_latest_page(last_known_page=0):
    if is_404(load_page(last_known_page+1).text):
        return load_page(last_known_page)
    else:
        return load_latest_page(last_known_page+1)

def remove_slot_text(s):
    if "Slot unlocked at" in s:
        return s

    return s.split(" (Slot unlocked at")[0]

def rotation_info_from_source(html):
    soup = BeautifulSoup(html, 'html.parser')
    latest_post_content = soup.select(".TopicPost-bodyContent")[-1]

    header = latest_post_content.span.text
    date = header.split("Rotation: ")[-1]
    heroes = [remove_slot_text(li.text) for li in latest_post_content.find_all("li")]

    return date, heroes

if __name__ == "__main__":
    # read last known page number if we have it
    last_known = read_last_known_page()

    # load latest page, starting from last known page number
    resp = load_latest_page(last_known)

    # extract date and hero rotation
    date, heroes = rotation_info_from_source(resp.text)

    # write latest page number for future
    page_num = int(resp.url.split("=")[-1])
    write_last_known_page(page_num)

    print(date)
    print(heroes)
