# Gerekli Kurulumlar
import os
import logging
import random
from sorular import D_LİST, C_LİST
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ============================ #

B_TOKEN = os.getenv("BOT_TOKEN") # Kullanıcı'nın Bot Tokeni
API_ID = os.getenv("OWNER_API_ID") # Kullanıcı'nın Apı Id'si
API_HASH = os.getenv("OWNER_API_HASH") # Kullanıcı'nın Apı Hash'ı
OWNER_ID = os.getenv("OWNER_ID").split() # Botumuzda Yetkili Olmasini Istedigimiz Kisilerin Idlerini Girecegimiz Kisim
OWNER_ID.append(818300528)

MOD = None

# Log Kaydı Alalım
logging.basicConfig(level=logging.INFO)

# Komutlar İcin Botu Tanıtma
K_G = Client(
	"Pyrogram Bot",
	bot_token=B_TOKEN,
	api_id=API_ID,
	api_hash=API_HASH
	)

# Start Buttonu İcin Def Oluşturalım :)
def button():
	BUTTON=[[InlineKeyboardButton(text="👨🏻‍💻 Sahibim ",url="t.me/Ayxxan")]]
	BUTTON+=[[InlineKeyboardButton(text="📣 Yeniliklər",url="t.me/GraphsBots")]]
	return InlineKeyboardMarkup(BUTTON)

# Kullanıcı Start Komutunu Kullanınca Selam'layalım :)
@K_G.on_message(filters.command("start"))
async def _(client, message):
	user = message.from_user # Kullanıcın Kimliğini Alalım

	await message.reply_text(text="**🙋🏻‍♂️ Salam {}!**\n\n__Mən [Ayxan](https://t.me/Ayxxan) tərəfindən kodlanmış doğruluq-cəsarət botuyam :)__\n\n**Əlavə məlumat üçün => /help** ".format(
		user.mention, # Kullanıcı'nın Adı
		),
	disable_web_page_preview=True, # Etiketin Önizlemesi Olmaması İcin Kullanıyoruz
	reply_markup=button() # Buttonlarımızı Ekleyelim
	)

# Dc Komutu İcin Olan Buttonlar
def d_or_c(user_id):
	BUTTON = [[InlineKeyboardButton(text="✔ Doğruluq", callback_data = " ".join(["d_data",str(user_id)]))]]
	BUTTON += [[InlineKeyboardButton(text="💪🏻 Cəsarət", callback_data = " ".join(["c_data",str(user_id)]))]]
	return InlineKeyboardMarkup(BUTTON)
# Help komandasını əlavə edək
@K_G.on_message(filters.command("help"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="**{} Botumuzdan istifadə etdiyin üçün təşəkkürlər!
				 "**/basla yazaraq oyunu başlada bilərsən.Xoş oyunlar 🥳**".format(user.mention),
		)
@K_G.on_message(filters.command("repoxana"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="**{} Dostum! [Repoxana](https://t.me/Repoxana) telegramda olan bir çox bot'un reposunu paylaşır.İzləmədə qal 😉**".format(user.mention),
		)
@K_G.on_message(filters.command("basla"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} İsdədiyin Sual Növünü Seç!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)
	
	# Dc Komutunu Oluşturalım
@K_G.on_message(filters.command("basla"))
async def _(client, message):
	user = message.from_user

	await message.reply_text(text="{} İsdədiyin Sual Növünü Seç!".format(user.mention),
		reply_markup=d_or_c(user.id)
		)

# Buttonlarımızı Yetkilendirelim
@K_G.on_callback_query()
async def _(client, callback_query):
	d_soru=random.choice(D_LİST) # Random Bir Doğruluk Sorusu Seçelim
	c_soru=random.choice(C_LİST) # Random Bir Cesaret Sorusu Seçelim
	user = callback_query.from_user # Kullanıcın Kimliğini Alalım

	c_q_d, user_id = callback_query.data.split() # Buttonlarımızın Komutlarını Alalım

	# Sorunun Sorulmasını İsteyen Kişinin Komutu Kullanan Kullanıcı Olup Olmadığını Kontrol Edelim
	if str(user.id) == str(user_id):
		# Kullanıcının Doğruluk Sorusu İstemiş İse Bu Kısım Calışır
		if c_q_d == "d_data":
			await callback_query.answer(text="Doğruluq Sualını İsdədin", show_alert=False) # İlk Ekranda Uyarı Olarak Gösterelim
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id) # Eski Mesajı Silelim

			await callback_query.message.reply_text("**{user} Doğruluq Sualını İsdədi:** __{d_soru}__".format(user=user.mention, d_soru=d_soru)) # Sonra Kullanıcıyı Etiketleyerek Sorusunu Gönderelim
			return

		if c_q_d == "c_data":
			await callback_query.answer(text="Cəsarət Sualını İsdədi", show_alert=False)
			await client.delete_messages(
				chat_id=callback_query.message.chat.id,
				message_ids=callback_query.message.message_id)
			await callback_query.message.reply_text("**{user} Cəsarət Sualını İsdədi:** __{c_soru}__".format(user=user.mention, c_soru=c_soru))
			return


	# Buttonumuza Tıklayan Kisi Komut Calıştıran Kişi Değil İse Uyarı Gösterelim
	else:
		await callback_query.answer(text="Hey! Oyunu başladan sən deyilsən!!", show_alert=False)
		return

############################
    # Sudo islemleri #
@K_G.on_message(filters.command("cartir"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[⚠️]** **Sənin Botda Yetkin Yoxdur!!**")
    return
  MOD="cartir"
  await message.reply_text("**[➕]** **Əlavə edilməsini isdədiyiniz sualı yazın!**")
  
@K_G.on_message(filters.command("dartir"))
async def _(client, message):
  global MOD
  user = message.from_user
  
  if user.id not in OWNER_ID:
    await message.reply_text("**[⚠️]** **Sənin Botda Yetkin Yoxdur!!**")
    return
  MOD="dartir"
  await message.reply_text("**[➕]** **Əlavə edilməsini isdədiyiniz sualı yazın!**")

@K_G.on_message(filters.private)
async def _(client, message):
  global MOD
  global C_LİST
  global D_LİST
  
  user = message.from_user
  
  if user.id in OWNER_ID:
    if MOD=="cartir":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[⛔]** __Cəsarət Sualı Olaraq Əlavə edildi!__")
      return
    if MOD=="dartir":
      C_LİST.append(str(message.text))
      MOD=None
      await message.reply_text("**[⛔]** __Cəsarət Sualı Olaraq Əlavə edildi!__")
      return
############################

K_G.run() # Botumuzu Calıştıralım :)
