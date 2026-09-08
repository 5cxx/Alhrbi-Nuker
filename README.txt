=========================================
          Alhrbi Tool - Readme
=========================================

Requirements:

* Windows 10 / 11
* Python 3.10 - 3.13
* discord.py-self (for Self-Bot - Recommended)
* colorama
* aiohttp


How to Install:

1. Install Python from:
   https://python.org/downloads
   
   Recommended: Python 3.10 or 3.11
   Python 3.13 works but may have issues

2. Run setup.bat:
   Just double-click setup.bat
   - Choose [1] for Self-Bot (User Token) - Recommended
   - Choose [2] for Bot Token

   Or install manually via CMD:
   
   For Self-Bot (Recommended):
   pip uninstall discord.py discord discord.py-self -y
   pip install discord.py-self --force-reinstall --no-cache-dir
   pip install colorama
   pip install aiohttp

   For Bot Token:
   pip uninstall discord.py discord discord.py-self -y
   pip install discord.py==2.3.2 --force-reinstall --no-cache-dir
   pip install colorama
   pip install aiohttp

3. Make sure the script file is named:
   alhrbi.py
   (No spaces in the name)

4. Run the tool:
   Double-click run.bat
   Or type in CMD: python alhrbi.py


How to Use:

1. Enter your Token
2. Enter the Guild ID (Server ID)
3. Choose token type:
   [1] Bot Token
   [2] User Token (Self-Bot) - Recommended
4. Select an option from the menu
5. Type alhrbi for hidden art/nuke


How to Get User Token (Self-Bot):

1. Open Discord in browser (Chrome/Edge)
2. Press F12 (Developer Tools)
3. Go to Console tab
4. Paste this and press Enter:

   (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c)}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()

5. Copy the token that appears
6. Paste it in the tool


How to Get Guild ID (Server ID):

1. Open Discord Settings
2. Go to Advanced
3. Enable Developer Mode
4. Right-click on the server
5. Click "Copy Server ID"


Menu Options:

[1] Delete All Channels - Deletes every channel instantly
[2] Delete All Roles - Deletes every role instantly
[3] Create Mass Channels - Creates many channels at once
[4] Mass Rename Channels (Random) - Renames all channels randomly
[5] Mass Rename Channels (Custom) - Rename with your own names
[6] Mass Send Messages - Spam messages to all channels
[7] Ban All Members - Bans everyone instantly
[8] Kick All Members - Kicks everyone instantly
[9] NUKE SERVER - Full nuke (delete everything + ban all)
[0] Exit - Close the tool
alhrbi - Hidden art display


Important Notes:

- For Self-Bot: Your account needs admin permissions in the server
- For Bot Token: Bot needs Administrator permission
- All operations are FAST (no delay between actions)
- Press ENTER during operations to cancel (if available)
- Program won't close on error, press Enter to continue


Troubleshooting:

1. "No module named discord":
   Run: pip install discord.py-self --force-reinstall --no-cache-dir

2. "No module named colorama":
   Run: pip install colorama

3. "No module named aiohttp":
   Run: pip install aiohttp

4. "Intents attribute error":
   The script handles this automatically
   No action needed

5. "Connection failed":
   - Token is wrong or expired
   - Get a new token
   - Check internet connection
   - Try different token type

6. "Guild not found":
   - Wrong Guild ID
   - Your account/bot is not in that server
   - Make sure you copied the correct ID

7. Program opens and closes immediately:
   - Run from CMD to see error: python alhrbi.py
   - Check if file name is alhrbi.py
   - Run setup.bat first


WARNING:

- Self-Bot is against Discord ToS
- Your account may get banned
- Use a secondary account only
- Use at your own risk
- Developer is not responsible for banned accounts


Developer Info:

Owner: MaybeRayan
Contact: mayberayanalhrbi
Discord: mayberayanalhrbi
=========================================
