import asyncio
import os
import subprocess

from aiogram.utils import executor
from django.core.management.base import BaseCommand

from telegram_bots.bot import start_bot_under_dj


class Command(BaseCommand):
    help = 'start bot'

    def handle(self, *args, **kwargs):
        start_bot_under_dj()