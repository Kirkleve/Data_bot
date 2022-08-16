from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler
import logging
from DataBase import *

db = None
newName = ''
newTel = ''
newCity = ''
personID = ''
id = 0

SELECT, INPUTNAME, INPUTTEL, INPUTCITY, INPUTFILTER, INPUTID, DELETEID = range(7)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def Menu(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Выбирете действие:\n'
        '/show - показать записи\n'
        '/filter - фильтр записей\n'
        '/add - добавить запись\n'
        '/delete - удалить запись\n'
        '/save - сохранить изменения\n'
        '/end - закончить работу'
    )

def Start(update: Update, context: CallbackContext):
    global db
    db = OpenDataBase()
    Menu(update, context)
    return SELECT

def Show(update: Update,context: CallbackContext):
    global db
    data = GetAllPersons(db)
    message = '\n'.join(
        [f'{i[0]},{i[1]},{i[2]},{i[3]}' for i in data])
    update.message.reply_text(message)
    Menu(update, context)
    return SELECT

def AddItem(update: Update,context: CallbackContext):
    update.message.reply_text('Введите имя или /end для отмены')
    return INPUTNAME

def AddName(update: Update,context:CallbackContext):
    global newTel
    text = update.message.text
    newTel = text
    update.message.reply_text('Введите номер телефона или /end для отмены')
    return INPUTTEL

def AddTel(update:Update, context: CallbackContext):
    global newCity
    text = update.message.text
    newCity = text
    update.message.reply_text('Введите город проживания или /end для отмены')
    return INPUTCITY

def AddCity(update:Update, context:CallbackContext):
    global newName, newTel, newCity, db
    text = update.message.text
    newCity = text
    AddPerson(db, newName, newTel, newCity)
    logger.info(f'Вы добавили нового человека в список "{newName},{newTel},{newCity}"')
    newName, newTel, newCity = ('', '', '')
    Menu(update, context)
    return SELECT

def Cancel(update:Update,context: CallbackContext):
    logger.info('Вы отменили операцию')
    Menu(update, context)
    return SELECT

def PrintFilter(update: Update, context: CallbackContext):
    logger.info(f'Вы хотите просмотреть базу по фильтру?')
    update.message.reply_text('Введите строку для фильтрации')
    return INPUTFILTER

def InputFilter(update: Update, context: CallbackContext):
    text = update.message.text
    data = GetFilterPerson(db, text)
    if len(data) != 0:
        message = '\n'.join(
            [f'{i[0]},{i[1]},{i[2]},{i[3]}' for i in data])
    else:
        message = 'Нет данных'
    update.message.reply_text(message)
    Menu(update, context)
    return SELECT

def ID_For_Delete (updete: Update, context: CallbackContext):
    logger.info('Вы выбрали удаление')
    updete.message.reply_text('Введите id человека для удаления или /end для отмены')
    return INPUTID

def Delete (update: Update, context: CallbackContext):
    global id
    text = update.message.text
    logger.info(f'Имя для удаления "{text}"')
    try:
        id = int(text)
        person = GetPerson(db, id)
        if person == None:
            raise
    except:
        update.message.reply_text('Неверный id\n'
                                  'Введите id человека для удаления'
                                  'или /end для отмены')
        return INPUTID
    update.message.reply_text(f'{person[0]}, {person[1]}, {person[2]}, {person[3]}, {person[4]}\n'
                              f'Подтвердите удаление командой /delete или /end для отмены')
    return DELETEID

def Del_ID(updete: Update,context: CallbackContext):
    global db, id
    RemovePerson(db, id)
    Menu(updete, context)
    return SELECT

def PrintCity(updete: Update, context: CallbackContext):
    global db
    city = GetAllCity(db)
    if len(city) !=0:
        message = '\n'.join(
            [f'{i[0]}, {i[1]}' for i in city])
    else:
        message = 'Список городов пуст'
    updete.message.reply_text(message)
    Menu(updete, context)
    return SELECT

def Save(update:Update, context:CallbackContext):
    SaveDataBase(db)
    logger.info(f'{update.message.from_user.first_name}, вы сохранили в базу!')
    Menu(update, context)
    return SELECT

def TheEnd(updete:Update, context:CallbackContext):
    updete.message.reply_text('Работа с базой завершена')
    return ConversationHandler.END

def Text(update, context):
    logger.info(f'{update.message.from_user.first_name}, зачем вы ввели это сообщение: \n'
                f'"{update.message.text}"? ')

def Unknown(update, context):
    user = update.message.from_user
    logger.info(
        f"Пользователь {user.first_name} ввел не обработанную комаду '{update.message.text}'")









