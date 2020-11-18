from telegram import Update, ParseMode, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler, CallbackContext
from replykeyboards import ReplyKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from DB.main import update_user_info, get_cargo_by_id, update_cargo_status, get_user_cargoes
from languages import LANGS
from helpers import set_user_data
from layouts import get_new_cargo_layout
from inlinekeyboards import InlineKeyboard
from config import GROUP_ID
from inlinekeyboards.inlinekeyboardtypes import inline_keyboard_types
from inlinekeyboards.inlinekeyboardvariables import *
from globalvariables import *
from replykeyboards.replykeyboardvariables import *
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()


def main_inline_keyboard_callback(update: Update, context: CallbackContext):
    # with open('callback_query.json', 'w') as callback_query_file:
    #     callback_query_file.write(callback_query.to_json())
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    callback_query = update.callback_query
    data = callback_query.data

    match_obj = re.search(r'^(\d+_closed)$', data)
    match_obj_2 = re.search(r'^(w_\d+)$', data)

    if match_obj:

        # print(data)
        data = match_obj.string.split('_')
        cargo_id = int(data[0])
        cargo_status = data[-1]
        return_value = update_cargo_status(cargo_id, cargo_status)

        if return_value == 'updated' or return_value == 'not updated':

            user_data['user_cargoes'] = get_user_cargoes(user[ID])
            cargo_data = get_cargo_by_id(cargo_id)

            shipping_datetime = cargo_data['shipping_datetime']
            cargo_data[DATE] = shipping_datetime.strftime('%d-%m-%Y')
            cargo_data[TIME] = shipping_datetime.strftime('%H:%M')
            cargo_data[FROM_LOCATION] = None
            cargo_data[TO_LOCATION] = None
            cargo_data[NAME] = user[NAME]
            cargo_data[SURNAME] = user[SURNAME]
            cargo_data[USERNAME] = user[USERNAME]

            layout = get_new_cargo_layout(cargo_data, user[LANG])
            layout_2 = get_new_cargo_layout(cargo_data, 'cy', hide_user_data=True)

            open_text = inline_keyboard_types[paginate_keyboard][user[LANG]][1]
            button4_text = f'{open_text}'
            button4_data = f'{cargo_id}_opened'

            inline_keyboard = callback_query.message.reply_markup
            inline_keyboard['inline_keyboard'][-1][0] = InlineKeyboardButton(button4_text, callback_data=button4_data)

            callback_query.answer()
            callback_query.edit_message_text(layout, parse_mode=ParseMode.HTML, reply_markup=inline_keyboard)

            if return_value == 'updated':

                if user_data['user_cargoes'][cargo_id]['photo_id']:
                    context.bot.edit_message_caption(GROUP_ID, user_data['user_cargoes'][cargo_id][POST_ID],
                                                     caption=layout_2, parse_mode=ParseMode.HTML)
                else:
                    context.bot.edit_message_text(layout_2, GROUP_ID, user_data['user_cargoes'][cargo_id][POST_ID],
                                                  parse_mode=ParseMode.HTML)

    elif match_obj_2:

        user_data['user_cargoes'] = get_user_cargoes(user[ID])

        wanted = int(match_obj_2.string.split('_')[-1])
        wanted_cargo_data = user_data['user_cargoes'][wanted - 1]

        shipping_datetime = wanted_cargo_data['shipping_datetime']
        wanted_cargo_data[DATE] = shipping_datetime.strftime('%d-%m-%Y')
        wanted_cargo_data[TIME] = shipping_datetime.strftime('%H:%M')
        wanted_cargo_data[NAME] = user[NAME]
        wanted_cargo_data[SURNAME] = user[SURNAME]
        wanted_cargo_data[USERNAME] = user[USERNAME]

        layout = get_new_cargo_layout(wanted_cargo_data, user[LANG])
        inline_keyboard = InlineKeyboard(paginate_keyboard, user[LANG],
                                         data=(wanted, user_data['user_cargoes'])).get_keyboard()
        callback_query.answer()
        callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    elif data == BUTTONS_DATA_DICT[7] or data == BUTTONS_DATA_DICT[8] or data == BUTTONS_DATA_DICT[9]:

        if data == BUTTONS_DATA_DICT[7]:
            lang = LANGS[0]
            text = "Til: O'zbekcha"
            reply_text = "Til o'zgartirildi"
            edited_text = '\U0001F1FA\U0001F1FF'

        elif data == BUTTONS_DATA_DICT[8]:
            lang = LANGS[1]
            text = "Язык: русский"
            reply_text = 'Язык был изменен'
            edited_text = '\U0001F1F7\U0001F1FA'

        elif data == BUTTONS_DATA_DICT[9]:
            lang = LANGS[2]
            text = "Тил: Ўзбекча"
            reply_text = "Тил ўзгартирилди"
            edited_text = '\U0001F1FA\U0001F1FF'

        context.bot.answer_callback_query(callback_query.id, reply_text)

        update_user_info(user[TG_ID], lang=lang)
        user_data['user_data'][LANG] = lang

        reply_keyboard = ReplyKeyboard(menu_keyboard, lang).get_keyboard()
        callback_query.edit_message_text(edited_text)
        callback_query.message.reply_text(text, reply_markup=reply_keyboard)

    else:
        callback_query.answer()


inline_keyboard_handler = CallbackQueryHandler(main_inline_keyboard_callback)
