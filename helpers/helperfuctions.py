from DB import get_user


def set_user_data(user_id, user_data):
    value = user_data.setdefault('user_data', None)

    if not value:
        value = get_user(user_id)
        user_data['user_data'] = value


def wrap_tags(*args):
    symbol = ''

    if len(args) > 1:
        symbol = ' '

    return f'<b><i><u>{symbol.join(args)}</u></i></b>'


def format_phone_number(phone_number):
    country_code = phone_number[:4]
    operator_code = phone_number[4:][:2]
    phone_number = phone_number[4:][2:]

    # return value like +998 (99) 855 - 9819

    return f'{country_code} ({operator_code}) {phone_number[:3]} - {phone_number[3:]}'
