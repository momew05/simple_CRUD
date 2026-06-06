import os
import logging
from datetime import datetime

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

ui_logger = logging.getLogger('ui')
ui_handler = logging.FileHandler(os.path.join('logs', 'ui_events.log'), encoding='utf-8')
ui_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
ui_logger.addHandler(ui_handler)
ui_logger.setLevel(logging.INFO)

sys_logger = logging.getLogger('system')
sys_handler = logging.FileHandler(os.path.join('logs', 'system_logic.log'), encoding='utf-8')
sys_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s'))
sys_logger.addHandler(sys_handler)
sys_logger.setLevel(logging.INFO)

def log_ui(message):
    ui_logger.info(message)

def log_sys_info(message):
    sys_logger.info(message)

def log_sys_err(message):
    sys_logger.error(message)

def check_achievements_logic():
    import database
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM tasks')
        total_tasks = cursor.fetchone()[0]
        if total_tasks >= 1:
            cursor.execute("UPDATE achievements SET unlocked = 1 WHERE code = 'first_task'")
            
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'done'")
        done_tasks = cursor.fetchone()[0]
        if done_tasks >= 5:
            cursor.execute("UPDATE achievements SET unlocked = 1 WHERE code = 'done_5'")
            
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'overdue'")
        overdue_tasks = cursor.fetchone()[0]
        if overdue_tasks == 0 and total_tasks > 0:
            cursor.execute("UPDATE achievements SET unlocked = 1 WHERE code = 'no_overdue'")
            
        conn.commit()
        conn.close()
    except Exception as e:
        log_sys_err(f'Ошибка проверки достижений: {str(e)}')

