from . import HeroDoesNotExistError
from .heroes_data import HEROES


class Hero:
    """Hero is able to represent a hero that exists in the game, as
    well as convert to different representations (battle.net slug,
    CSS class)."""

    PUNCTUATION_BLACKLIST = (",", ".", "`", "'")

    def __init__(self, name):
        if name not in HEROES:
            raise HeroDoesNotExistError

        self.name = name

    def css_id(self):
        """Returns the CSS id name for use in the subreddit stylesheet.
        Historically, this has been the name with all punctuation and
        whitespace removed, without changing any capitalization.

        Examples:
            * E.T.C. -> ETC
            * Lt. Morales -> LtMorales
        """

        no_punc = self._name_punc_stripped()
        return ''.join(no_punc.split())

    def battle_net_slug(self):
        """Returns the Battle.net slug for the hero used for the links
        from http://us.battle.net/heroes/en/heroes/#/. As far as we
        have seen, this is the name downcased, punctuation removed, and
        spaces replaced with hyphens.

        Examples:
            * E.T.C. -> etc
            * Lt. Morales -> lt-morales
        """

        no_punc = self._name_punc_stripped()
        return no_punc.replace(" ", "-").lower()

    def _name_punc_stripped(self):
        """Returns the Hero name stripped of all punctuation in the
        blacklist."""

        return ''.join(c for c in self.name if c not in self.PUNCTUATION_BLACKLIST)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
