from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, ParseMode
from DB import *
from inlinekeyboards import InlineKeyboard
from layouts import get_new_cargo_layout
from languages import LANGS
from globalvariables import *
from inlinekeyboards.inlinekeyboardvariables import *


def edit_date_and_time_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_data = context.user_data
    user = user_data['user_data']

    if data == 'back' or data == 'now':
        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()
        answer = None

        if data == 'now':
            user_data[USER_INPUT_DATA][DATE] = datetime.datetime.now().strftime('%d-%m-%Y')
            user_data[USER_INPUT_DATA][TIME] = 'now'

            if user[LANG] == LANGS[0]:
                answer = "Kun va vaqt tahrirlandi"

            if user[LANG] == LANGS[1]:
                answer = "Дата и время изменены"

            if user[LANG] == LANGS[2]:
                answer = "Кун ва вақт таҳрирланди"

            answer = '\U0001F44F\U0001F44F\U0001F44F ' + answer

        layout = get_new_cargo_layout(user_data[USER_INPUT_DATA], user[LANG])

        state = 'edit'

    if data == 'today' or data == 'tomorrow' or data == 'after_tomorrow':

        if data == 'today':
            user_data[USER_INPUT_DATA]['new_date'] = datetime.datetime.now().strftime('%d-%m-%Y')

        if data == 'tomorrow':
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            user_data[USER_INPUT_DATA]['new_date'] = tomorrow.strftime('%d-%m-%Y')

        if data == 'after_tomorrow':
            after_tomorrow = datetime.datetime.now() + datetime.timedelta(days=2)
            user_data[USER_INPUT_DATA]['new_date'] = after_tomorrow.strftime('%d-%m-%Y')

        if user[LANG] == LANGS[0]:
            text = "Soatni belgilang"
            button_text = 'Ortga'

        if user[LANG] == LANGS[1]:
            text = "Выберите время"
            button_text = "Назад"

        if user[LANG] == LANGS[2]:
            text = "Соатни белгиланг"
            button_text = "Ортга"

        text = f'{text} :'
        button_text = '« ' + button_text

        inline_keyboard = InlineKeyboard(hours_keyboard, user[LANG], begin=6, end=17).get_keyboard()
        inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back')])

        layout = text
        answer = None
        state = 'edit_hour'

    callback_query.answer(answer)

    if user_data[USER_INPUT_DATA][PHOTO]:
        callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)
    else:
        callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    user_data[USER_INPUT_DATA][STATE] = state
    return state


def edit_hour_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    data = callback_query.data

    user_data = context.user_data
    user = user_data['user_data']

    if data == 'back_btn' or data == 'next_btn' or data == 'back':

        if user[LANG] == LANGS[0]:
            button_text = "Ortga"

        if user[LANG] == LANGS[1]:
            button_text = "Назад"

        if user[LANG] == LANGS[2]:
            button_text = "Ортга"

        button_text = f'« {button_text}'

        if data == 'back':
            user_data[USER_INPUT_DATA].pop('new_date')

            inline_keyboard = InlineKeyboard(dates_keyboard, user[LANG]).get_keyboard()
            inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back')])

            state = 'edit_date_and_time'

        if data == 'next_btn' or data == 'back_btn':

            if data == 'next_btn':
                inline_keyboard = InlineKeyboard(hours_keyboard, user[LANG], begin=18, end=29).get_keyboard()

            if data == 'back_btn':
                inline_keyboard = InlineKeyboard(hours_keyboard, user[LANG], begin=6, end=17).get_keyboard()
                inline_keyboard['inline_keyboard'].append([InlineKeyboardButton(button_text, callback_data='back')])

            state = user_data[USER_INPUT_DATA][STATE]

        callback_query.answer()
        callback_query.edit_message_reply_markup(inline_keyboard)

        user_data[USER_INPUT_DATA][STATE] = state
        return state

    else:

        if user[LANG] == LANGS[0]:
            answer = "Kun va vaqt tahrirlandi"

        if user[LANG] == LANGS[1]:
            answer = "Дата и время изменены"

        if user[LANG] == LANGS[2]:
            answer = "Кун ва вақт таҳрирланди"

        answer = f'\U0001F44F\U0001F44F\U0001F44F {answer}'
        callback_query.answer(answer)

        user_data[USER_INPUT_DATA][TIME] = data
        user_data[USER_INPUT_DATA][DATE] = user_data[USER_INPUT_DATA].pop('new_date')

        layout = get_new_cargo_layout(user_data[USER_INPUT_DATA], user[LANG])
        inline_keyboard = InlineKeyboard(edit_keyboard, user[LANG]).get_keyboard()

        if user_data[USER_INPUT_DATA][PHOTO]:
            callback_query.edit_message_caption(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        else:
            callback_query.edit_message_text(layout, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

        state = 'edit'
        user_data[USER_INPUT_DATA][STATE] = state

        return state


edit_date_and_time_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_date_and_time_callback,
                                       pattern='^(now|today|tomorrow|after_tomorrow|back)$')],
    states={
        'edit_hour': [CallbackQueryHandler(edit_hour_callback, pattern=r'^(back_btn|next_btn|back|\d+[:]00)$')],

    },
    fallbacks=[],

    map_to_parent={
        'edit': 'edit',
        'edit_date_and_time': 'edit_date_and_time'
    },
    persistent=True,
    name='edit_date_and_time_conversation'
)
# (0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-](20\d\d)
