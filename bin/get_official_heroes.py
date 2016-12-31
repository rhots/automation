import sys

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

"""
The official heroes listing on battle.net is populated by a list of
Objects defined in JS (window.heroes). This script fetches the full
list and outputs a list of tuples relating official hero names to the
battle.net slugs.

To run this script, you should install phantomjs in addition to the
import dependencies.
"""

def get_heroes_data():
    # We prefer the PhantomJS driver to avoid opening any GUI windows.
    browser = webdriver.PhantomJS()
    browser.get("http://us.battle.net/heroes/en/heroes/#/")
    heroes = browser.execute_script("return window.heroes;")
    browser.quit()

    return heroes

def main():
    heroes = get_heroes_data()
    heroes = [(h['name'], h['slug']) for h in heroes]
    print(heroes)

if __name__ == "__main__":
    main()
