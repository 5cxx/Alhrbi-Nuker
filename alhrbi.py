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
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc("[+] All channels deleted!")
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
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc("[+] All roles deleted!")
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
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc(f"[+] Created {count} channels!")
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
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc("[+] All channels renamed!")
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
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc("[+] All channels renamed!")
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
    
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc("[+] All messages sent!")
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
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc(f"[+] Banned {len(members)} members!")
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
    await asyncio.gather(*tasks, return_exceptions=True)
    
    printc(f"[+] Kicked {len(members)} members!")
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
    
    await asyncio.gather(*all_tasks, return_exceptions=True)
    
    printc("[+] Nuke completed!")
    
    printc("[+] Creating new channels...")
    channel_names = ["alhrbi", "nuked-by-alhrbi", "alhrbi-was-here", "maybe-alhrbi", "alhrbi-community"]
    
    create_tasks = [fast_create(guild, random.choice(channel_names)) for _ in range(50)]
    await asyncio.gather(*create_tasks, return_exceptions=True)
    
    printc("[+] Server NUKED Successfully!")
    printc("[+] Press Enter to return")
    inp("")

# ==================== MENU ====================
async def main_menu(guild):
    while True:
        print_logo()
        printc(f"Connected Server: {guild.name} (ID: {guild.id})")
        printc("=" * 60)
        printc("[1] Delete All Channels")
        printc("[2] Delete All Roles")
        printc("[3] Create Mass Channels")
        printc("[4] Mass Rename Channels (Random)")
        printc("[5] Mass Rename Channels (Custom)")
        printc("[6] Mass Send Messages")
        printc("[7] Ban All Members")
        printc("[8] Kick All Members")
        printc("[9] NUKE SERVER")
        printc("[0] Exit")
        printc("=" * 60)

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
            input(YELLOW + "\n[!] Press Enter to continue...")
            continue
        
        print()
        printc("1. Bot Token")
        printc("2. User Token (Self-Bot)")
        print()
        choice = inp("[?] Choose: ").strip()
        
        try:
            if choice == "2":
                try:
                    if intents:
                        bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)
                    else:
                        bot = commands.Bot(command_prefix="!", self_bot=True)
                except:
                    bot = commands.Bot(command_prefix="!", self_bot=True)
                
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
                    input(YELLOW + "\n[!] Press Enter to try again...")
                    continue
            
            else:
                try:
                    if intents:
                        bot = commands.Bot(command_prefix="!", intents=intents)
                    else:
                        bot = commands.Bot(command_prefix="!")
                except:
                    bot = commands.Bot(command_prefix="!")
                
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
                    input(YELLOW + "\n[!] Press Enter to try again...")
                    continue
        
        except Exception as e:
            printc(f"[X] Error: {e}")
            input(YELLOW + "\n[!] Press Enter to continue...")
            continue

if __name__ == "__main__":
    try:
        asyncio.run(start())
    except Exception as e:
        print(RED + f"[X] Error: {e}")
        input(YELLOW + "\n[!] Press Enter to exit...")
