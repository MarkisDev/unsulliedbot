# Unsullied Bot - A bot used by [Unsullied blog](https://blog.unsullied.xyz)
## What is this?
The [blog](https://blog.unsullied.xyz) at Unsullied required the GFX artist to make an [Instagram](https://instagram.com/unsulliedstudios)
version of the post from a template pretty much everyday.  
So I did what any sane coder would do, decided to automate it.

## How does this work?
So the bot is pretty straightforward. It's a Telegram based bot. It uses [pyTelegramBotApi](https://github.com/eternnoir/pyTelegramBotAPI) to send and recieve requests from Telegram API.  
The idea is, you send an image link and it shall save the image from the link and paste it onto the template (using pillow), with the values either fed manually or using the recommended values. This image is then saved and uploaded to imgBB with an expiration date of 3 days, and the link is sent to the user.  

This was made to automate the tedious task of having the GFX artist make the post, almost everyday. Also, this makes it easier for anyone in the team to use the bot so nobody has to rely on a single person.

## How do I self-host this?
Okay, so for obvious reasons I've removed my telegram bot token and my imgBB token.  
- Install the requirements by running `pip install -r requirements.txt` in a terminal window, at the root of the folder.
- You can generate a token for your bot following [this article](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token).  
- Once you have your bot token edit ``main.py`` and copy paste your token there.
- After that, generate an API key at [imgBB]https://api.imgbb.com/).
- Edit ``img.py`` and copy paste the API key there.
- There you go! You're done. You can now run the script by typing `python main.py` in a terminal window, at the root of the folder.

Accoring to the script, there are three templates : `orange.png`, `purple.png`, `green.png`.  
If you're self hosting this for whatever reason, make sure you change the code in `img.py` and add the template image in `img` folder.

_I have removed the template used by [Unsullied Studios](https://instagram.com/unsulliedstudios) because I don't want anyone replicating fake posts._

## Who made this?
Hello there,  
I am [MarkisDev.](https://markis.dev)  
I build whatever interests me, feel free to join my [Discord server](https://join.markis.dev)

_I apologize in advance because this code isn't as efficient as I'd like it to be. I made this mostly for personal use, and was honestly just messing around with Telegram API for the first time_
