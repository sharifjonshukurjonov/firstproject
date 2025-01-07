import telebot
from telebot import types
import json

# Bot tokeningizni kiriting
TOKEN = "7643242155:AAGMadSvFXad2gzbJN1BRC4pniJah0K2Bgs"
bot = telebot.TeleBot(TOKEN)

# Mahsulotlar faylini saqlash va yuklash
def omborni_yukla(user_id):
    try:
        with open(f"ombor_{user_id}.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def omborni_saqlash(user_id, ombor):
    with open(f"ombor_{user_id}.json", "w") as f:
        json.dump(ombor, f)

# Mahsulot funksiyalari
def mahsulot_qoshish(ombor, nomi, narxi, soni):
    for mahsulot in ombor:
        if mahsulot["nomi"] == nomi:
            mahsulot["narxi"] = (mahsulot["narxi"] * mahsulot["soni"] + narxi * soni) / (mahsulot["soni"] + soni)
            mahsulot["soni"] += soni
            return
    ombor.append({"nomi": nomi, "narxi": narxi, "soni": soni})

def mahsulot_ayirish(ombor, nomi, soni):
    for mahsulot in ombor:
        if mahsulot["nomi"] == nomi:
            if mahsulot["soni"] >= soni:
                mahsulot["soni"] -= soni
                if mahsulot["soni"] == 0:
                    ombor.remove(mahsulot)
                return True
            else:
                return False
    return None

def mahsulot_narxini_ozgartirish(ombor, nomi, yangi_narxi):
    for mahsulot in ombor:
        if mahsulot["nomi"] == nomi:
            mahsulot["narxi"] = yangi_narxi
            return True
    return False

# Asosiy menyu
menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    types.KeyboardButton("➕ Mahsulot qo'shish"),
    types.KeyboardButton("➖ Mahsulot ayirish"),
    types.KeyboardButton("📋 Omborni ko'rish"),
    types.KeyboardButton("✏️ Mahsulot narxini o'zgartirish")
)

# /start komanda
@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.chat.id
    bot.send_message(
        user_id,
        "👋 Assalomu alaykum! Ombor boshqaruv botiga xush kelibsiz. Tugmalardan birini tanlang:",
        reply_markup=menu
    )


# /help komanda
@bot.message_handler(commands=["help"])
def help_handler(message):
    user_id = message.chat.id
    help_text = (
        "🆘 <b>Yordam</b>\n\n"
        "Botdan foydalanish uchun quyidagi tugmalardan birini tanlang:\n"
        "➕ <b>Mahsulot qo'shish</b> - Omborga yangi mahsulot qo'shish.\n"
        "➖ <b>Mahsulot ayirish</b> - Ombordan mahsulotni ayirish.\n"
        "📋 <b>Omborni ko'rish</b> - Omborda mavjud mahsulotlarni ko'rish.\n"
        "✏️ <b>Narxni o'zgartirish</b> - Mahsulot narxini yangilash.\n\n"
        "🔗 <b>Yordam kerakmi?</b> Biz bilan bog'laning: @millioner_6690"
    )
    bot.send_message(user_id, help_text, parse_mode="HTML")



@bot.message_handler(func=lambda message: message.text == "🔙 Orqaga qaytish")
def back_to_main_menu(message):
    bot.send_message(message.chat.id, "Bosh menyu", reply_markup=menu)

# Mahsulot qo'shish funksiyasi
@bot.message_handler(func=lambda message: message.text == "➕ Mahsulot qo'shish")
def add_handler(message):
    user_id = message.chat.id
    ombor = omborni_yukla(user_id)

    def nom_qabul(message):
        nomi = message.text.capitalize()
        bot.send_message(user_id, "📍 Mahsulot narxini kiriting:")
        bot.register_next_step_handler(message, narx_qabul, nomi)

    def narx_qabul(message, nomi):
        try:
            narxi = float(message.text)
            bot.send_message(user_id, "📦 Mahsulot sonini kiriting:")
            bot.register_next_step_handler(message, son_qabul, nomi, narxi)
        except ValueError:
            bot.send_message(user_id, "❌ Iltimos, narxni to'g'ri kiriting!")
            bot.register_next_step_handler(message, narx_qabul, nomi)

    def son_qabul(message, nomi, narxi):
        try:
            soni = int(message.text)
            mahsulot_qoshish(ombor, nomi, narxi, soni)
            omborni_saqlash(user_id, ombor)
            bot.send_message(user_id, f"✅ {nomi} muvaffaqiyatli qo'shildi!", reply_markup=menu)
        except ValueError:
            bot.send_message(user_id, "❌ Iltimos, sonini to'g'ri kiriting!")
            bot.register_next_step_handler(message, son_qabul, nomi, narxi)

    bot.send_message(user_id, "✏️ Mahsulot nomini kiriting:")
    bot.register_next_step_handler(message, nom_qabul)

