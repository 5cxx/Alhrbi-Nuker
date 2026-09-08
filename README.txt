=========================================
          Alhrbi Tool - Readme
=========================================

Requirements:

* Windows 10 / 11
* Python 3.10 - 3.13
* discord.py or discord.py-self
* colorama
* aiohttp


How to Install:

1. Install Python from:
   https://python.org/downloads
   
   NOTE: If you get "Intents" error, use discord.py instead of discord.py-self

2. Run setup.bat to install required packages:
   Just double-click setup.bat

   Or install manually via CMD:
   
   For Self-Bot (User Token):
   pip uninstall discord.py discord discord.py-self -y
   pip install discord.py-self
   pip install colorama
   pip install aiohttp

   For Bot Token:
   pip uninstall discord.py discord discord.py-self -y
   pip install discord.py==2.3.2
   pip install colorama
   pip install aiohttp

3. Rename the script file:
   From: "Alhrbi Nuker.py"
   To: alhrbi.py
   (Remove spaces to avoid errors)

4. Run the tool:
   Double-click run.bat
   Or type in CMD: python alhrbi.py


How to Use:

1. Enter your Token (Bot Token or User Token)
2. Enter the Guild ID (Server ID)
3. Choose token type:
   [1] Bot Token
   [2] User Token (Self-Bot)
4. Select an option from the main menu
5. Type alhrbi to trigger the hidden option


How to Get User Token (Self-Bot):

1. Open Discord in your browser (Chrome/Edge)
2. Press F12 to open Developer Tools
3. Go to Console tab
4. Paste this code and press Enter:
   
   (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c)}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()

5. Copy the token that appears


How to Get Guild ID (Server ID):

1. Open Discord Settings
2. Go to Advanced
3. Enable Developer Mode
4. Right-click on the server
5. Copy Server ID


Menu Options:

[1] Delete All Channels
[2] Delete All Roles
[3] Mass Create Channels
[4] Mass Rename Channels (Random)
[5] Mass Rename Channels (Custom Name)
[6] Mass Send Messages to All Channels
[7] Ban All Members
[8] Kick All Members
[9] NUKE SERVER
[0] Exit
alhrbi - Hidden Art / Full Nuke Command


Important Notes:

- For Bot Token: The bot MUST have Administrator permissions
- For User Token (Self-Bot): Your account must have admin permissions
- Press ENTER during heavy operations to cancel the task
- The program will not close on error, press Enter to continue
- If you get "AttributeError: module 'discord' has no attribute 'Intents'":
  * Run: pip uninstall discord.py discord discord.py-self -y
  * Then: pip install discord.py==2.3.2
  * This happens with discord.py-self on some Python versions
- If you get "Connection failed" error:
  * Make sure your token is correct
  * Make sure you have internet connection
  * Try getting a new token
- If you get "Guild not found":
  * Make sure you entered the correct Guild ID
  * Make sure your account/bot is in that server
  * For User Token: You must be a member of the server
  * For Bot Token: The bot must be added to the server


WARNING:

- Using Self-Bot (User Token) is against Discord ToS
- Your account may get banned
- Use a secondary account for Self-Bot
- Bot Token is safer than User Token
- Use at your own risk
- The developer is not responsible for any banned accounts


Troubleshooting:

1. "No module named discord":
   Run: pip install discord.py==2.3.2

2. "No module named colorama":
   Run: pip install colorama

3. "No module named aiohttp":
   Run: pip install aiohttp

4. "Intents attribute error":
   Run: pip uninstall discord.py discord discord.py-self -y
   Then: pip install discord.py==2.3.2

5. "Connection failed":
   - Check your token
   - Try a different token type
   - Check your internet

6. "Guild not found":
   - Check the Guild ID
   - Make sure you're in the server
   - For bot: add bot to the server first


Developer Info:

Owner: MaybeRayan
Contact: mayberayanalhrbi
Discord: mayberayanalhrbi
=========================================
