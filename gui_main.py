import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkcalendar as tc
from datetime import datetime
import database
import os
import shutil
from utils import (BG_DARK, BG_CARD, BG_INPUT, BG_HEADER, BORDER, ACCENT, 
                   ACCENT_GOLD, ACCENT_RED, ACCENT_GREEN, TEXT_PRIMARY, TEXT_SECONDARY, 
                   log_ui, log_sys_info, log_sys_err, check_achievements_logic)

def open_achievements(parent):
    log_ui('Открыто окно достижений')
    ach_win = tk.Toplevel(parent)
    ach_win.title('Мои достижения')
    ach_win.geometry('680x560')
    ach_win.configure(bg=BG_DARK, highlightthickness=0)
    ach_win.grab_set()

    tk.Label(ach_win, text='Мои награды', 
             font=('Segoe UI', 18, 'bold'), 
             bg=BG_DARK, fg=ACCENT_GOLD, 
             highlightthickness=0).pack(pady=20)

    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, unlocked FROM achievements')
        rows = cursor.fetchall()
        conn.close()

        for title, desc, unlocked in rows:
            card = tk.Frame(ach_win, bg=BG_CARD, bd=1, relief='solid', highlightbackground=BORDER, highlightthickness=0)
            card.pack(fill='x', padx=30, pady=5, ipady=5)
            
            status_text = 'Получено' if unlocked == 1 else 'Блокировано'
            lbl_color = ACCENT_GREEN if unlocked == 1 else TEXT_SECONDARY
            
            tk.Label(card, text=title, 
                     font=('Segoe UI', 12, 'bold'), 
                     bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor='w', padx=15, pady=(5, 2))
            
            tk.Label(card, text=desc, 
                     font=('Segoe UI', 10), 
                     bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor='w', padx=15)
            
            tk.Label(card, text=status_text, 
                     font=('Segoe UI', 10, 'bold'), 
                     bg=BG_CARD, fg=lbl_color).pack(anchor='e', padx=15, pady=(0, 5))
            
    except Exception as e:
        log_sys_err(f'Ошибка загрузки достижений в UI: {str(e)}')

