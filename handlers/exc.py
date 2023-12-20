from aiogram import types, Dispatcher
from create_bot import dp
import xlsxwriter
import datetime as dt

count = 1
workbook = xlsxwriter.Workbook('messages.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'Дата')
worksheet.write(0, 1, 'Время')
worksheet.write(0, 2, 'Вид соообщения')
worksheet.write(0, 3, 'Отправитель')
worksheet.write(0, 4, 'ID отправителя')
worksheet.write(0, 5, 'Сообщение и id стикера')
worksheet.write(0, 6, 'Эмоция стикера')


@dp.message_handler(content_types=['text'])
async def send_text(message: types.Message):
    print(message)
    global count
    if message.content_type == 'text':
        if message.text != 'стоп':
            worksheet.write(count, 0, str(dt.datetime.now().date()))
            worksheet.write(count, 1, str(dt.datetime.now().time()))
            worksheet.write(count, 2, 'текст')
            worksheet.write(count, 3, message.from_user.first_name)
            worksheet.write(count, 4, message.from_user.id)
            worksheet.write(count, 5, message.text)
            count += 1


workbook.close()
print('success')


def register_handlers_exc(dp: Dispatcher):
    dp.register_message_handler(send_text)


if __name__ == '__main__':
    executor.start_polling(dp)

