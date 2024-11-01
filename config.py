from os import environ

# bot
API_ID = int(environ.get('API_ID', '22980696'))
API_HASH = environ.get('API_HASH', '2b653cb53821a82097efaba6732f5d75')
BOT_TOKEN = environ.get('BOT_TOKEN', '7776137055:AAGhSffaIGl1MvUUl1969RiOBcsFhK9zSsk')

# database

DATABASE_URL = environ.get('DATABASE_URL', 'mongodb+srv://Zfile:zfile@cluster0.erkr0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
