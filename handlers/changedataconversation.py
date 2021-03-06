from telegram import Update, ParseMode
from telegram.ext import MessageHandler, ConversationHandler, CallbackQueryHandler, CallbackContext, Filters

from inlinekeyboards import InlineKeyboard
from buttonsdatadict import BUTTONS_DATA_DICT
from helpers import set_user_data
from layouts import wrap_tags, get_user_info_layout
from DB import update_user_info
from languages import LANGS
from inlinekeyboards.inlinekeyboardvariables import *
from globalvariables import *

NEW_NAME, NEW_SURNAME = ('new_name', 'new_surname')


def change_data_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    callback_query = update.callback_query
    data = callback_query.data

    if data == BUTTONS_DATA_DICT[3]:

        if user[LANG] == LANGS[0]:
            text = "Ismni o'zgartirish"
            reply_text = "Yangi ismningizni yuboring"

        if user[LANG] == LANGS[1]:
            text = "Изменить имя"
            reply_text = "Отправьте свое новое имя"

        if user[LANG] == LANGS[2]:
            text = "Исмни ўзгартириш"
            reply_text = "Янги исмнингизни юборинг"

        state = NEW_NAME

    if data == BUTTONS_DATA_DICT[4]:

        if user[LANG] == LANGS[0]:
            text = "Familyani o'zgartirish"
            reply_text = "Yangi familyangizni yuboring"

        if user[LANG] == LANGS[1]:
            text = "Изменить фамилию"
            reply_text = "Отправьте вашу новую фамилию"

        if user[LANG] == LANGS[2]:
            text = "Фамиляни ўзгартириш"
            reply_text = "Янги фамилянгизни юборинг"

        state = NEW_SURNAME

    reply_text = f'{wrap_tags(reply_text)} :'

    callback_query.edit_message_text(text, parse_mode=ParseMode.HTML)
    callback_query.message.reply_html(reply_text)

    return state


def change_name_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    name = update.message.text

    if name == '/cancel' or name == '/menu' or name == '/start':

        if user[LANG] == LANGS[0]:
            text = "Ismni o'zgartirish bekor qilindi"

        if user[LANG] == LANGS[1]:
            text = 'Смена имени отменена'

        if user[LANG] == LANGS[2]:
            text = "Исмни ўзгартириш бекор қилинди"

        text = f'\U0000274C {text} !'

    else:

        result = update_user_info(user[TG_ID], name=name)

        if result == 'updated':

            user_data['user_data'][NAME] = name

            if user[LANG] == LANGS[0]:
                text = "Ismingiz o'zgartirildi"

            if user[LANG] == LANGS[1]:
                text = "Ваше имя изменено"

            if user[LANG] == LANGS[2]:
                text = "Исмингиз ўзгартирилди"

            text = f'\U00002705 {text} !'

        elif result == 'not updated':

            if user[LANG] == LANGS[0]:
                text = "Ismingiz o'zgartirilmadi"

            if user[LANG] == LANGS[1]:
                text = 'Ваше имя не было изменено'

            if user[LANG] == LANGS[2]:
                text = "Исмингиз ўзгартирилмади"

            text = f'\U000026A0 {text} !'

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard(user_data_keyboard, user[LANG]).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


def change_surname_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    surname = update.message.text

    if surname == '/cancel' or surname == '/menu' or surname == '/start':

        if user[LANG] == LANGS[0]:
            text = "Familyani o'zgartirish bekor qilindi"

        if user[LANG] == LANGS[1]:
            text = "Смена фамилии отменена"

        if user[LANG] == LANGS[2]:
            text = "Фамиляни ўзгартириш бекор қилинди"

        text = f'\U0000274C {text} !'

    else:

        result = update_user_info(user[TG_ID], surname=surname)

        if result == 'updated':

            user_data['user_data'][SURNAME] = surname

            if user[LANG] == LANGS[0]:
                text = "Familyangiz o'zgatrilildi"

            if user[LANG] == LANGS[1]:
                text = "Ваша фамилия изменена"

            if user[LANG] == LANGS[2]:
                text = "Фамилянгиз ўзгатрилилди"

            text = f'\U00002705 {text} !'

        elif result == 'not updated':

            if user[LANG] == LANGS[0]:
                text = "Familyangiz o'zgartirilmadi"

            if user[LANG] == LANGS[1]:
                text = 'Ваше фамилия не было изменено'

            if user[LANG] == LANGS[2]:
                text = "Фамилянгиз ўзгартирилмади"

            text = f'\U000026A0 {text} !'

    update.message.reply_text(text)

    inline_keyboard = InlineKeyboard(user_data_keyboard, user[LANG]).get_keyboard()
    update.message.reply_html(get_user_info_layout(user), reply_markup=inline_keyboard)

    return ConversationHandler.END


changedataconversation_handler = ConversationHandler(

    entry_points=[CallbackQueryHandler(change_data_callback, pattern=r'^change_(\w+)_btn$')],

    states={

        NEW_NAME: [MessageHandler(Filters.text, change_name_callback)],

        NEW_SURNAME: [MessageHandler(Filters.text, change_surname_callback)],

    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ],
    persistent=True,
    name='changedata_conversation'
)
