from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler, CallbackQueryHandler
from Command import *
from Token import TOKEN


updater = Updater(TOKEN())


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', Start)],
    states={
        SELECT: [CommandHandler('show', Show),
                 CommandHandler('add', AddCity),
                 CommandHandler('filter', PrintFilter),
                 CommandHandler('delete', Delete),
                 CommandHandler('city', AddCity),
                 CommandHandler('save', Save)
                 ],

        # Add State
        INPUTNAME: [MessageHandler(Filters.text & ~Filters.command, AddItem),
                    CommandHandler('cancel', Cancel)],
        INPUTTEL: [MessageHandler(Filters.text & ~Filters.command, AddName),
                   CommandHandler('cancel', Cancel)],
        INPUTCITY: [MessageHandler(Filters.text & ~Filters.command, AddTel),
                   CommandHandler('cancel', Cancel)],

        # Filter State
        INPUTFILTER: [MessageHandler(Filters.text & ~Filters.command, InputFilter),
                      CommandHandler('cancel', Cancel)],

        # Remove State
        DELETEID: [MessageHandler(Filters.text & ~Filters.command, Delete),
                  CommandHandler('cancel', Cancel)],
    },
    fallbacks=[CommandHandler('exit', TheEnd)],
)

updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(MessageHandler(Filters.command, Unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, Text))

print("Бот запущен.")
updater.start_polling()
updater.idle()