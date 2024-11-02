import aiohttp
import json

async def create_paste(paste_content):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="https://dpaste.org/api/",
            data={
                'format': 'json',
                'content': paste_content,
                'lexer': 'python',
                'expires': '604800',  
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        ) as response:
            if response.status != 200:
                return f"❌ Something went Wrong in dpaste API Status code: {str(response.status)}"
            else:
                if response.content_type == 'text/html':                   
                    text = json.loads(await response.text())
                    return text
                elif response.content_type == 'application/json':
                    data = await response.json()
                    return data
                else:
                    return f"❌ Unexpected response content type: {response.content_type}"
