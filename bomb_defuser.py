#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
#
# bomb_defuser.py - python implementation of Bomb Defusal Manual he.pdf':
# https://www.bombmanual.com/he/print/KeepTalkingAndNobodyExplodes-BombDefusalManual-v2-he.pdf
#
# https://github.com/arduino12/ 2022/10/21
#
# https://github.com/python-telegram-bot/python-telegram-bot
# pip install python-telegram-bot --pre
#
# https://steamcommunity.com/app/341800/discussions/0/481115363870829238/
import os

while(1):
    try:
        from telegram.ext import (
            Application,
            CommandHandler,
            ContextTypes,
            CallbackQueryHandler,
            ConversationHandler,
            MessageHandler,
            filters,
        )
        from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
    except:
        os.system('pip3 install python-telegram-bot --pre')
        continue
    break


def split_list(l, index=4):
    return [[str(j) for j in l[i:i+abs(index)][::index // abs(index)]] for i in range(0, len(l), abs(index))]


RED, YELLOW, BLUE, WHITE, BLACK = 'אצכלש'
WORDS = [
    'אבטיח', 'אטליז', 'אמנות', 'אפרוח', 'ארטיק',
    'בוטיק', 'ביטוח', 'ברווז', 'דוגמה', 'דחליל',
    'זירוז', 'זרנוק', 'חללית', 'ירושה', 'כוסמת',
    'כתובת', 'מחוגה', 'מצודה', 'נחשול', 'ניצול',
    'סיסמה', 'סיפוח', 'פרוטה', 'ציפור', 'צלצול',
    'ריבוע', 'רצועה', 'שאלות', 'שושלת', 'שיעול',
    'שליטה', 'שמיכה', 'תינוק', 'תנשמת', 'תרדמת',
]

SYMBOLS_IN_ORDERS = [
    "ϬӬ҂æψҊΩ",
    "ψټѢϾ¶Ѯ★",
    "Ϭ¶ѢѬҖ¿ټ",
    "©ѼҨҖԆƛ☆",
    "ӬϘϿҨ☆ϗ¿",
    "ϘѦƛϰѬϗϿ",
]

SYMBOLS_KEYBOARD = split_list(
    list(set(''.join(SYMBOLS_IN_ORDERS))), 5) + [['Done']]

SERIAL_KEYBOARD = split_list(['A1', 'A2', 'B1', 'B2'], 2)

WIRES_KEYBOARD = split_list(
    ['אדום', 'צהוב', 'כחול', 'לבן', 'שחור'], 5) + [['יאללה']]

BATTERIES_KEYBOARD = split_list(range(8))

CONNECTORS_KEYBOARD = split_list(
    ['DVI', 'PAR', 'PS2', 'RJ45', 'SER', 'RCA'], 3) + [['Done']]

HEBREW_KEYBOARD = split_list('אבגדהוזחטיכלמנסעפצקרשת', -6) + [['זהו']]

INDICATORS_KEYBOARD = split_list(
    ['SND', 'CLR', 'CAR', 'IND', 'FRQ', 'SIG', 'NSA', 'MSA', 'TRN', 'BOB', 'FRK'], 4) + [['סיימתי']]

# 1ח 0ל 2ס 3מ 4ב
COMPLEX_WIRES = [
    '1W', '1WS', '0WL', '4WSL',
    '2R', '1RS', '4RL', '4RSL',
    '2B', '0BS', '3BL', '3BSL',
    '2RB', '3RBS', '2RBL', '0RBSL',
]


class BombDefuser(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self._serial_number = ''
        self._battery_count = 0
        self._connectors = []
        self._indicators = []

    def _is_even_serial_number(self):
        # return not int(serial_number[-1]) % 2
        return self._serial_number[-1] in '02468'

    def solve_simple_wires(self, wires):
        l = len(wires)
        if l == 3:
            if RED not in wires:
                return 2
            if wires.count(BLUE) > 1 and not wires.endswith(WHITE):
                return wires.rfind(BLUE) + 1
            return 3
        elif l == 4:
            if wires.count(RED) > 1 and not self._is_even_serial_number():
                return wires.rfind(RED) + 1
            if wires.endswith(YELLOW) and RED not in wires or wires.count(BLUE) == 1:
                return 1
            if wires.count(YELLOW) > 1:
                return 4
            return 2
        elif l == 5:
            if wires.endswith(BLACK) and not self._is_even_serial_number():
                return 4
            if wires.count(YELLOW) > 1 and wires.count(RED) == 1:
                return 1
            if not wires.count(BLACK):
                return 2
            return 1
        elif l == 6:
            if not wires.count(YELLOW) and not self._is_even_serial_number():
                return 3
            if not wires.count(RED) and not (wires.count(YELLOW) == 1 and wires.count(WHITE) > 1):
                return 6
            return 4
        return -1  # error

    def solve_password(self, charsets):
        if isinstance(charsets, str):
            charsets = [charsets]
        return [word for word in WORDS if
                all(word[i] in charset for i, charset in enumerate(charsets))]

    def solve_weird_symbols(self, symbols):
        return set(map(lambda allSymbolsInOrder: ''.join([symbolInOrder[0] for symbolInOrder in sorted([(symbol, allSymbolsInOrder.index(symbol)) for symbol in symbols], key=lambda s: s[1])]),
                       [allSymbolsInOrder for allSymbolsInOrder in SYMBOLS_IN_ORDERS if all(symbol in allSymbolsInOrder for symbol in symbols)]))

    def solve_complex_wires(self):
        return [w[1:] if [0, 1, self._is_even_serial_number(), 'PAR' in self._connectors, self._battery_count >= 2][int(w[0])] else ' ' for w in COMPLEX_WIRES]

    def __str__(self):
        return f'''
מספר סידורי: {self._serial_number}
סוללות: {self._battery_count}
חיוויים: {", ".join(self._indicators)}
חיבורים: {", ".join(self._connectors)}'''


bomb_defuser = BombDefuser()


TOKEN = '5587993580:AAFx7dur_bG9zP_RSN1cQhQnbyyedGEzT04'  # t.me/BombDefuserBot
MENU_STATE, REPLY_STATE, REPLY_INIT_STATE = range(3)
MENU_KEY_NEW_BOMB = 'פצצה חדשה'
MENU_KEY_SIMPLE_WIRES = 'חוטים'
MENU_KEY_COMPLEX_WIRES = 'כבלים'
MENU_KEY_WORDS = 'מילים'
MENU_KEY_SYMBOLS_WORDS = 'סמלים'
MENU_KEYBOARD = split_list([MENU_KEY_SIMPLE_WIRES, MENU_KEY_COMPLEX_WIRES, MENU_KEY_WORDS,
                            MENU_KEY_SYMBOLS_WORDS], -4) + [[MENU_KEY_NEW_BOMB]]
MENU_MARKUP = ReplyKeyboardMarkup(MENU_KEYBOARD, one_time_keyboard=True)


def get_inline_keyboard_markup(keys, marked_keys=[]):
    keyboard = [list(map(lambda n: InlineKeyboardButton(
        f'[{n}]' if n in marked_keys else n, callback_data=n), list(x))) for x in keys]

    return InlineKeyboardMarkup(keyboard, one_time_keyboard=False)


def get_pattern_from_keyboard(keyboard):
    return f'^{"|".join(item for innerlist in keyboard for item in innerlist)}$'


def get_callback_handler(callback, keyboard):
    return CallbackQueryHandler(callback, pattern=get_pattern_from_keyboard(keyboard))


async def handle_start(update, context):
    context.user_data['menu'] = MENU_KEY_NEW_BOMB
    markup = get_inline_keyboard_markup(SERIAL_KEYBOARD)
    bomb_defuser.reset()

    await update.message.reply_text('אעאעאע!', reply_markup=MENU_MARKUP)
    await update.message.reply_text('מה המספר הסידורי?', reply_markup=markup)

    return REPLY_INIT_STATE


async def handle_menu(update, context):
    menu = update.message.text
    context.user_data['menu'] = menu
    context.user_data['symbols'] = []
    context.user_data['words'] = ''
    context.user_data['wires'] = ''
    markup = MENU_MARKUP
    ret = REPLY_STATE

    if menu == MENU_KEY_WORDS:
        reply = 'לחצו על האותיות עבור כל גליל מימין לשמאל'
        markup = get_inline_keyboard_markup(HEBREW_KEYBOARD)
    elif menu == MENU_KEY_COMPLEX_WIRES:
        reply = 'חיתכו את החוטים המופיעים בטבלה'
        markup = get_inline_keyboard_markup(
            split_list(bomb_defuser.solve_complex_wires()))
        ret = MENU_STATE
    elif menu == MENU_KEY_SIMPLE_WIRES:
        reply = 'לחצו על החוטים מלמעלה למטה'
        markup = get_inline_keyboard_markup(WIRES_KEYBOARD)
    elif menu == MENU_KEY_SYMBOLS_WORDS:
        reply = 'לחצו על ארבעת הסימנים'
        markup = get_inline_keyboard_markup(SYMBOLS_KEYBOARD)
    else:
        reply = '?'

    await update.message.reply_text(reply, reply_markup=markup)

    return ret


async def reply_symbols(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if (query.data == 'Done'):
        reply = bomb_defuser.solve_weird_symbols(context.user_data['symbols'])
        await query.edit_message_text('\n'.join(reply) or "לא מצאתי :(")
        return MENU_STATE
    else:
        if (query.data in context.user_data['symbols']):
            context.user_data['symbols'].remove(query.data)
        else:
            context.user_data['symbols'].append(query.data)

    markup = get_inline_keyboard_markup(
        SYMBOLS_KEYBOARD, context.user_data['symbols'])
    reply = 'לחצו על ארבעת הסימנים'
    await query.edit_message_text(reply, reply_markup=markup)

    return REPLY_STATE


async def reply_serial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    bomb_defuser._serial_number = query.data
    markup = get_inline_keyboard_markup(BATTERIES_KEYBOARD)
    await query.edit_message_text('כמה סוללות?', reply_markup=markup)

    return REPLY_INIT_STATE


async def reply_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if (query.data == 'זהו'):
        passwords = bomb_defuser.solve_password(
            context.user_data['words'].split())

        if (len(passwords) <= 2):
            await query.edit_message_text(', '.join(passwords))
            return MENU_STATE

        context.user_data['words'] += ' '
        return REPLY_STATE
    else:
        context.user_data['words'] += query.data

    return REPLY_STATE


async def reply_wires(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if (query.data == 'יאללה'):
        reply = bomb_defuser.solve_simple_wires(context.user_data['wires'])

        await query.edit_message_text(reply)
        return MENU_STATE
    else:
        context.user_data['wires'] += query.data[0]

    return REPLY_STATE


async def reply_batteries_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        count = int(query.data)
    except:
        count = 0

    bomb_defuser._battery_count = count
    markup = get_inline_keyboard_markup(INDICATORS_KEYBOARD)
    await query.edit_message_text('בחרו את החיוויים שיש על הפצצה', reply_markup=markup)

    return REPLY_INIT_STATE


async def reply_indicators(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    markup = get_inline_keyboard_markup(CONNECTORS_KEYBOARD)
    if (query.data == 'סיימתי'):
        await query.edit_message_text('בחרו את החיבורים שיש על הפצצה', reply_markup=markup)
        return REPLY_INIT_STATE
    else:
        bomb_defuser._indicators.append(query.data)

    return REPLY_INIT_STATE


async def reply_connectors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if (query.data == 'Done'):
        await query.edit_message_text(str(bomb_defuser))
        return MENU_STATE
    else:
        bomb_defuser._connectors.append(query.data)

    return REPLY_INIT_STATE


def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handle_start),
                      MessageHandler(filters.Regex(f'^{MENU_KEY_NEW_BOMB}$'), handle_start)],
        states={
            MENU_STATE: [
                MessageHandler(
                    filters.Regex(
                        f'^({"|".join(MENU_KEYBOARD[0])})$'), handle_menu
                ),
            ],
            REPLY_INIT_STATE: [
                get_callback_handler(reply_serial, SERIAL_KEYBOARD),
                get_callback_handler(
                    reply_batteries_count, BATTERIES_KEYBOARD),
                get_callback_handler(reply_indicators, INDICATORS_KEYBOARD),
                get_callback_handler(reply_connectors, CONNECTORS_KEYBOARD),
            ],
            REPLY_STATE: [
                get_callback_handler(reply_wires, WIRES_KEYBOARD),
                get_callback_handler(reply_symbols, SYMBOLS_KEYBOARD),
                get_callback_handler(reply_words, HEBREW_KEYBOARD),
            ],
        },
        fallbacks=[MessageHandler(filters.Regex(f'^{MENU_KEY_NEW_BOMB}$'), handle_start),
                   MessageHandler(filters.Regex('^Done$'), handle_menu)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
