import os
import logging
from logging.handlers import RotatingFileHandler

BG_DARK = '#0E1117'
BG_CARD = '#161B27'
BG_INPUT = '#1C2333'
BG_HEADER = '#0A0D14'
BORDER = '#2A3347'
ACCENT = '#4A6CF7'
ACCENT_GOLD = '#F5C542'
ACCENT_RED = '#E84545'
ACCENT_GREEN = '#2DD4BF'
TEXT_PRIMARY = '#EAF0FF'
TEXT_SECONDARY = '#8892A4'

os.makedirs('logs', exist_ok=True)

MAX_LOG_SIZE = 5 * 1024 * 1024 
BACKUP_COUNT = 3                

ui_logger = logging.getLogger('ui')
ui_handler = RotatingFileHandler(
    os.path.join('logs', 'ui_events.log'), 
    maxBytes=MAX_LOG_SIZE, 
    backupCount=BACKUP_COUNT,
    encoding='utf-8')

ui_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
ui_logger.addHandler(ui_handler)
ui_logger.setLevel(logging.INFO)

sys_logger = logging.getLogger('system')
sys_handler = RotatingFileHandler(
    os.path.join('logs', 'system_logic.log'), 
    maxBytes=MAX_LOG_SIZE, 
    backupCount=BACKUP_COUNT,
    encoding='utf-8')

sys_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
sys_logger.addHandler(sys_handler)
sys_logger.setLevel(logging.INFO)

def log_ui(message):
    ui_logger.info(message)

def log_sys_info(message):
    sys_logger.info(message)

def log_sys_err(message):
    sys_logger.error(message)

