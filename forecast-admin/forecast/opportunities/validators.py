from django.core.exceptions import ValidationError
import re


# Enforce NAICS code as 5 digits
def validate_NAICS(naics):
    if re.match(r"\d{5}", naics) == None:
        raise ValidationError('NAICS code must be 5 digits long')
    return True


# Enforce dollar amounts
def validate_dollars(amount):
    pass
