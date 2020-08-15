import asyncio
import concurrent.futures
import os
import time
from pprint import pprint

import aiohttp
import alpaca_trade_api as tradeapi
import discord
from discord import Webhook, RequestsWebhookAdapter
from apscheduler.schedulers.blocking import BlockingScheduler
from discord.ext import commands
from dotenv import load_dotenv

import marketAPI as api

load_dotenv()
hook_id = os.getenv('DANK_HOOK_ID')
hook_token = os.getenv('DANK_HOOK_TOKEN')

# hook_id = os.getenv('TEST_ID')
# hook_token = os.getenv('TEST_TOKEN')

sched = BlockingScheduler()

# reads a list of tickers from a file and scans for 9ers on the daily timeframe
@sched.scheduled_job('cron', day_of_week='mon-fri', hour='18')
def scanDaily():
    out = "```\n"

    with open("tickers.txt") as f:
        for line in f:
            out += api.scanTicker(line.strip(), "day")

    if len(out) > 5:
        out += "```"
        webhook = Webhook.partial(hook_id, hook_token, adapter=RequestsWebhookAdapter())
        webhook.send(out, username="Daily9er")

sched.start()