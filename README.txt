=========================================
          Alhrbi Tool - Readme
=========================================

Requirements:

* Windows 10 / 11
* Python 3.10 - 3.11 (Recommended)
* discord.py-self (for Self-Bot support)
* discord.py (for Bot support)
* colorama
* aiohttp


How to Install:

1. Install Python 3.10 or 3.11:
   https://python.org/downloads
   NOTE: Python 3.12+ may cause issues (Recommended: Python 3.10)

2. Run setup.bat to install required packages:
   Just double-click setup.bat

   Or install manually via CMD:
   pip uninstall discord.py discord discord.py-self -y
   pip install discord.py-self
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
- If you encounter "ModuleNotFoundError: No module named 'cgi'":
  * Install Python 3.10 or 3.11 instead of Python 3.12+
  * Or run: pip install discord.py-self --upgrade
- If you get "AttributeError: module 'discord' has no attribute 'Intents'":
  * Run: pip uninstall discord.py discord discord.py-self -y
  * Then: pip install discord.py-self


WARNING:

- Using Self-Bot (User Token) is against Discord ToS
- Your account may get banned
- Use a secondary account for Self-Bot
- Bot Token is safer than User Token
- Use at your own risk


Developer Info:

Owner: MaybeRayan
Contact: mayberayanalhrbi
=========================================
