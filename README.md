# telegram_bot_bahinsta
It's a telegram bot that downloads instagram photos and videos. 
You can find it in telegram as @bahinsta.

To download from private accounts you need to sign in. To do this use /login username password. 
Otherwise you will be able to download only public photos and videos. 
To download just send to the bot the url of instagram photo or video and wait for response.
Have fun!

# P.S.
The program uses the python library "requests" and telegram API.
As you can guess, file "bot.py" represents the actions of our bot. 
It imports module "instagram_file_downloader", but you can also use file "instagram_file_downloader.py" as self working script that downloads instagram files directly to your machine if you run function "download_content(login_post, url)", where login_post = {'username': 'your_username', 'password': 'your_password'} or simply {} if you don't want to sign in.
