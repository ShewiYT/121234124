import subprocess
import logging
from Worker.config import *
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

subprocess.Popen('python Worker/bot.py')
subprocess.Popen('python ArbitrageBot/bot.py')
subprocess.Popen('python Casino/bot.py')
subprocess.Popen('python Trade/bot.py')

logging.basicConfig(level=logging.INFO)