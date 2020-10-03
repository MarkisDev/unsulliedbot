"""
Unsullied Bot - A script to automate blog stuff.
This script has the main code for the bot to function
@author : MarkisDev
@copyright : https://markis.dev
"""  
# Importing all the libs needed
from telebot import types, util
import telebot
import time
import validators
from img import *
import os

# Setting our token
TOKEN = 'YOUR_BOT_TOKEN'

# Initializing data for image and setting users
data = {}
# List of users message.chat.id in int or just run /userid to get the value
users = []

# Initializing bot
bot = telebot.TeleBot(TOKEN)

# Command to display help text
@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    bot.send_message(message.chat.id, 
"""
I am meant to be used to make Instagram posts for <a href="https://instagram.com/unsulliedstudios">@unsulliedstudios</a>

Type /help to get a list of all my commands.  

<b><u>COMMANDS</u></b>
/ping - Check if I am alive!
/size - This will fetch image details for the given url.
/quickpost - This will generate the post with recommended values.
/makepost - This will make your instagram post with custom values.
/post - This will generate your post in one line!
/userid - This will give you your userid.
/lovemarkis - This will show Markis some love &lt;3

<b><i>Tell @markisdev you love him, it took him a day to build me!</i></b>
""", parse_mode='HTML')

#
#           QUICK POST SECTION 
#

# Command to initialize step-by-step inputs for quickpost
@bot.message_handler(commands=['quickpost'])
def quickpost(message):
    if message.chat.id in users:
        msg  = bot.send_message(message.chat.id,
"""
You've chosen to make an instagram post. 

<u><b>Please follow the onscreen instructions.</b></u>

Type <b>YES</b> to continue.

<i>Type /cancel at anytime to quit.</i>
""", parse_mode='HTML')
        bot.register_next_step_handler(msg, choose_color_quick)
    else:
        bot.reply_to(message, """<b>You're not part of unsullied!</b>""", parse_mode='HTML')

