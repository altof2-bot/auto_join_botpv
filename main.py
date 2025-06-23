import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from deep_translator import GoogleTranslator

API_TOKEN = 'TON_TOKEN_ICI'
CANAL_USERNAME = 'sineur_x_bot'
ADMINS = [5116530698]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Obtenir l’IP publique
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except:
        return "IP non disponible"

# Commande /start
@dp.message(Command("start"))
async def start(message: types.Message):
    ip_address = get_public_ip()
    bouton = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Rejoindre le canal", url=f"https://t.me/{CANAL_USERNAME}")]
    ])
    texte = (
        "👋 Bienvenue sur le bot !\n"
        f"🌐 IP du serveur : {ip_address}\n"
        "🔒 Ce bot imite un comportement humain pour éviter le bannissement."
    )
    await message.answer(texte, reply_markup=bouton)

# Commande /admin
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.reply("⛔ Accès refusé.")
        return
    await message.reply("🔐 Panneau admin :\n- /stats\n- /add_admin [ID]\n- /del_admin [ID]\n- /broadcast [message]")

# Commande /stats
@dp.message(Command("stats"))
async def stats(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    await message.reply("📊 Statistiques :\n- Utilisateurs : à implémenter\n- Messages envoyés : à implémenter")

# Ajouter un admin
@dp.message(Command("add_admin"))
async def add_admin(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    try:
        new_id = int(message.text.split()[1])
        if new_id not in ADMINS:
            ADMINS.append(new_id)
            await message.reply(f"✅ Admin ajouté : {new_id}")
    except:
        await message.reply("❌ Utilisation : /add_admin [ID]")

# Supprimer un admin
@dp.message(Command("del_admin"))
async def del_admin(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    try:
        del_id = int(message.text.split()[1])
        if del_id in ADMINS:
            ADMINS.remove(del_id)
            await message.reply(f"✅ Admin supprimé : {del_id}")
    except:
        await message.reply("❌ Utilisation : /del_admin [ID]")

# Broadcast
@dp.message(Command("broadcast"))
async def broadcast(message: types.Message):
    if message.from_user.id not in ADMINS:
        return
    text = message.text.partition(' ')[2]
    await message.reply("📢 Fonction de diffusion à implémenter")

# ✅ Traduction automatique (ex: pour canal)
@dp.message()
async def translate_auto(message: types.Message):
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1)

    original = message.text
    try:
        translated = GoogleTranslator(source='auto', target='fr').translate(original)
        await message.reply(f"📝 Traduction FR :\n{translated}")
    except:
        await message.reply("⚠️ Erreur de traduction")

# Main async
async def main():
    print("🚀 Bot en cours d'exécution...")
    await dp.start_polling(bot)

# Lancement
if __name__ == '__main__':
    asyncio.run(main())
