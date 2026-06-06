import tkinter as tk
import tkinter.messagebox as mb
import database
import shutil
import os
from datetime import datetime
from utils import BG_DARK, BG_CARD, BG_INPUT, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY, log_ui, log_sys_info, log_sys_err

def show_auth_window(on_success):
    win = tk.Tk()
    win.title('Вход в систему')
    win.geometry('2560x1440')
    win.minsize(2560, 1440)
    win.configure(bg=BG_DARK)

    is_first_run = not database.has_users()
    log_sys_info(f'Запуск окна авторизации. Первый запуск: {is_first_run}')

    frame = tk.Frame(win, bg=BG_CARD, bd=1, relief='solid', highlightbackground=BG_INPUT)
    frame.place(relx=0.5, rely=0.5, anchor='center', width=1280, height=1280)

    content = tk.Frame(frame, bg=BG_CARD)
    content.place(relx=0.5, rely=0.5, anchor='center', width=900, height=900)

    title_text = 'Создание пароля' if is_first_run else 'Авторизация'
    tk.Label(content, text=title_text, font=('Segoe UI', 24, 'bold'), bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor='center', pady=30)

    tk.Label(content, text='Введите пароль:', font=('Segoe UI', 14), bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor='w', padx=60, pady=(10, 5))
    pass_entry = tk.Entry(content, font=('Segoe UI', 14), show='*', highlightthickness=0, bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief='solid')
    pass_entry.pack(fill='x', padx=60, pady=5)

    def make_backup():
        try:
            if os.path.exists(database.DB_PATH):
                os.makedirs('backup', exist_ok=True)
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                shutil.copy2(database.DB_PATH, f'backup/deadlines_{ts}_login.db')
                log_sys_info('Автоматический бэкап при входе успешно создан')
        except Exception as e:
            log_sys_err(f'Ошибка создания бэкапа при входе: {str(e)}')

    def handle_action():
        pwd = pass_entry.get().strip()
        if not pwd:
            mb.showerror('Ошибка', 'Пароль не может быть пустым')
            return

        if is_first_run:
            if len(pwd) < 4:
                mb.showerror('Ошибка', 'Пароль должен быть от 4 символов')
                return
            database.register_user(pwd)
            log_ui('Создан новый мастер-пароль')
            mb.showinfo('Успех', 'Мастер-пароль успешно сохранен!')
            make_backup()
            win.destroy()
            on_success()
        else:
            if database.check_user(pwd):
                log_ui('Успешный вход в систему')
                make_backup()
                win.destroy()
                on_success()
            else:
                log_ui('Неудачная попытка входа: неверный пароль')
                mb.showerror('Ошибка', 'Неверный пароль!')
                pass_entry.delete(0, 'end')

    btn_text = 'Зарегистрировать' if is_first_run else 'Войти'
    tk.Button(content, text=btn_text, font=('Segoe UI', 14, 'bold'), bg=ACCENT, fg=TEXT_PRIMARY, activebackground=ACCENT, highlightthickness=0, activeforeground=TEXT_PRIMARY, cursor='hand2', command=handle_action).pack(fill='x', padx=60, pady=30)

    win.mainloop()