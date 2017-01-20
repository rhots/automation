from bs4 import BeautifulSoup
import requests

from .hero import Hero


class Rotation:
    """Rotation is able to get the latest free hero rotation."""

    FORUM_URL = "https://us.battle.net/heroes/en/forum/topic/17936383460"
    # TODO: omg get this outta here
    SECOND_SPRITESHEET_HEROES = ["Samuro", "Ragnaros", "Varian"]

    def __init__(self):
        pass

    def get_rotation(self):
        html = requests.get(self.FORUM_URL).text
        soup = BeautifulSoup(html, "html.parser")
        post = soup.select("div.TopicPost-bodyContent")[0]
        header = post.span.text

        date = header.split("Rotation: ")[-1]

        heroes = [self._remove_slot_text(li.text) for li in post.find_all("li")]
        heroes = [Hero(name) for name in heroes]

        return date, heroes

    # TODO: omg get this outta here
    def sidebar_text(self):
        """We want the sidebar text to be formatted like the following:
            * spacer
            * 3 heroes
            * spacer
            * 4 heroes
            * spacer
            * 3 heroes
            * spacer
            * bottom
        """

        _, heroes = self.get_rotation()
        formatted_heroes = [self._format_hero(h) for h in heroes]

        spacer = "[](#spacer)"
        bottom = "[](#bottom)"

        # This could be more concise using inserts, but this seems to
        # be the clearest method for future readers.
        final_line_items = [spacer]
        final_line_items += formatted_heroes[:3]
        final_line_items += [spacer]
        final_line_items += formatted_heroes[3:7]
        final_line_items += [spacer]
        final_line_items += formatted_heroes[7:10]
        final_line_items += [spacer]
        final_line_items += [bottom]

        return "\n".join(final_line_items)

    def _format_hero(self, hero):
        """_format_hero formats a hero's name into a line item in
        the sidebar's free rotation."""

        bnet_slug = hero.battle_net_slug()
        css_id = hero.css_id()

        # Reddit's stylesheet images have a limited size, so we have
        # more than one spritesheet providing the rotation icons.
        sheet_suffix = "2" if self._needs_second_sheet(hero) else ""

        format_str = "[](http://us.battle.net/heroes/en/heroes/{0}/#free_rotation{1}#{2})"
        return format_str.format(
                bnet_slug,
                sheet_suffix,
                css_id)

    def _remove_slot_text(self, s):
        if "Slot unlocked at" not in s:
            return s

        return s.split(" (Slot unlocked at")[0]

    # TODO: omg get this outta here
    def _needs_second_sheet(self, hero):
        return hero.name in self.SECOND_SPRITESHEET_HEROES
