from django.core import validators, exceptions


def validate_email(email):
    try:
        validators.validate_email(email)
    except exceptions.ValidationError:
        return False
    return True


def validate_username(username):
    if username == 'me':
        return False
    return True
