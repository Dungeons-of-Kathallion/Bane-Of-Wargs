import os
import appdirs
from datetime import *

def log_message(message):
    program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

    with open(f'{program_dir}/logs/{date.today()}.log', 'a') as f:
        f.write(f'{datetime.now()}: {message}\n')
