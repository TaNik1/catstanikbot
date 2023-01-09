from main import bot, dp
from aiogram import types
import random
import requests
from data_base import Chat

hmtai_list = ["wave", "wink", "tea", "bonk", "punch", "poke", "bully", "pat", "kiss", "kick", "blush", "feed", "smug",
              "hug", "cuddle", "cry", "cringe", "slap", "five", "glomp", "happy", "hold", "nom", "smile", "throw",
              "lick", "bite", "dance", "boop", "sleep", "like", "kill", "tickle", "nosebleed", "threaten", "depression",
              "wolf_arts", "jahy_arts", "neko_arts", "coffee_arts", "wallpaper", "mobileWallpaper", "ass", "anal",
              "bdsm", "classic", "cum", "creampie", "manga", "femdom", "hentai", "incest", "masturbation", "public",
              "ero", "orgy", "elves", "yuri", "pantsu", "pussy", "glasses", "cuckold", "blowjob", "boobjob", "handjob",
              "footjob", "boobs", "thighs", "ahegao", "uniform", "gangbang", "tentacles", "nsfwNeko",
              "nsfwMobileWallpaper", "zettaiRyouiki"]

hmtai_list_sfw = ["wave", "wink", "tea", "bonk", "punch", "poke", "bully", "pat", "kiss", "kick", "blush", "feed",
                  "smug", "hug", "cuddle", "cry", "cringe", "slap", "five", "glomp", "happy", "hold", "nom", "smile",
                  "throw", "lick", "bite", "dance", "boop", "sleep", "like", "kill", "tickle", "nosebleed", "threaten",
                  "depression", "wolf_arts", "jahy_arts", "neko_arts", "coffee_arts", "wallpaper", "mobileWallpaper"]


@dp.message_handler(commands=['start'])
async def mess(message: types.Message):
    chat, create = Chat.get_or_create(tg_id=message.chat.id)
    chat.save()
    await bot.send_message(message.chat.id,
                           'Привет, любитель посмотреть интересные картинки ;)Знаешь ли ты, что, чтобы посмотреть на собачек, кошек и кошко-девочек не нужно подбирать подходящее время, не нужно боятся своих желаний и прятаться от голодных взглядов в твой смратфон/ пк? Наши картинки может смотреть даже младенец, а значит и ты тоже! Выбери категорию и наслаждайся!')


@dp.message_handler(commands=['cats'])
async def mess(message: types.Message):
    chat, create = Chat.get_or_create(tg_id=message.chat.id)
    chat.save()
    api_request = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(api_request)
    response = response.json()[0]['url']
    await bot.send_photo(message.chat.id, response)


@dp.message_handler(commands=['dogs'])
async def mess(message: types.Message):
    chat, create = Chat.get_or_create(tg_id=message.chat.id)
    chat.save()
    api_request = 'https://dog.ceo/api/breeds/image/random'
    response = requests.get(api_request)
    response = response.json()['message']
    await bot.send_photo(message.chat.id, response)


@dp.message_handler(commands=['girlcats_nsfw'])
async def mess(message: types.Message):
    chat, create = Chat.get_or_create(tg_id=message.chat.id)
    chat.save()
    if chat.settings == 1:
        res = requests.get(f"https://hmtai.hatsunia.cfd/v2/nsfwNeko")
        if "message" in res.json():
            await bot.send_message(message.chat.id, 'Фотография случайно не отправилась')
        else:
            await bot.send_photo(message.chat.id, res.json()["url"])


@dp.message_handler(commands=['girlcats'])
async def mess(message: types.Message):
    chat, create = Chat.get_or_create(tg_id=message.chat.id)
    chat.save()
    if chat.settings == 1:
        res = requests.get(f"https://hmtai.hatsunia.cfd/v2/neko_arts")
        if "message" in res.json():
            await bot.send_message(message.chat.id, 'Фотография случайно не отправилась')
        else:
            await bot.send_photo(message.chat.id, res.json()["url"])


@dp.message_handler(commands=['hentai'])
async def mess(message: types.Message):
    chat, create = Chat.get_or_create(tg_id=message.chat.id)
    chat.save()
    if chat.settings == 1:
        category = random.choice(hmtai_list)
    else:
        category = random.choice(hmtai_list_sfw)
    res = requests.get(f"https://hmtai.hatsunia.cfd/v2/{category}")
    if "message" in res.json():
        await bot.send_message(message.chat.id, 'Фотография случайно не отправилась')
    else:
        await bot.send_photo(message.chat.id, res.json()["url"])


@dp.message_handler(commands=['gif'])
async def mess(message: types.Message):
    chat, create = Chat.get_or_create(tg_id=message.chat.id)
    chat.save()
    res = requests.get(f"https://hmtai.hatsunia.cfd/v2/gif")
    if "message" in res.json():
        await bot.send_message(message.chat.id, 'Фотография случайно не отправилась')
    else:
        await bot.send_animation(message.chat.id, res.json()["url"])


@dp.message_handler(commands=['nsfw_settings'])
async def mess(message: types.Message):
    if message.from_user.id == message.chat.id:
        await bot.send_message(message.chat.id, 'Комманда предназначена тольок для групп')
    else:
        f = await bot.get_chat_member(message.chat.id, message.from_user.id)
        if f['status'] != 'member':
            settings, create = Chat.get_or_create(tg_id=message.chat.id)
            settings.settings = -settings.settings
            settings.save()
            await bot.send_message(message.chat.id,
                             'nsfw режим выключен' if settings.settings == -1 else 'nsfw режим включен')


@dp.message_handler(commands=['sendbd'])
async def process_command_join(message: types.Message):
    db = types.InputFile('users.db')
    await bot.send_document(message.from_user.id, db)