# Mahsulotdan ayirish funksiyasi
@bot.message_handler(func=lambda message: message.text == "➖ Mahsulot ayirish")
def subtract_handler(message):
    user_id = message.chat.id
    ombor = omborni_yukla(user_id)

    if not ombor:
        bot.send_message(user_id, "🗃 Omboringiz bo'sh!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for mahsulot in ombor:
        keyboard.add(types.KeyboardButton(mahsulot["nomi"]))
    keyboard.add(types.KeyboardButton("🔙 Orqaga qaytish"))

    bot.send_message(user_id, "🔄 Qaysi mahsulotdan ayirmoqchisiz:", reply_markup=keyboard)

    def quantity_to_subtract(message):
        if message.text == "🔙 Orqaga qaytish":
            back_to_main_menu(message)
            return

        nomi = message.text
        bot.send_message(user_id, f"📦 {nomi} mahsulotidan qancha ayirmoqchisiz?")
        bot.register_next_step_handler(message, subtract_quantity, nomi, ombor)

    def subtract_quantity(message, nomi, ombor):
        try:
            soni = int(message.text)
            result = mahsulot_ayirish(ombor, nomi, soni)
            if result is True:
                omborni_saqlash(user_id, ombor)
                bot.send_message(user_id, f"✅ {nomi} mahsulotidan {soni} dona ayirildi!", reply_markup=menu)
            elif result is False:
                bot.send_message(user_id, f"❌ Omborda {nomi} yetarli emas.")
            else:
                bot.send_message(user_id, "❌ Mahsulot topilmadi.")
        except ValueError:
            bot.send_message(user_id, "❌ Iltimos, sonini to'g'ri kiriting!")
            bot.register_next_step_handler(message, subtract_quantity, nomi, ombor)

    bot.register_next_step_handler(message, quantity_to_subtract)

# Narx o'zgartirish funksiyasi
@bot.message_handler(func=lambda message: message.text == "✏️ Mahsulot narxini o'zgartirish")
def change_price_handler(message):
    user_id = message.chat.id
    ombor = omborni_yukla(user_id)

    if not ombor:
        bot.send_message(user_id, "🗃 Omboringiz bo'sh! Narxni o'zgartirish uchun mahsulot qo'shing.")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for mahsulot in ombor:
        keyboard.add(types.KeyboardButton(mahsulot["nomi"]))
    keyboard.add(types.KeyboardButton("🔙 Orqaga qaytish"))

    bot.send_message(user_id, "🔄 Narxini o'zgartirmoqchi bo'lgan mahsulotni tanlang:", reply_markup=keyboard)

    def new_price_handler(message):
        if message.text == "🔙 Orqaga qaytish":
            back_to_main_menu(message)
            return

        nomi = message.text
        bot.send_message(user_id, f"📍 {nomi} mahsulotining yangi narxini kiriting:")
        bot.register_next_step_handler(message, update_price, nomi)

    def update_price(message, nomi):
        try:
            yangi_narxi = float(message.text)
            if mahsulot_narxini_ozgartirish(ombor, nomi, yangi_narxi):
                omborni_saqlash(user_id, ombor)
                bot.send_message(user_id, f"✅ {nomi} mahsulotining narxi yangilandi!", reply_markup=menu)
            else:
                bot.send_message(user_id, "❌ Mahsulot topilmadi.")
        except ValueError:
            bot.send_message(user_id, "❌ Iltimos, yangi narxni to'g'ri kiriting!")
            bot.register_next_step_handler(message, update_price, nomi)

    bot.register_next_step_handler(message, new_price_handler)

# Omborni ko'rish funksiyasi
@bot.message_handler(func=lambda message: message.text == "📋 Omborni ko'rish")
def view_inventory_handler(message):
    user_id = message.chat.id
    ombor = omborni_yukla(user_id)

    if not ombor:
        bot.send_message(user_id, "🗃 Omboringizda mahsulot yo'q.")
    else:
        inventory_list = "\n".join([f"{mahsulot['nomi']} - {mahsulot['soni']} dona - {mahsulot['narxi']} so'm" for mahsulot in ombor])
        bot.send_message(user_id, f"📋 Omboringizdagi mahsulotlar:\n{inventory_list}")

# Botni ishga tushurish
bot.polling(none_stop=True, timeout=30)