from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from bs4 import BeautifulSoup

bot = Bot(token='6911511961:AAH8hB4FQk8iL3sggMVEh3I7MGaL6i-N16A')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=5)
    btns_text = ('Прогноз', 'Погода', 'Карты фактической погоды', 'Карта осадков', 'Качество воздуха')
    keyboard_markup.row(*(types.KeyboardButton(text) for text in btns_text))
    await message.reply("Выберите одну из кнопок:", reply_markup=keyboard_markup)


@dp.message_handler()
async def echo_message(msg: types.Message):
    button_text = msg.text.lower()

    if button_text == 'прогноз':
        url = 'https://yandex.ru/pogoda/kazan?lat=55.783569&lon=49.149578'
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "lxml")
        prognoz = bs.find('div', 'title-icon__text')
        await bot.send_message(msg.from_user.id, prognoz.text)
    elif button_text == 'погода':
        url = 'https://yandex.com.am/weather?lat=55.79612732&lon=49.10641479'
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "lxml")
        temp4 = bs.find('div', 'temp fact__temp fact__temp_size_s')
        temp2 = bs.find('div', 'term term_orient_h fact__feels-like')
        temp3 = bs.find('h1', 'title title_level_1 header-title__title')
        temp5 = bs.find('span', 'wind-speed')
        await bot.send_message(msg.from_user.id,
                               '{0}\n{1} {2}{3}\n{4}{5}\n{6} {7} {8}'.format(temp3.text, str('Температура воздуха:'),
                                                                             temp4.text, str(
                                       '°C,'), temp2.text, str('°C,'), str(
                                       'Скорость ветра:'), temp5.text, str('м/с')))
    elif button_text == 'карты фактической погоды':
        url = "https://meteoinfo.ru/hmc-input/mapsynop/Analiz.png"
        img = requests.get(url)
        img_option = open('synop.png', 'wb')
        img_option.write(img.content)
        await bot.send_photo(msg.from_user.id, open('C://Users//admin//PycharmProjects//project1//synop.png', 'rb'))
    elif button_text == 'карта осадков':
        url = "https://meteoinfo.ru/hmc-input/mapsynop/Precip.png"
        img = requests.get(url)
        img_option = open('osadki.png', 'wb')
        img_option.write(img.content)
        await bot.send_photo(msg.from_user.id, open('C://Users//admin//PycharmProjects//project1//osadki.png', 'rb'))
    elif button_text == 'качество воздуха':
        url = 'https://yandex.ru/pogoda/ru-RU/kazan/pollution?lat=55.783661&lon=49.149731'
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "lxml")
        air = bs.find('h3', 'sc-e482dbd4-2 sc-5b594c7-4 jYHumq eiGpCV')
        air2 = bs.find('p')
        await bot.send_message(msg.from_user.id,
                               '{0} {1}\n{2}'.format(str('Значение показателя загрязнения воздуха в Казани:'), air.text,
                                                     air2.text))


if __name__ == '__main__':
    executor.start_polling(dp)
