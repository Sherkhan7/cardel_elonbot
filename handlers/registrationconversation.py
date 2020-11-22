from telegram import Update
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters,
                          CallbackQueryHandler)
from inlinekeyboards import InlineKeyboard
from filters import *
from replykeyboards import ReplyKeyboard
from DB import insert_user
from helpers import set_user_data
from languages import LANGS
from globalvariables import *
from replykeyboards.replykeyboardvariables import *
from inlinekeyboards.inlinekeyboardvariables import *
from helpers import wrap_tags
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
logger = logging.getLogger()

FULLNAME, LANG = ('fullname', 'lang')


def do_command(update: Update, context: CallbackContext):
    # with open('update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    command = update.message.text

    if command == '/start' or command == '/menu':

        if user:

            if user[LANG] == LANGS[0]:
                text = "Siz ro'yxatdan o'tgansiz"

            if user[LANG] == LANGS[1]:
                text = "Вы зарегистрированы"

            if user[LANG] == LANGS[2]:
                text = "Сиз рўйхатдан ўтгансиз"

            text = f'\U000026A0 {text} !'

            if command == '/menu':

                if user[LANG] == LANGS[0]:
                    reply_text = "Menyu"

                if user[LANG] == LANGS[1]:
                    reply_text = "Меню"

                if user[LANG] == LANGS[2]:
                    reply_text = "Меню"

                text = f'\U0001F4D6 {reply_text}'

            reply_keyboard = ReplyKeyboard(menu_keyboard, user[LANG]).get_keyboard()
            update.message.reply_text(text, reply_markup=reply_keyboard)

            state = ConversationHandler.END

        else:
            user_data[USER_INPUT_DATA] = dict()
            user_data[USER_INPUT_DATA][TG_ID] = update.effective_user.id
            user_data[USER_INPUT_DATA][USERNAME] = update.effective_user.username

            inline_keyboard = InlineKeyboard(langs_keyboard).get_keyboard()
            message = update.message.reply_text('Tilni tanlang\n'
                                                'Выберите язык\n'
                                                'Тилни танланг', reply_markup=inline_keyboard)
            user_data[USER_INPUT_DATA][MESSAGE_ID] = message.message_id

            state = LANG

        logger.info('user_data: %s', user_data)

        return state


def lang_callback(update: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data

    callback_query = update.callback_query

    if callback_query:

        data = callback_query.data

        user_data = context.user_data
        user_data[USER_INPUT_DATA].pop(MESSAGE_ID)

        user_data[USER_INPUT_DATA][LANG] = data

        if data == LANGS[0]:
            edit_text = "Til: \U0001F1FA\U0001F1FF"
            text = "Salom !\n" \
                   "Ism va familyangizni quyidagi formatda yuboring"
            example = "Misol: Sherzod Esanov"

        if data == LANGS[1]:
            edit_text = 'Язык: \U0001F1F7\U0001F1FA'
            text = 'Привет !\n' \
                   'Отправьте свое имя и фамилию в формате ниже'
            example = 'Пример: Шерзод Эсанов'

        if data == LANGS[2]:
            edit_text = "Тил: \U0001F1FA\U0001F1FF"
            text = "Салом !\n" \
                   "Исм ва фамилянгизни қуйидаги форматда юборинг"
            example = "Мисол: Шерзод Эсанов"

        text = f'\U0001F44B {text}:\n\n {wrap_tags(example)}'

        callback_query.edit_message_text(edit_text)
        callback_query.message.reply_html(text)

        state = FULLNAME

    else:

        context.bot.edit_message_reply_markup(update.effective_user.id, user_data[USER_INPUT_DATA].pop(MESSAGE_ID))

        inline_keyboard = InlineKeyboard(langs_keyboard).get_keyboard()
        message = update.message.reply_text('Tilni tanlang\n'
                                            'Выберите язык\n'
                                            'Тилни танланг', reply_markup=inline_keyboard, quote=True)
        user_data[USER_INPUT_DATA][MESSAGE_ID] = message.message_id

        state = LANG

    logger.info('user_data: %s', user_data)

    return state


def fullname_callback(update: Update, context: CallbackContext):
    # with open('../update.json', 'w') as update_file:
    #     update_file.write(update.to_json())
    user_data = context.user_data

    text = update.message.text
    fullname = fullname_filter(text)

    if fullname:

        user_data[USER_INPUT_DATA][NAME] = fullname[0]
        user_data[USER_INPUT_DATA][SURNAME] = fullname[1]

        insert_user(user_data[USER_INPUT_DATA])
        set_user_data(update.effective_user.id, user_data)

        if user_data[USER_INPUT_DATA][LANG] == LANGS[0]:
            text = "Tabriklaymiz !\n" \
                   "Siz ro'yxatdan muvofaqqiyatli o'tdingiz\n\n" \
                   "E'lon berishingiz mumkin"

        if user_data[USER_INPUT_DATA][LANG] == LANGS[1]:
            text = "Поздравляем !\n" \
                   "Вы успешно зарегистрировались\n\n" \
                   "Вы можете помешать объявление"

        if user_data[USER_INPUT_DATA][LANG] == LANGS[2]:
            text = "Табриклаймиз !\n" \
                   "Сиз рўйхатдан мувофаққиятли ўтдингиз\n\n" \
                   "Эълон беришингиз мумкин"

        text = '\U0001F44F\U0001F44F\U0001F44F ' + text

        reply_keyboard = ReplyKeyboard(menu_keyboard, user_data[USER_INPUT_DATA][LANG]).get_keyboard()
        update.message.reply_text(text, reply_markup=reply_keyboard)

        del user_data[USER_INPUT_DATA]

        state = ConversationHandler.END

    else:

        if user_data[USER_INPUT_DATA][LANG] == LANGS[0]:
            text = "Ism va familya xato yuborildi !\n" \
                   "Qaytadan quyidagi formatda yuboring"
            example = "Misol: Sherzod Esanov"

        if user_data[USER_INPUT_DATA][LANG] == LANGS[1]:
            text = 'Имя и фамилия введено неверное !\n' \
                   'Отправьте еще раз в следующем формате'
            example = 'Пример: Шерзод Эсанов'

        if user_data[USER_INPUT_DATA][LANG] == LANGS[2]:
            text = "Исм ва фамиля хато юборилди !\n" \
                   "Қайтадан қуйидаги форматда юборинг"
            example = "Мисол: Шерзод Эсанов"

        text = f'\U000026A0 {text}:\n\n {wrap_tags(example)}'

        update.message.reply_html(text, quote=True)

        state = FULLNAME

    logger.info('user_data: %s', user_data)

    return state


registration_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(['start', 'menu'], do_command, filters=~Filters.update.edited_message),
    ],
    states={
        LANG: [CallbackQueryHandler(lang_callback), MessageHandler(Filters.text, lang_callback)],

        FULLNAME: [MessageHandler(Filters.text, fullname_callback)],
    },
    fallbacks=[
        # CommandHandler('cancel', do_cancel)
    ],
    persistent=True,
    name='registration_conversation'
)
