# Discord 2.0
Discord seen through the eyes of a bot

### This project was developed as a experiment only, not as a way to abuse the discord API.
### This project is not finished and may have some bugs and security holes

The project consists of a bot that uses the discord API to send information to a second program, which will show it in a Discord-like UI, being possible to read and send messages in text channels.

The PyQt6 library was used together with the Qt Designer to create the UI, the communication between the 2 files is done by a local server

![image](https://user-images.githubusercontent.com/94933775/153419030-57009821-8d7e-4e66-bfc8-c8b655553c60.png)

To run the program, you must first create a bot: https://discord.com/developers/applications  
Then insert the Token in the last line of the bot_main.py  
Run this same file and wait for the message "Bot ready!" and then run the bot_ui_main.py file.  
Press the "get servers" button to get the list of servers where the bot can see.  
Click on the server where you want see the list of channels and members, select a text channel and the chat will appear.  
To reload the channel click on the text channel again.
