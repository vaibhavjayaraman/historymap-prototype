"""This file contains password validator classes to be used for Django Account Signup."""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class SpecialCharacterValidator(object):
    """Ensures that min_number of characters is used in password."""
    def __init__(self, characters = "+!@#$%^&*()?/\[]{}:;,<>", min_num = 1):
        self.min_num = min_num
        self.characters = characters

    def validate(self, password, user=None):
        if not len(re.findall(self.characters, password)) >= self.min_num:
            raise ValidationError(
                    _("The password must contain at least %(min_num) special characters %(characters)."), 
                    params = {"min_num": self.min_num, 
                              "characters": self.characters}, 
            )

    def get_help_text(self):
        return _("The password must contain at least %(min_num) special characters %(characters).") % {"min_num": self.min_num, "characters": self.characters}

class NumberValidator(object):
    """Ensures that min_number of digits is used in password."""
    def __init__(self, min_num = 1):
        self.min_num = min_num

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_num:
            raise ValidationError(
                    _("The password must contain at least %(min_num) digits [0 - 9]."), 
                    params = {"min_num": self.min_num,}
            )

    def get_help_text(self):
        return _("The password must contain at least %(min_num) digits [0-9].") % {"min_num": self.min_num}

class UpperCaseValidator(object):
    """Ensures that min_number of uppercase letters is used in password."""
    def __init__(self, min_num = 1):
        self.min_num = min_num

    def validate(self, password, user=None):
        if not len(re.findall('[A=Z]', password)) >= self.min_num:
            raise ValidationError(
                    _("The password must contain at least %(min_num) uppercase words [A - Z]."), 
                    params = {"min_num": self.min_num}
            )

    def get_help_text(self):
        return _("The password must contain at least %(min_num) uppercase words [A-Z].") % {"min_num": self.min_num}
