"""Main executable file of CD_MBot"""

import os
import json

from aiogram import executor

from src.bot import MBot
from background import keep_alive

token = open(os.path.join(os.path.dirname(__file__), 'conf', 'prod_token.conf')).readline()
conf = json.load(open(os.path.join(os.path.dirname(__file__), 'conf', 'conf.json'), 'r', encoding='utf-8'))

if not conf['YDL']['cachedir'] or\
   not conf['YDL']['outtmpl'] or\
   not conf['Logger']['logdir']:

    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    log_dir = os.path.join(os.path.dirname(__file__), 'log')
    out_tmpl = os.path.join(cache_dir, '%(title)s.%(ext)s')
    conf['YDL']['cachedir'] = cache_dir
    conf['YDL']['outtmpl'] = out_tmpl
    conf['Logger']['logdir'] = log_dir
    json.dump(conf,
              open(os.path.join(os.path.dirname(__file__), 'conf', 'conf.json'), 'w', encoding='utf-8'),
              sort_keys=True,
              indent=4,
              separators=(', ', ': '))
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)

bot = MBot(token, conf)

keep_alive()
executor.start_polling(bot.dispatcher)