def show_main_window():
    log_sys_info('Инициализация главного рабочего окна')
    root = tk.Tk()
    root.title('Помогите пожалуйста мне очень страшно')
    root.geometry('2560x1440')
    root.minsize(2560, 1440)
    root.configure(bg=BG_DARK)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview', background=BG_CARD, 
                    fieldbackground=BG_CARD, 
                    foreground=TEXT_PRIMARY, 
                    bordercolor=BORDER, 
                    rowheight=38)
    style.configure('Treeview.Heading', background=BG_HEADER, 
                    foreground=TEXT_PRIMARY, 
                    bordercolor=BORDER, 
                    lightcolor=BORDER, 
                    darkcolor=BORDER, 
                    highlightthickness=0)
    style.map('Treeview', 
              background=[('selected', ACCENT)], 
              foreground=[('selected', TEXT_PRIMARY)])
    style.map('Treeview.Heading',
              background=[('active', BG_HEADER)],
              foreground=[('active', TEXT_PRIMARY)])

    top_frame = tk.Frame(root, bg=BG_CARD, bd=1, relief='solid', highlightbackground=BORDER, highlightthickness=0)
    top_frame.pack(fill='x', padx=20, pady=20, ipady=20)

    top_frame.columnconfigure(1, weight=1)
    top_frame.columnconfigure(3, weight=1)
    top_frame.columnconfigure(5, weight=1)

    top_frame.columnconfigure(0, weight=0)
    top_frame.columnconfigure(2, weight=0)
    top_frame.columnconfigure(4, weight=0)

    tk.Label(top_frame, text='Добавление учебной задачи', 
             font=('Segoe UI', 16, 'bold'), 
             bg=BG_CARD, fg=TEXT_PRIMARY).grid(row=0, column=0, columnspan=6, pady=20)

    tk.Label(top_frame, text='Название:', 
             bg=BG_CARD, fg=TEXT_SECONDARY, 
             highlightthickness=0).grid(row=1, column=0, padx=10, pady=10)
    
    title_ent = tk.Entry(top_frame, font=('Segoe UI', 12), 
                         width=25, bg=BG_INPUT, fg=TEXT_PRIMARY, 
                         insertbackground=TEXT_PRIMARY, 
                         bd=1, relief='solid', highlightthickness=0)
    
    title_ent.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(top_frame, text='Предмет:', 
             bg=BG_CARD, fg=TEXT_SECONDARY, 
             highlightthickness=0).grid(row=1, column=2, padx=10, pady=10, sticky='w')
    
    subject_ent = tk.Entry(top_frame, font=('Segoe UI', 12), 
                           width=20, bg=BG_INPUT, fg=TEXT_PRIMARY, 
                           insertbackground=TEXT_PRIMARY, 
                           bd=1, relief='solid', highlightthickness=0)
    
    subject_ent.grid(row=1, column=3, padx=10, pady=10, sticky='w')

    tk.Label(top_frame, text='Дедлайн:', 
             bg=BG_CARD, fg=TEXT_SECONDARY, 
             highlightthickness=0).grid(row=1, column=4, padx=10, pady=10)
    
    deadline = tc.DateEntry(top_frame, font=('Segoe UI', 12), 
                            width=20, bg=BG_INPUT, fg=TEXT_PRIMARY, 
                            insertbackground=TEXT_PRIMARY, state='readonly', 
                            bd=1, relief='solid', highlightthickness=0)
    deadline.grid(row=1, column=5, padx=10, pady=10)

    tk.Label(top_frame, text='Описание:', 
             bg=BG_CARD, fg=TEXT_SECONDARY, 
             highlightthickness=0).grid(row=2, column=0, padx=10, pady=10)
    
    desc_ent = tk.Entry(top_frame, font=('Segoe UI', 12), 
                        width=25, bg=BG_INPUT, fg=TEXT_PRIMARY, 
                        insertbackground=TEXT_PRIMARY, highlightthickness=0, 
                        bd=1, relief='solid')
    
    desc_ent.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(top_frame, text='Приоритет:', 
             bg=BG_CARD, fg=TEXT_SECONDARY, 
             highlightthickness=0).grid(row=2, column=2, padx=10, pady=0)
    
    prio_combo = ttk.Combobox(top_frame, values=['Низкий', 'Средний', 'Высокий'], state='readonly', width=27)
    prio_combo.current(1)
    prio_combo.grid(row=2, column=3, padx=10, pady=10, sticky='w')

    center_frame = tk.Frame(root, bg=BG_DARK)
    center_frame.pack(fill='both', expand=True, padx=20, pady=10)

    cols = ('title', 'description', 'subject', 'deadline', 'priority', 'status')
    tree = ttk.Treeview(center_frame, columns=cols, show='headings')
    tree.heading('title', text='Задача')
    tree.heading('description', text='Описание')
    tree.heading('subject', text='Дисциплина')
    tree.heading('deadline', text='Дедлайн')
    tree.heading('priority', text='Приоритет')
    tree.heading('status', text='Статус')
    
    tree.column('title', width=300, anchor='center')
    tree.column('description', width=600, anchor='center')
    tree.column('subject', width=300, anchor='center')
    tree.column('deadline', width=250, anchor='center')
    tree.column('priority', width=200, anchor='center')
    tree.column('status', width=200, anchor='center')
    tree.pack(fill='both', expand=True, side='left')

    def refresh_table():
        try:
            for i in tree.get_children():
                tree.delete(i)
            conn = database.get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT id, title, description, subject, deadline, priority, status FROM tasks')

            status_mapping = {
                'current': 'В процессе',
                'done': 'Завершена',
                'overdue': 'Просрочена'
            }
            
            for row in cursor.fetchall():
                task_id = row[0]
                task_data = list(row[1:])
                db_status = task_data[-1]
                task_data[-1] = status_mapping.get(db_status, db_status)
                tree.insert('', 'end', iid=task_id, values=task_data)
                
            conn.close()
        except Exception as e:
            log_sys_err(f'Ошибка обновления таблицы задач: {str(e)}')

    def add_task():
        t = title_ent.get().strip()
        s = subject_ent.get().strip()
        d = deadline.get_date()
        desc = desc_ent.get().strip()
        p = prio_combo.get()

        if not t or not d:
            mb.showerror('Ошибка', 'Название и Дедлайн обязательны!')
            return

        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (title, description, subject, deadline, priority, status) VALUES (?, ?, ?, ?, ?, ?)',
                           (t, desc, s, d, p, 'current'))
            conn.commit()
            conn.close()
            
            log_ui(f'Добавлена новая задача: {t}')
            check_achievements_logic()
            refresh_table()
            title_ent.delete(0, 'end')
            desc_ent.delete(0, 'end')
            subject_ent.delete(0, 'end')
        except Exception as e:
            log_sys_err(f'Ошибка добавления задачи в БД: {str(e)}')

    tk.Button(top_frame, text='Добавить задачу', font=('Segoe UI', 12, 'bold'), 
              bg=ACCENT, fg=TEXT_PRIMARY, 
              activebackground=ACCENT, activeforeground=TEXT_PRIMARY, 
              width=19, cursor='hand2', command=add_task, 
              highlightthickness=0).grid(row=2, column=5, padx=10, pady=10)

    btn_frame = tk.Frame(root, bg=BG_DARK)
    btn_frame.pack(fill='x', padx=20, pady=5)

    def complete_task():
        sel = tree.selection()
        if not sel:
            return

        task_id = sel[0] 
        
        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ?", (task_id,))
            conn.commit()
            conn.close()
            
            log_ui(f'Задача ID {task_id} отмечена как выполненная')
            check_achievements_logic()
            refresh_table()
        except Exception as e:
            log_sys_err(f'Ошибка обновления статуса задачи: {str(e)}')

    def delete_task():
        sel = tree.selection()
        if not sel:
            return

        task_id = sel[0]
        
        try:
            conn = database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            
            log_ui(f'Задача ID {task_id} удалена')
            refresh_table()
        except Exception as e:
            log_sys_err(f'Ошибка удаления задачи из БД: {str(e)}')

    tk.Button(btn_frame, text='Отметить как выполнено', font=('Segoe UI', 12), 
              bg=BG_CARD, fg=ACCENT_GREEN, 
              activebackground=BG_CARD, activeforeground=ACCENT_GREEN, 
              bd=1, relief='solid', highlightbackground=BORDER, 
              cursor='hand2', command=complete_task, 
              highlightthickness=0).pack(side='left', padx=5)
    
    tk.Button(btn_frame, text='Удалить задачу', font=('Segoe UI', 12), 
              bg=BG_CARD, fg=ACCENT_RED, 
              activebackground=BG_CARD, activeforeground=ACCENT_RED, 
              bd=1, relief='solid', highlightbackground=BORDER, 
              cursor='hand2', command=delete_task, 
              highlightthickness=0).pack(side='left', padx=5)

    bottom_frame = tk.Frame(root, bg=BG_HEADER, height=50, bd=1, relief='solid', highlightbackground=BORDER, highlightthickness=0)
    bottom_frame.pack(fill='x', side='bottom', padx=20, pady=20)

    backup_time = datetime.now().strftime('%d.%m.%Y %H:%M')
    status_lbl = tk.Label(bottom_frame, text=f'Готов к работе | Автоматический бэкап: {backup_time}', 
                          bg=BG_HEADER, fg=TEXT_SECONDARY, 
                          font=('Segoe UI', 11))
    status_lbl.pack(side='left', padx=20, pady=10)

    def trigger_manual_backup():
        try:
            if os.path.exists(database.DB_PATH):
                os.makedirs('backup', exist_ok=True)
                ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                fname = f'deadlines_{ts}_manual.db'
                shutil.copy2(database.DB_PATH, f'backup/{fname}')
                log_ui('Создан ручной бэкап базы данных')
                status_lbl.config(text=f'Бэкап создан: {fname} | {datetime.now().strftime("%H:%M:%S")}')
        except Exception as e:
            log_sys_err(f'Ошибка создания ручного бэкапа: {str(e)}')

    tk.Button(bottom_frame, text='Сделать бэкап', font=('Segoe UI', 11), 
              bg=BG_CARD, fg=TEXT_PRIMARY, 
              activebackground=BG_CARD, activeforeground=TEXT_PRIMARY, 
              bd=0, cursor='hand2', command=trigger_manual_backup, 
              highlightthickness=0).pack(side='right', padx=10, pady=5)
    
    tk.Button(bottom_frame, text='Мои достижения', 
              font=('Segoe UI', 11, 'bold'), 
              bg=ACCENT_GOLD, fg=BG_DARK, 
              activebackground=ACCENT_GOLD, activeforeground=BG_DARK, 
              bd=0, cursor='hand2', command=lambda: open_achievements(root), highlightthickness=0).pack(side='right', padx=20, pady=5)

    refresh_table()
    root.mainloop()
    #надо было на кондитера поступать