# Command to take confirmation from user and move to color input (quickpost)
def choose_color_quick(message):
    if message.content_type == 'text':
        if message.text.lower() == "yes"  or message.text.lower() == 'y':
            buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
            btn_orange = types.KeyboardButton("Orange")
            btn_purple = types.KeyboardButton("Purple")
            btn_green = types.KeyboardButton("Green")
            buttons.add(btn_orange, btn_purple, btn_green)
            msg =  bot.send_message(message.chat.id, "Choose the theme color: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_url_quick)
        else:
            bot.reply_to(message, "Okay then, don't waste my time (>.<)")
    else:
        bot.send_message(message.chat.id, """This is <u><b>NOT</b></u> yes! (&gt;.&lt;)""",reply_to_message_id=message.message_id, parse_mode='HTML')

# Command to confirm color and take URL (quickpost)
def choose_url_quick(message):
    if message.content_type == 'text':
        buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        btn_orange = types.KeyboardButton("Orange")
        btn_purple = types.KeyboardButton("Purple")
        btn_green = types.KeyboardButton("Green")
        buttons.add(btn_orange, btn_purple, btn_green)
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.lower() == 'orange':
            data['color'] = 'orange'
        elif message.text.lower() == 'purple':
            data['color'] = 'purple'
        elif message.text.lower() == 'green':
            data['color'] = 'green'
        else:
            bot.send_message(message.chat.id, "Please enter a valid option!")
            msg = bot.send_message(message.chat.id, "Choose the theme color: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_url_quick)
            return
        msg = bot.reply_to(message, "Enter the image URL: ")
        bot.register_next_step_handler(msg, choose_title_quick)
    else:
        bot.send_message(message.chat.id, "Please enter a valid option!")
        msg = bot.send_message(message.chat.id, "Choose the theme color: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_url_quick)
        return

# Command to confirm URL and take title (quickpost)
def choose_title_quick(message):
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if validators.url(message.text):
            image = get_img(message.text)
            if(image['status']):
                data['image'] = image['image']
                bot.send_message(message.chat.id,
f"""

<b>IMAGE FETCHED!</b>

<b>WIDTH:</b> {image['width']}
<b>HEIGHT:</b> {image['height']}

<u><b>RECOMMENDED VALUES</b></u>

<b>WIDTH: 512</b>
<b>HEIGHT: 288</b>

<i>Image size values have to be greater or equal to recommended values. </i>
""", reply_to_message_id=message.message_id, parse_mode='HTML')
                msg =  bot.send_message(message.chat.id, "Enter title: ")
                bot.register_next_step_handler(msg, choose_author_quick)
            else:
               bot.send_message(message.chat.id, "Please enter a valid URL!")
               msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
               bot.register_next_step_handler(msg, choose_title_quick)

        else:
            bot.send_message(message.chat.id, "Please enter a valid URL!")
            msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
            bot.register_next_step_handler(msg, choose_title_quick)
    else:
        bot.send_message(message.chat.id, "Please enter a valid URL!")
        msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
        bot.register_next_step_handler(msg, choose_title_quick)

# Command to confirm title and take author name (quickpost)
def choose_author_quick(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("25")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        btn_1 = "- Joe"
        btn_2 = "- Nidhi"
        btn_3 = "- Snehal"
        btn_4 = "- Sarahfin"
        btn_5 = "- Swapneel"
        btn_6 = "- Dheeraj"
        btn_8 = "- Rushi"
        btn_9 = "- Rijuth"
        buttons.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_8, btn_9)
        data['title_size'] = 25
        data['title'] = message.text
        data['title_x'] = 180
        data['title_y'] = 455
        msg =  bot.send_message(message.chat.id, "Enter author name: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, gen_img_quick)
    else:
        bot.send_message(message.chat.id, "Please enter a valid title!")
        msg =  bot.send_message(message.chat.id, "Enter title: ")
        bot.register_next_step_handler(msg, choose_author_quick)

# Function to confirm author name and send generated image (quickpost)
def gen_img_quick(message):
    buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    btn_1 = "- Joe"
    btn_2 = "- Nidhi"
    btn_3 = "- Snehal"
    btn_4 = "- Sarahfin"
    btn_5 = "- Swapneel"
    btn_6 = "- Dheeraj"
    btn_7 = "- Denin"
    btn_8 = "- Rushi"
    btn_9 = "- Rijuth"
    buttons.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8, btn_9)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        data['author_size'] = 19
        data['author'] = message.text
        data['author_x'] = 488
        data['author_y'] = 526
        data['img_width'] = 390
        data['img_height'] = 200
        data['img_x'] = 185
        data['img_y'] = 225
        data['image'] = resize_img(data['image'], data['img_width'], data['img_height'])
        data['image'] = make_img(data['image'], data['color'], data['img_x'], data['img_y'])
        data['image'] = write_title(data['image'], data['title'], data['title_size'], data['title_x'], data['title_y'])
        data['image'] = write_author(data['image'], data['color'], data['author'], data['author_size'], data['author_x'], data['author_y'])
        saved_img = save_img(data['image'])
        img = upload_img(saved_img['directory'])
        if (img['success'] == True):
            bot.send_message(message.chat.id,
"""
<b>IMAGE GENERATED!</b>
<i>Uploading...</i>
""", parse_mode='HTML')
            bot.send_message(message.chat.id, img['data']['url'])
            os.remove(saved_img['directory'])
        else:
            bot.send_message(message.chat.id, "<b><u>IMAGE WAS NOT UPLOADED!</u></b>", parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "Please enter a valid name")
        msg =  bot.send_message(message.chat.id, "Enter author name: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, gen_img_quick)


#
#           MAKE POST SECTION 
#

# Command to initialize step-by-step inputs for makepost
@bot.message_handler(commands=['makepost'])
def makepost(message):
    if message.chat.id in users:
        msg  = bot.send_message(message.chat.id,
"""
You've chosen to make an instagram post. 

<b> <u> Please follow the onscreen instructions.</u> </b>

Type <b>YES</b> to continue.

<i>Type /cancel at anytime to quit.</i>

""", parse_mode='HTML')
        bot.register_next_step_handler(msg, choose_color)
    else:
        bot.reply_to(message, """<b>You're not part of unsullied!</b>""", parse_mode='HTML')

# Command to take confirmation from user and move to color input (makepost)
def choose_color(message):
    if message.content_type == 'text':
        if message.text.lower() == "yes" or message.text.lower() == 'y':
            buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
            btn_orange = types.KeyboardButton("Orange")
            btn_purple = types.KeyboardButton("Purple")
            btn_green = types.KeyboardButton("Green")
            buttons.add(btn_orange, btn_purple, btn_green)
            msg =  bot.send_message(message.chat.id, "Choose the theme color: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_url)
        else:
            bot.reply_to(message, "Okay then, don't waste my time (>.<)")
    else:
        bot.send_message(message.chat.id, """This is <u><b>NOT</b></u> yes (&gt;.&lt;)""",reply_to_message_id=message.message_id, parse_mode='HTML')


# Command to confirm color and take URL (makepost)
def choose_url(message):
    if message.content_type == 'text':
        buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
        btn_orange = types.KeyboardButton("Orange")
        btn_purple = types.KeyboardButton("Purple")
        btn_green = types.KeyboardButton("Green")
        buttons.add(btn_orange, btn_purple, btn_green)
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.lower() == 'orange':
            data['color'] = 'orange'
        elif message.text.lower() == 'purple':
            data['color'] = 'purple'
        elif message.text.lower() == 'green':
            data['color'] = 'green'
        else:
            bot.send_message(message.chat.id, "Please enter a valid option!")
            msg = bot.send_message(message.chat.id, "Choose the theme color: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_url)
            return
        msg = bot.reply_to(message, "Enter the image URL: ")
        bot.register_next_step_handler(msg, choose_img_width)
    else:
        bot.send_message(message.chat.id, "Please enter a valid option!")
        msg = bot.send_message(message.chat.id, "Choose the theme color: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_url)
        return


# Command to confirm url and take image width (makepost)
def choose_img_width(message):
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if validators.url(message.text):
            image = get_img(message.text)
            if(image['status']):
                data['image'] = image['image']
                bot.send_message(message.chat.id,
f"""

<b>IMAGE FETCHED!</b>

<b>WIDTH:</b> {image['width']}
<b>HEIGHT:</b> {image['height']}

<u><b>RECOMMENDED VALUES</b></u>

<b>WIDTH: 512</b>
<b>HEIGHT: 288</b>

<i>Image size values have to be greater or equal to recommended values. </i>
""", reply_to_message_id=message.message_id, parse_mode='HTML')
                buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
                btn_width = types.KeyboardButton("390")
                buttons.add(btn_width)
                msg =  bot.send_message(message.chat.id, "Enter image width: ", reply_markup=buttons)
                bot.register_next_step_handler(msg, choose_img_height)
            else:
               bot.send_message(message.chat.id, "Please enter a valid URL!")
               msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
               bot.register_next_step_handler(msg, choose_img_width)

        else:
            bot.send_message(message.chat.id, "Please enter a valid URL!")
            msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
            bot.register_next_step_handler(msg, choose_img_width)
    else:
        bot.send_message(message.chat.id, "Please enter a valid URL!")
        msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
        bot.register_next_step_handler(msg, choose_img_width)
            
# Command to confirm image width and take image height (makepost)
def choose_img_height(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_width = types.KeyboardButton("390")
    buttons.add(btn_width)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['img_width'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            btn_height = types.KeyboardButton("200")
            buttons.add(btn_height)
            msg =  bot.send_message(message.chat.id, "Enter image height: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_img_x)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter image width: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_img_height)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter image width: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_img_height)

# Command to confirm height and take image x-coordinate (makepost)
def choose_img_x(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_height = types.KeyboardButton("200")
    buttons.add(btn_height)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['img_height'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            btn_x = types.KeyboardButton("185")
            buttons.add(btn_x)
            msg =  bot.send_message(message.chat.id, "Enter image x-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_img_y)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter image height: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_img_x)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter image height: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_img_x)

# Command to confirm image x-coordinate and take image y-coordinate (makepost)
def choose_img_y(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("185")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['img_x'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            btn_y = types.KeyboardButton("225")
            buttons.add(btn_y)
            msg =  bot.send_message(message.chat.id, "Enter image y-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_title)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter image x-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_img_y)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter image x-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_img_y)

# Command to confirm image y-coordinate and take title (makepost)
def choose_title(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("225")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['img_y'] = int(message.text)
            msg =  bot.send_message(message.chat.id, "Enter title: ")
            bot.register_next_step_handler(msg, choose_title_x)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter image y-coordinate ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_title)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter image y-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_title)

# Command to confirm title and take title x-coordinate (makepost)
def choose_title_x(message):
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        data['title'] = message.text
        buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        btn_x = types.KeyboardButton("180")
        buttons.add(btn_x)
        msg =  bot.send_message(message.chat.id, "Enter title x-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_title_y)
    else:
        bot.send_message(message.chat.id, "Please enter a valid title!")
        msg =  bot.send_message(message.chat.id, "Enter title: ")
        bot.register_next_step_handler(msg, choose_title_x)


# Command to confirm title x-coordinate and take title y-coordinate (makepost)
def choose_title_y(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("180")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['title_x'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            btn_y = types.KeyboardButton("455")
            buttons.add(btn_y)
            msg =  bot.send_message(message.chat.id, "Enter title y-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_title_size)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter title x-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_title_y)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter title x-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_title_y)

# Command to confirm title y-coordinate and take title fontsize (makepost)
def choose_title_size(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("455")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['title_y'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            btn_size = types.KeyboardButton("25")
            buttons.add(btn_size)
            msg =  bot.send_message(message.chat.id, "Enter title font size: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_author)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter title y-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_title_size)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter title y-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_title_size)

# Command to confirm title font size and take author name (makepost)
def choose_author(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("25")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['title_size'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
            btn_1 = "- Joe"
            btn_2 = "- Nidhi"
            btn_3 = "- Snehal"
            btn_4 = "- Sarahfin"
            btn_5 = "- Swapneel"
            btn_6 = "- Dheeraj"
            btn_7 = "- Denin"
            btn_8 = "- Rushi"
            btn_9 = "- Rijuth"
            buttons.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8, btn_9)
            data['title_font'] = int(message.text)
            msg =  bot.send_message(message.chat.id, "Enter author name: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_author_x)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter title font size: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_author)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter title font size: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_author)

# Command to confirm author name and take author x-coordinate (makepost)
def choose_author_x(message):
    buttons = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    btn_1 = "- Joe"
    btn_2 = "- Nidhi"
    btn_3 = "- Snehal"
    btn_4 = "- Sarahfin"
    btn_5 = "- Swapneel"
    btn_6 = "- Dheeraj"
    btn_8 = "- Rushi"
    btn_9 = "- Rijuth"
    buttons.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_8, btn_9)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        data['author'] = message.text
        buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        btn_x = types.KeyboardButton("488")
        buttons.add(btn_x)
        msg =  bot.send_message(message.chat.id, "Enter author x-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_author_y)
    else:
        bot.send_message(message.chat.id, "Please enter a valid name!")
        msg =  bot.send_message(message.chat.id, "Enter author name: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_author_x)

# Command to confirm author x-coordinate and take author y-coordinate (makepost)
def choose_author_y(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("488")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['author_x'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            btn_y = types.KeyboardButton("526")
            buttons.add(btn_y)
            msg =  bot.send_message(message.chat.id, "Enter author y-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_author_size)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter author x-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_author_y)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter author x-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_author_y)

# Command to confirm author y-coordinate and take author font size (makepost)
def choose_author_size(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("526")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['author_y'] = int(message.text)
            buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            btn_size = types.KeyboardButton("19")
            buttons.add(btn_size)
            msg =  bot.send_message(message.chat.id, "Enter author font size: ", reply_markup=buttons)
            bot.register_next_step_handler(message, gen_img)
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter author y-coordinate: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, choose_author_size)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter author y-coordinate: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, choose_author_size)

# Function to confirm author font size and send generated image (makepost)
def gen_img(message):
    buttons = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    btn_y = types.KeyboardButton("19")
    buttons.add(btn_y)
    if message.content_type == 'text':
        if util.is_command(message.text) and util.extract_command(message.text) in commands.keys():
            command_send(util.extract_command(message.text), message)
            return
        if message.text.isdigit():
            data['author_size'] = int(message.text)
            data['image'] = resize_img(data['image'], data['img_width'], data['img_height'])
            data['image'] = make_img(data['image'], data['color'], data['img_x'], data['img_y'])
            data['image'] = write_title(data['image'], data['title'], data['title_size'], data['title_x'], data['title_y'])
            data['image'] = write_author(data['image'], data['color'], data['author'], data['author_size'], data['author_x'], data['author_y'])
            saved_img = save_img(data['image'])
            img = upload_img(saved_img['directory'])
            if (img['success'] == True):
                bot.send_message(message.chat.id,
"""
<b>IMAGE GENERATED!</b>
<i>Uploading...</i>
""", parse_mode='HTML')
                bot.send_message(message.chat.id, img['data']['url'])
                os.remove(saved_img['directory'])
            else:
                bot.send_message(message.chat.id, "<b><u>IMAGE WAS NOT UPLOADED!</u></b>", parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "Please enter a valid number!")
            msg =  bot.send_message(message.chat.id, "Enter author font size: ", reply_markup=buttons)
            bot.register_next_step_handler(msg, gen_img)
    else:
        bot.send_message(message.chat.id, "Please enter a valid number!")
        msg =  bot.send_message(message.chat.id, "Enter author font size: ", reply_markup=buttons)
        bot.register_next_step_handler(msg, gen_img)

# Command to make a very quick post [LINUX STYLE PARAMETERS]
@bot.message_handler(commands=['post'])
def poster(message):
    if message.chat.id in users:
        if util.is_command(message.text) and util.extract_arguments(message.text) == 'help':
            bot.send_message(message.chat.id,
"""

<u><b> PARAMETERS</b></u>

<b>Color : -c</b>

<b>Image URL  : -u</b>
<b>Image Width : -iw</b>
<b>Image Height : -ih</b>
<b>Image x-coordinate : -ix</b>
<b>Image y-coordinate : -iy</b>

<b>Author Name : -a</b>
<b>Author Size : -as</b>
<b>Author x-coordinate : -ax</b>
<b>Author y-coordinate : -ay</b>

<b>Title Name : -t</b>
<b>Title Size : -ts</b>
<b>Title x-coordinate : -tx</b>
<b>Title y-coordinate : -ty</b>

""", reply_to_message_id=message.message_id, parse_mode='HTML')
            bot.send_message(message.chat.id,
"""

<u><b>EXAMPLE</b></u>

/post -c orange -u https://unsullied.xyz/img/logo/meta.png -iw 390 -ih 200 -ix 185 -iy 225 -t "Testing is fun." -ts 25 -tx 180 -ty 455 -a "- Sarahfin" -as 19 -ax 488 -ay 526
""", reply_to_message_id=message.message_id, parse_mode='HTML')
            return
        try:
            param = message.text.split(' ')
            if validators.url(param[param.index('-u')+1]):
                image = get_img(param[param.index('-u')+1])
                if(image['status']):
                    data['image'] =  image['image']
                    bot.send_message(message.chat.id,
f"""

<b>IMAGE FETCHED!</b>

<b>WIDTH:</b> {image['width']}
<b>HEIGHT:</b> {image['height']}

<u><b>RECOMMENDED VALUES</b></u>

<b>WIDTH: 512</b>
<b>HEIGHT: 288</b>

<i>Image size values have to be greater or equal to recommended values. </i>
""", reply_to_message_id=message.message_id, parse_mode='HTML')
                    title = message.text[message.text.find('-t'):len(message.text)-1].replace('-t ', '')
                    data['title']  = ''
                    for i in range(1,len(title)-1):
                        if title[i] == '"':
                            break
                        data['title'] = data['title'] + title[i]
                    data['title_size'] = int(param[param.index('-ts')+1])
                    author = message.text[message.text.find('-a'):len(message.text)-1].replace('-a ', '')
                    data['author']  = ''
                    
                    for i in range(1,len(author)-1):
                        if author[i] == '"':
                            break
                        data['author'] = data['author'] + author[i]
                    data['author_size'] = int(param[param.index('-as')+1])
                    data['img_x'] = int(param[param.index('-ix')+1])
                    data['img_y'] = int(param[param.index('-iy')+1])
                    data['img_width'] = int(param[param.index('-iw')+1])
                    data['img_height'] = int(param[param.index('-ih')+1])
                    data['author_x'] = int(param[param.index('-ax')+1])
                    data['author_y'] = int(param[param.index('-ay')+1])
                    data['title_x'] = int(param[param.index('-tx')+1])
                    data['title_y'] = int(param[param.index('-ty')+1])
                    data['color'] = param[param.index('-c')+1].lower()
                    data['image'] = resize_img(data['image'], data['img_width'], data['img_height'])
                    data['image'] = make_img(data['image'], data['color'], data['img_x'], data['img_y'])
                    data['image'] = write_title(data['image'], data['title'], data['title_size'], data['title_x'], data['title_y'])
                    data['image'] = write_author(data['image'], data['color'], data['author'], data['author_size'], data['author_x'], data['author_y'])
                    saved_img = save_img(data['image'])
                    img = upload_img(saved_img['directory'])
                    if (img['success'] == True):

                        bot.send_message(message.chat.id,
"""
<b>IMAGE GENERATED!</b>
<i>Uploading...</i>
""", parse_mode='HTML')
                        bot.send_message(message.chat.id, img['data']['url'])
                        os.remove(saved_img['directory'])
                    else:
                        bot.send_message(message.chat.id, "<b><u>IMAGE WAS NOT UPLOADED!</u></b>", parse_mode="HTML")
                else:
                    bot.send_message(message.chat.id, "Please enter a valid URL!")
                    msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
                    bot.register_next_step_handler(msg, choose_img_width)
            else:
                bot.send_message(message.chat.id, "Please enter a valid URL!")
                msg =  bot.send_message(message.chat.id, "Enter the image URL: ")
                bot.register_next_step_handler(msg, choose_img_width)
        except Exception as e:
            bot.send_message(message.chat.id,
f"""
<b>INVALID COMMAND!</b>

Run <code>/post help</code> to get the list of accepted arguments
<b>Error : {e}</b>
""", parse_mode='HTML')
    else:
        bot.reply_to(message, """<b>You're not part of unsullied!</b>""", parse_mode='HTML')

# Command to show user's unique chat id
@bot.message_handler(commands=['userid'])
def userid(message):
    bot.send_message(message.chat.id, f"Your user id: <b>{message.chat.id}</b>", parse_mode='HTML' )

# Command to retrieve image details from a valid URL
@bot.message_handler(commands=['size'])
def size(message):
    if message.content_type == 'text':
        url = util.extract_arguments(message.text)
        if url!=None or url == '':
            if validators.url(url):
                image = get_img(url)
                bot.send_message(message.chat.id, """<b><i>Fetching image details...</i></b>""", parse_mode='HTML', reply_to_message_id=message.message_id)
                if image['status']:
                    bot.send_message(message.chat.id,
f"""

<u><b>IMAGE DETAILS</b></u>

<b>WIDTH:  {image['width']}</b>
<b>HEIGHT: {image['height']}</b>

<u><b>RECOMMENDED VALUES</b></u>

<b>WIDTH: 512</b>
<b>HEIGHT: 288</b>

<i>Image size values have to be greater or equal to recommended values. </i>
""", parse_mode='HTML'
)
                else:
                    m = bot.reply_to(message, "Please enter a valid URL")
                    bot.register_next_step_handler(m, size)
            else:
                msg = bot.reply_to(message, "Please enter a valid URL!")
                m = bot.send_message(msg.chat.id, """<b><u>Example: </u></b> <b>/size https://unsullied.xyz/img/logo/meta.png</b>""", parse_mode='HTML', reply_to_message_id=message.message_id)
                bot.register_next_step_handler(m, size)
        else:
            msg = bot.reply_to(message, "URL missing!")
            m = bot.send_message(msg.chat.id, """Example : <b>/size https://unsullied.xyz/img/logo/meta.png</b>""", parse_mode='HTML', reply_to_message_id=message.message_id)
            bot.register_next_step_handler(m, size)
    else:
        m = bot.reply_to(message, "Enter a valid URL!")
        bot.register_next_step_handler(m, size)

# Command to cancel / quit "step-by-step" proces
def quitter(message):
    bot.send_message(message.chat.id, """<b>You've exited the process!</b>""", reply_to_message_id=message.message_id, parse_mode='HTML')

# Command to just show me some love cause I'm narsisstic :P
@bot.message_handler(commands=['lovemarkis'])
def lovemarkis(message):
    bot.send_message(message.chat.id, 
"""
<b>Awww, you love Markis?</b>

I'll tell him you love him, I promise.

But, guess what? 
<b>He loves you too!</b>

Here's a cookie &#127850;

""", reply_to_message_id=message.message_id, parse_mode='HTML')
    bot.send_message(1100994385, 
f"""
Hey Markis, 
<b>@{message.from_user.username} - {message.from_user.first_name} {message.from_user.last_name}</b>
<b>Chat ID : {message.chat.id}</b>
Wanted you to know that they love you. 
I'm not your emotional support bot, but I gave them a cookie (&gt;.&lt;)
""", parse_mode='HTML')

# Command to quit while a "step by step" command is in process
def command_send(command, message):
    bot.send_message(message.chat.id, """<b>Quiting..</b>""", parse_mode='HTML')
    commands.get(command)(message)

# Command to check if bot is alive
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id,
f"""
<b> I am alive and kicking!</b>
""", parse_mode='HTML')

# Defining all the functions in the commands dictionary
commands = {
    'help': send_help,
    'start':send_help,
    'quit': quitter,
    'cancel':quitter,
    'userid':userid,
    'size':size,
    'lovemarkis':lovemarkis,
    'makepost': makepost,
    'post':poster,
    'ping':ping
    }


# Starting our bot and making it run even if connection is closed
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(3)
