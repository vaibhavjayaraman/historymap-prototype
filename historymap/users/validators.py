"""This file contains password validator classes to be used for Django Account Signup."""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class SpecialCharacterValidator(object):
    def __init__(self, characters = "[()[\]{}|~!@#$%^&;*_\-+=;:,<>./?]", min_num = 1):
        self.min_num = min_num
        self.characters = characters

    def validate(self, password, user=None):
        if not len(re.findall(self.characters, password)) >= self.min_num:
            raise ValidationError(
                    _("The password must contain at least %(min_num)d special characters %(characters)s.") % {"min_num": self.min_num, "characters": self.characters}, 
            )
            
    def get_help_text(self):
        return _("The password must contain at least %(min_num)d special character %(characters)s.") % {"min_num": self.min_num, "characters" : self.characters}
    
class NumberValidator(object):
    def __init__(self, min_num = 1):
        self.min_num = min_num

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_num:
            raise ValidationError(
                    _("The password must contain at least %(min_num)d digit(s) [0 - 9].") %
                    {"min_num": self.min_num,}
            )

    def get_help_text(self):
        return _("The password must contain at least %(min_num)d digit(s) [0-9].") % {"min_num": self.min_num}
    
class UpperCaseValidator(object):
    def __init__(self, min_num = 1):
        self.min_num = min_num

    def validate(self, password, user=None):
        if not len(re.findall('[A-Z]', password)) >= self.min_num:
            raise ValidationError(
                    _("The password must contain at least %(min_num)d uppercase word(s) [A - Z].")  %
                    {"min_num": self.min_num}
            )

    def get_help_text(self):
        return _("The password must contain at least %(min_num)d uppercase word(s) [A-Z].") % {"min_num": self.min_num}

class LowerCaseValidator(object):
    def __init__(self, min_num = 1):
        self.min_num = min_num

    def validate(self, password, user=None):
        if not len(re.findall('[a-z]', password)) >= self.min_num:
            raise ValidationError(
                    _("The password must contain at least %(min_num)d lowercase word(s) [a - z].")  %
                    {"min_num": self.min_num}
            )

    def get_help_text(self):
        return _("The password must contain at least %(min_num)d lowercase word(s) [a-z].") % {"min_num": self.min_num}
