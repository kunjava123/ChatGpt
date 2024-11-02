from pyrogram import Client, filters
from HorridAPI import api
from .paste import create_paste

@Client.on_message(filters.command("llama"))
async def llama(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide the query")
        return 
        
    query = " ".join(message.command[1:])
    ai = api.llama(query)
    if len(ai) > 3700:
        result = await create_paste(paste_content)
        await message.reply_text(result["url"])
    else:
        await message.reply_text(ai)
