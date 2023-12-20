import xlsxwriter

workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, 'Дата')
worksheet.write(0, 1, 'Время')
worksheet.write(0, 2, 'Вид соообщения')
worksheet.write(0, 3, 'Отправитель')
worksheet.write(0, 4, 'ID отправителя')
worksheet.write(0, 5, 'Сообщение и id стикера')
worksheet.write(0, 6, 'Эмоция стикера')


workbook.close()
