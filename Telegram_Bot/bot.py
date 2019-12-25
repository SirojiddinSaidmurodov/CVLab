#!/usr/bin/env python
import telebot
import cv2 as cv

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.reply_to(message,
                          "Отправляйте фото и получайте раскраски. /start для запуска бота, /help чтобы увидеть это сообщение")


@bot.message_handler(content_types='photo')
def imageHandler(message):
    local_image = imageExtractor(message)
    processed_image = imageToColoring(local_image)
    cv.imwrite('image.jpg', processed_image)
    bot.send_photo(message.chat.id, open("image.jpg", 'rb'))


def imageExtractor(photo_message):
    received_file_info = bot.get_file(photo_message.photo[-1].file_id)
    image_file = bot.download_file(received_file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(image_file)
    return cv.imread("image.jpg")


def imageToColoring(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 127, 255, 0)
    # ret, thresh = cv.threshold(gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_TC89_KCOS)
    img[:, :] = (255, 255, 255)
    cv.drawContours(img, contours, -1, (0, 0, 0), 2)
    return img


bot.polling(60)  # for avoiding timeout errors
