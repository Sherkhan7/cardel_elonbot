from DB import get_region_and_district
from helpers import wrap_tags
from units import UNITS
from layouts.layoutdicts import *


def get_new_cargo_layout(cargo_data, lang, hide_user_data=None):
    from_point = get_region_and_district(cargo_data[FROM_REGION], cargo_data[FROM_DISTRICT])
    from_district_name = from_point[1][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]
    from_region_name = from_point[0][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]

    to_point = get_region_and_district(cargo_data[TO_REGION], cargo_data[TO_DISTRICT])
    to_district_name = to_point[1][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]
    to_region_name = to_point[0][NEW_CARGO_LAYOUT_DICT[lang][REGION_NAME]]

    date = cargo_data[DATE]
    time = cargo_data[TIME]
    user_name = cargo_data[NAME]
    user_surname = cargo_data[SURNAME]
    user_phone_number = cargo_data[USER_PHONE_NUMBER]

    weight = volume = definition = user_username = NEW_CARGO_LAYOUT_DICT[lang][UNDEFINED_TEXT]

    if cargo_data[WEIGHT]:
        weight = f'{cargo_data[WEIGHT]} {UNITS[lang][cargo_data[WEIGHT_UNIT]]}'

    if cargo_data[VOLUME]:
        volume = f'{cargo_data[VOLUME]} {UNITS[lang][cargo_data[VOLUME_UNIT]]}'

    if cargo_data[DEFINITION]:
        definition = cargo_data[DEFINITION]

    if cargo_data[USERNAME]:
        user_username = f'@{cargo_data[USERNAME]}'

    if cargo_data[STATE] == 'opened':
        status = NEW_CARGO_LAYOUT_DICT[lang][OPENED_STATUS]
        emoji = '\U0001F7E2'

    elif cargo_data[STATE] == 'closed':
        status = NEW_CARGO_LAYOUT_DICT[lang][CLOSED_STATUS]
        emoji = '\U0001F534'

    else:
        status = NEW_CARGO_LAYOUT_DICT[lang][NOT_CONFIRMED_STATUS]
        emoji = '\U0001F7E1'

    if cargo_data[TIME] == 'now':
        time = NEW_CARGO_LAYOUT_DICT[lang][TIME]

    layout = [
        f'\U0001F4CD  {NEW_CARGO_LAYOUT_DICT[lang][FROM_TEXT]}: {wrap_tags(from_district_name, from_region_name)}',
        f'\U0001F3C1  {NEW_CARGO_LAYOUT_DICT[lang][TO_TEXT]}: {wrap_tags(to_district_name, to_region_name)}\n',
        f'\U0001F4E6  {NEW_CARGO_LAYOUT_DICT[lang][WEIGHT_TEXT]}: {wrap_tags(weight)}',
        f'\U0001F4E6  {NEW_CARGO_LAYOUT_DICT[lang][VOLUME_TEXT]}: {wrap_tags(volume)}',
        f'\U0001F5D2  {NEW_CARGO_LAYOUT_DICT[lang][DEFINITION_TEXT]}: {wrap_tags(definition)}',
        f'\U0001F4C6  {NEW_CARGO_LAYOUT_DICT[lang][DATE_TEXT]}: {wrap_tags(date)}',
        f'\U0001F553  {NEW_CARGO_LAYOUT_DICT[lang][TIME_TEXT]}: {wrap_tags(time)}\n',
        f'\U0001F464  {NEW_CARGO_LAYOUT_DICT[lang][USER_TEXT]}: {wrap_tags(user_name, user_surname)}',
        f'\U0001F4DE  {NEW_CARGO_LAYOUT_DICT[lang][USER_PHONE_NUMBER_TEXT]}: {wrap_tags(user_phone_number)}',
        f'\U0001F170  {NEW_CARGO_LAYOUT_DICT[lang][TG_ACCOUNT_TEXT]}: {wrap_tags(user_username)}\n',
        f'{emoji}  {NEW_CARGO_LAYOUT_DICT[lang][STATUS_TEXT]}: {wrap_tags(status)}\n',
        f'\U0001F916  @cardel_elonbot \U000000A9',
        f'\U0001F6E1  cardel online \U00002122',
    ]

    if hide_user_data:
        layout.pop(7)
        layout.pop(7)
        layout.pop(7)

    if ID in cargo_data:
        layout.append(f'\n\U0001F194 {str(cargo_data[ID]).zfill(4)}')

    layout = '\n'.join(layout)

    return layout


def get_user_info_layout(user):
    layout = f"{USER_INFO_LAYOUT_DICT[user['lang']][NAME]}: {wrap_tags(user['name'])}\n\n" \
             f"{USER_INFO_LAYOUT_DICT[user['lang']][SURNAME]}: {wrap_tags(user['surname'])}"
    # f"<b><i>{'-'.ljust(30, '-')}</i></b> \n" \
    # f"<b>\u0000260e {phone}: <i><u>{format_phone_number(user['phone_number'])}</u></i></b>" \
    # f"<b><i>\u0000260e {phone_2}: </i><u>{user['phone_number2']}</u></b> \n"

    return layout


def get_phone_number_layout(lang):
    return f"{PHONE_NUMBER_LAYOUT_DICT[lang][1]}:\n\n" \
           f"{PHONE_NUMBER_LAYOUT_DICT[lang][2]}: {wrap_tags('99 1234567')}\n" \
           f"{PHONE_NUMBER_LAYOUT_DICT[lang][3]}\n" \
           f"{PHONE_NUMBER_LAYOUT_DICT[lang][2]}: {wrap_tags('+998 99 1234567')}\n"
