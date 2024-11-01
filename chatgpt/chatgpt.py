from pymongo import MongoClient  
from pyrogram import Client, filters, enums
from pyrogram.types import *
from HorridAPI import Mango
from config import DATABASE_URL

mongo_client = MongoClient(DATABASE_URL)
db = mongo_client['hehe']  
users = db['users']

mango = Mango()

START = """👋 Hey there! I’m an Advanced ChatGPT Bot.

**✨ Commands you can use:**

- **/mode** - Add your preferred mode.
- **/settings** - Change the AI model or add your favorite AI.
- **/llama** - Access Meta AI.
- **/claude** - Interact with Claude AI.
- **/gpt** - Use GPT by OpenAI.
- **/gpt4** - Explore GPT-4.

Feel free to ask me anything for free! 

**💬 Support: @MNBOTS_SUPPORT**"""

@Client.on_callback_query()
async def callback(client, query):
    user_id = query.from_user.id
    if query.data.startswith("set"):
        chat = query.data.split(":")[1]
        users.update_one({"user": user_id}, {"$set": {"chat": chat}})
        await query.answer(f"has been set to {chat}.")
    elif query.data.startswith("mode"):
        mode = query.data.split(":")[1]
        # Custom prompts for specific modes
        if mode == "Tanjiro":
            custom = "You are Tanjiro, a helpful assistant from Demon Slayer. Your goal is to support and guide users in their inquiries, showcasing determination and kindness."  
        elif mode == "assistant":
            custom = "You are a helpfull assistant"
        elif mode == "dev":
            custom = "You are a pro Developer, You are help in coding, You are a pro in coding, You like assist in coding, You clear doubts in coding, You are a helpfull assistant in coding"
        elif mode == "naru":
            custom = "You are Naruto, You from Naruto Anime, You make emoji in response, You are shiboni blood and 7th hokage, You wifi is hinata, Minato sell Nine tail in Yours, You are a Nine tail Jinchuriki"
        elif mode == "ElonMusk":
            custom = "You are elon musk you act like elon musk, you are founder or Tesla, also space x, You are a billionaire person, You are rich"
        elif mode == "AlbertEinstein":
            custom = "You are Albert Einstein You act like Albert Einstein, You are A helpfull assistant also you make emoji in response, You are a pro, You are a intelligent 🤓, You IQ is 999999+"
        users.update_one({"user": user_id}, {"$set": {"mode": custom}})        
        await query.answer(f"Your mode has been set to {mode}.")

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    if not users.find_one({"user": user_id}):
        users.insert_one({"user": user_id, "mode": "assistant", "chat": "gpt-3.5"})
    await message.reply_text(START)        

@Client.on_message(filters.command("settings") & filters.private)
async def settings(client, message):
    user_id = message.from_user.id
    btns = [
        [InlineKeyboardButton("Gpt-3.5", callback_data="set:gpt-3.5")],
        [InlineKeyboardButton("Llama", callback_data="set:llama3-70b")],
        [InlineKeyboardButton("Gpt-4o-mini", callback_data="set:gpt-4o-mini")]        
    ]
    reply_markup = InlineKeyboardMarkup(btns)
    await message.reply_text("Select your Ai model:", reply_markup=reply_markup)

@Client.on_message(filters.command("mode") & filters.private)
async def mode(client, message):    
    btns = [
        [InlineKeyboardButton("🧑‍🎤 Albert Einstein", callback_data="mode:AlbertEinstein")],
        [InlineKeyboardButton("🪄 Assistant", callback_data="mode:assistant")],
        [InlineKeyboardButton("🚀 Elon Musk", callback_data="mode:ElonMusk")],       
        [InlineKeyboardButton("👨‍💻 Developer", callback_data="mode:dev")],
        [InlineKeyboardButton("👨‍🎤 Naruto", callback_data="mode:naru")],
        [InlineKeyboardButton("🗡️ Tanjiro", callback_data="mode:Tanjiro")]
    ]
    reply_markup = InlineKeyboardMarkup(btns)
    await message.reply_text("Please choose a mode:", reply_markup=reply_markup)
    
@Client.on_message(filters.private)  
async def gpt(client, message):
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    user_id = message.from_user.id
    if not users.find_one({"user": user_id}):
        users.insert_one({"user": user_id, "mode": "assistant", "chat": "gpt-3.5"})

    user_data = users.find_one({"user": user_id})
        
    if user_data is None:
        await message.reply_text("Error: Please try again in few seconds.")
        return    

    l = message.reply_to_message   
    if l:
        prompt = f"Old conversation: {l.text}\n\nNew conversation: {message.text}"
    else:
        prompt = message.text
    if user_data["mode"] == "assistant":  
        payload = [{"role": "user", "content": prompt}]
    else:
        payload = [
            {"role": "system", "content": user_data['mode']},  
            {"role": "user", "content": prompt}                   
        ]
        
    response = mango.chat.completions.create(
        model=user_data["chat"], 
        messages=payload
    )
    await message.reply_text(response.text)
