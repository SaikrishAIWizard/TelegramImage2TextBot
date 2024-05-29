from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import urllib.request
from io import BytesIO
import easyocr

TOKEN: Final = '6948285195:AAH2hyqBavpyaxo_RDlr8V3x6spsGy1NzAM'
BOT_USERNAME: Final = 'magi_magi_bot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting i am magiii!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('i am magiii! please type someting so i can respond!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')

# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    elif 'how are you' in processed:
        return 'I am good!'
    elif 'i love python' in processed:
        return 'Remember me'
    else:
        return 'I dont understand what you wrote...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}:"{text}"')


    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('Bot:', response)
    await  update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')


async def handle_image(update, context):
    # Check if the message contains an image
    if update.message.photo:
        # Get the file ID of the largest available image
        file_id = update.message.photo[-1].file_id
        # Get the file object from the file ID
        file = await context.bot.get_file(file_id)

        # Get the file path
        file_path = file.file_path
        print(file_path)
        # Download the file content
        #file_content = await download_file(file_path)
        #file_content = await download_file(context.bot.token, file_path)

        # Process the image
        #print(file_content)
        #image = Image.open(io.BytesIO(file_content))
        urllib.request.urlretrieve(file_path,"gfg.jpg")
        image = Image.open("gfg.jpg")
        image.show()
        # You can perform any image processing here
        # For example, you can resize the image
        resized_image = image.resize((200, 200))
        resized_image.show()

        # Save the resized image to a BytesIO buffer
        output_buffer = BytesIO()
        resized_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        # Send the processed image back to the user
        await update.message.reply_photo(photo=output_buffer)
    else:
        await update.message.reply_text("Please send me an image.")


if __name__ == '__main__':
    print("starting bot......")
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Images
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    #Errors
    app.add_error_handler(error)

    # Polls the bot
    print('polling')
    app.run_polling(poll_interval=3)