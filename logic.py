import os
import shutil
from datetime import datetime
import database
from utils import log_ui, log_sys_err, log_sys_info

def is_first_run():
    return not database.has_users()

def make_login_backup():
    try:
        if os.path.exists(database.DB_PATH):
            os.makedirs('backup', exist_ok=True)
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            shutil.copy2(database.DB_PATH, f'backup/deadlines_{ts}_login.db')
            log_sys_info('Автоматический бэкап при входе успешно создан')
            return True
    except Exception as e:
        log_sys_err(f'Ошибка создания бэкапа при входе: {str(e)}')
    return False

def process_auth(password):
    password = password.strip()
    if not password:
        return False, 'Пароль не может быть пустым', None

    first_run = is_first_run()

    if first_run:
        if len(password) < 4:
            return False, 'Пароль должен быть от 4 символов', first_run
        
        try:
            database.register_user(password)
            log_ui('Создан новый пароль')
            make_login_backup()
            return True, 'Пароль успешно сохранен!', first_run
        except Exception as e:
            return False, f'Ошибка при регистрации: {e}', first_run
    else:
        if database.check_user(password):
            log_ui('Успешный вход в систему')
            make_login_backup()
            return True, None, first_run
        else:
            log_ui('Неудачная попытка входа: неверный пароль')
            return False, 'Неверный пароль!', first_run

STATUS_MAP = {
    'current': 'В процессе',
    'done':    'Завершена',
    'overdue': 'Просрочена',
}

def fetch_tasks():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, subject, deadline, priority, status FROM tasks')
    rows = cursor.fetchall()
    conn.close()

    today_str = datetime.now().strftime('%Y-%m-%d')

    result = []
    for row in rows:
        task_id, title, description, subject, deadline, priority, status = row

        if status == 'current' and deadline < today_str:
            status = 'overdue'

        human_status = STATUS_MAP.get(status, status)
        
        result.append((task_id, title, description, subject, deadline, priority, human_status))
        
    return result


def add_task(title, description, subject, deadline, priority):
    if not title or not deadline:
        return False, 'Название и Дедлайн обязательны!'

    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description, subject, deadline, priority, status) VALUES (?, ?, ?, ?, ?, ?)',
            (title, description, subject, deadline, priority, 'current'),
        )
        conn.commit()
        conn.close()
        log_ui(f'Добавлена новая задача: {title}')
        check_achievements_logic()
        return True, None
    except Exception as e:
        log_sys_err(f'Ошибка добавления задачи в БД: {e}')
        return False, str(e)


def complete_task(task_id):
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        log_ui(f'Задача ID {task_id} отмечена как выполненная')
        check_achievements_logic()
        return True, None
    except Exception as e:
        log_sys_err(f'Ошибка обновления статуса задачи: {e}')
        return False, str(e)


def delete_task(task_id):
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        log_ui(f'Задача ID {task_id} удалена')
        return True, None
    except Exception as e:
        log_sys_err(f'Ошибка удаления задачи из БД: {e}')
        return False, str(e)

def update_task(task_id, title, description, subject, deadline, priority):
    if not title or not deadline:
        return False, 'Название и Дедлайн обязательны!'

    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE tasks 
               SET title = ?, description = ?, subject = ?, deadline = ?, priority = ? 
               WHERE id = ?''',
            (title, description, subject, deadline, priority, task_id),
        )
        conn.commit()
        conn.close()
        log_ui(f'Задача ID {task_id} успешно обновлена')
        check_achievements_logic()
        return True, None
    except Exception as e:
        log_sys_err(f'Ошибка обновления задачи в БД: {e}')
        return False, str(e)

def prepare_task_data_for_edit(values):
    if not values or len(values) < 5:
        return None

    parsed_date = None
    try:
        parsed_date = datetime.strptime(values[3], '%Y-%m-%d').date()
    except Exception:
        pass

    return {
        'title': values[0],
        'description': values[1],
        'subject': values[2],
        'deadline': parsed_date,
        'priority': values[4]
    }

def fetch_achievements():
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, unlocked FROM achievements')
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        log_sys_err(f'Ошибка загрузки достижений: {e}')
        return []

def create_backup():
    try:
        if not os.path.exists(database.DB_PATH):
            return None, 'Файл базы данных не найден'

        os.makedirs('backup', exist_ok=True)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        fname = f'deadlines_{ts}_manual.db'
        shutil.copy2(database.DB_PATH, f'backup/{fname}')
        log_ui('Создан ручной бэкап базы данных')
        return fname, None
    except Exception as e:
        log_sys_err(f'Ошибка создания ручного бэкапа: {e}')
        return None, str(e)
    
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