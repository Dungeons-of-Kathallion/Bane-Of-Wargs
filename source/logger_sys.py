import logging
import os
import appdirs
from datetime import date

def log_message(message):
    program_dir = str(appdirs.user_config_dir(appname='Bane-Of-Wargs'))

    # Create log file
    os.mkdir(f'{program_dir}')
    os.mkdir(f'{program_dir}/game')
    os.mkdir(f'{program_dir}/game/data')
    os.mkdir(f'{program_dir}/game/schemas')
    os.mkdir(f'{program_dir}/game/imgs')
    os.mkdir(f'{program_dir}/logs')
    os.mkdir(f'{program_dir}/plugins')
    os.mkdir(f'{program_dir}/saves')
    with open(f'{program_dir}/logs/{date.today()}.log', 'w') as f:
        f.write("LOG")
    
    # Create and configure logger
    logging.basicConfig(filename=f'{program_dir}/logs/{date.today()}.log',
                        format='%(asctime)s %(message)s',
                        filemode='w'
                        )


    # Let us create an object
    logger = logging.getLogger()

    logger.warning(message)
