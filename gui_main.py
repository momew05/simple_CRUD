import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkcalendar as tc
from datetime import datetime
import logic
from utils import (BG_DARK, BG_CARD, BG_INPUT, BG_HEADER, BORDER, ACCENT,
                   ACCENT_GOLD, ACCENT_RED, ACCENT_GREEN,
                   TEXT_PRIMARY, TEXT_SECONDARY,
                   log_ui, log_sys_info, log_sys_err)

def open_achievements(parent):
    log_ui('Открыто окно достижений')

    ach_win = tk.Toplevel(parent)
    ach_win.title('Мои достижения')
    ach_win.geometry('1000x1000')
    ach_win.configure(bg=BG_DARK, highlightthickness=0)
    ach_win.grab_set()

    tk.Label(ach_win, text='Мои награды', 
             font=('Segoe UI', 20, 'bold'), 
             bg=BG_DARK, fg=ACCENT_GOLD, 
             highlightthickness=0).pack(pady=40)


    for title, desc, unlocked in logic.fetch_achievements():
        card = tk.Frame(ach_win, bg=BG_CARD, bd=1, relief='solid', highlightbackground=BORDER, highlightthickness=0)
        card.pack(fill='x', padx=30, pady=10, ipady=20)
        
        status_text = 'Получено' if unlocked == 1 else 'Заблокировано'
        lbl_color = ACCENT_GREEN if unlocked == 1 else TEXT_SECONDARY
        
        tk.Label(card, text=title, 
                    font=('Segoe UI', 16, 'bold'), 
                    bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor='w', padx=25, pady=(25, 15))
        
        tk.Label(card, text=desc, 
                    font=('Segoe UI', 12), 
                    bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor='w', padx=25)
        
        tk.Label(card, text=status_text, 
                    font=('Segoe UI', 12, 'bold'), 
                    bg=BG_CARD, fg=lbl_color).pack(anchor='e', padx=25, pady=(0, 5))
            
def show_main_window():
    log_sys_info('Инициализация главного рабочего окна')

    root = tk.Tk()
    root.title('Менеджер учебных задач')

    root.geometry('2560x1440')
    root.minsize(2560, 1440)
    root.configure(bg=BG_DARK)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview', background=BG_CARD, 
                    fieldbackground=BG_CARD, 
                    foreground=TEXT_PRIMARY, 
                    bordercolor=BORDER, 
                    font=('Segoe UI', 12, 'bold'),
                    rowheight=50)
    style.configure('Treeview.Heading', background=BG_HEADER, 
                    foreground=TEXT_PRIMARY, 
                    bordercolor=BORDER, 
                    lightcolor=BORDER, 
                    darkcolor=BORDER, 
                    font=('Segoe UI', 14, 'bold'),
                    highlightthickness=0)
    style.map('Treeview', 
              background=[('selected', ACCENT)], 
              foreground=[('selected', TEXT_PRIMARY)])
    style.map('Treeview.Heading',
              background=[('active', BG_HEADER)],
              foreground=[('active', TEXT_PRIMARY)])

    top_frame = tk.Frame(root, bg=BG_CARD, bd=1, relief='solid', highlightbackground=BORDER, highlightthickness=0)
    top_frame.pack(fill='x', padx=20, pady=20, ipady=20)

    top_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

    tk.Label(top_frame, text='Добавление учебной задачи', 
             font=('Segoe UI', 20, 'bold'), 
             bg=BG_CARD, fg=TEXT_PRIMARY).grid(row=0, column=0, columnspan=6, pady=20)

    tk.Label(top_frame, text='Название:', font=('Segoe UI', 14),
             bg=BG_CARD, fg=TEXT_SECONDARY, highlightthickness=0).grid(row=1, column=0, padx=5, pady=10, sticky='e')
    
    title_ent = tk.Entry(top_frame, font=('Segoe UI', 12), width=23, 
                         bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, 
                         bd=1, relief='solid', highlightthickness=0)
    title_ent.grid(row=1, column=1, padx=5, pady=10, sticky='w')

    tk.Label(top_frame, text='Предмет:', font=('Segoe UI', 14), 
             bg=BG_CARD, fg=TEXT_SECONDARY, highlightthickness=0).grid(row=1, column=2, padx=5, pady=10, sticky='nswe')
    
    subject_ent = tk.Entry(top_frame, font=('Segoe UI', 12), width=23, 
                           bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, 
                           bd=1, relief='solid', highlightthickness=0)
    subject_ent.grid(row=1, column=3, padx=5, pady=10, sticky='w')

    tk.Label(top_frame, text='Дедлайн:', font=('Segoe UI', 14), 
             bg=BG_CARD, fg=TEXT_SECONDARY, highlightthickness=0).grid(row=1, column=4, padx=5, pady=10, sticky='e')
    
    deadline = tc.DateEntry(top_frame, font=('Segoe UI', 12), width=21, 
                            bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=BG_INPUT, 
                            state='readonly', bd=1, relief='solid', highlightthickness=0)
    deadline.grid(row=1, column=5, padx=5, pady=10, sticky='w')

    tk.Label(top_frame, text='Описание:', font=('Segoe UI', 14), 
             bg=BG_CARD, fg=TEXT_SECONDARY, highlightthickness=0).grid(row=2, column=0, padx=5, pady=10, sticky='e')
    
    desc_ent = tk.Entry(top_frame, font=('Segoe UI', 12), width=23, 
                        bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, 
                        highlightthickness=0, bd=1, relief='solid')
    desc_ent.grid(row=2, column=1, padx=5, pady=10, sticky='w')

    tk.Label(top_frame, text='Приоритет:', font=('Segoe UI', 14), 
             bg=BG_CARD, fg=TEXT_SECONDARY, highlightthickness=0).grid(row=2, column=2, padx=5, pady=10, sticky='nswe')
    
    prio_combo = ttk.Combobox(top_frame, values=['Низкий', 'Средний', 'Высокий'], 
                              font=('Segoe UI', 12), state='readonly', width=21)
    prio_combo.current(1)
    prio_combo.grid(row=2, column=3, padx=5, pady=10, sticky='w')

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

    editing_task_id = None

    def refresh_table():
        for i in tree.get_children():
            tree.delete(i)
        try:
            for row in logic.fetch_tasks():
                task_id = row[0]
                tree.insert('', 'end', iid=task_id, values=row[1:])
        except Exception as e:
            log_sys_err(f'Ошибка обновления таблицы задач: {e}')
    
    def clear_inputs():
        nonlocal editing_task_id
        editing_task_id = None
        for ent in (title_ent, desc_ent, subject_ent):
            ent.delete(0, 'end')
        prio_combo.current(1)
        submit_btn.config(text='Добавить задачу', bg=ACCENT)
    
    def handle_submit():
        nonlocal editing_task_id
        title = title_ent.get().strip()
        desc = desc_ent.get().strip()
        subject = subject_ent.get().strip()
        dl_date = deadline.get_date()
        priority = prio_combo.get()

        if editing_task_id is None:
            ok, err = logic.add_task(title, desc, subject, dl_date, priority)
        else:
            ok, err = logic.update_task(editing_task_id, title, desc, subject, dl_date, priority)

        if not ok:
            mb.showerror('Ошибка', err)
            return

        refresh_table()
        clear_inputs()

    submit_btn = tk.Button(top_frame, text='Добавить задачу', font=('Segoe UI', 12, 'bold'), 
                           bg=ACCENT, fg=TEXT_PRIMARY, 
                           activebackground=ACCENT, activeforeground=TEXT_PRIMARY, 
                           width=20, cursor='hand2', command=handle_submit, 
                           highlightthickness=0)
    submit_btn.grid(row=2, column=5, padx=10, pady=10, sticky='w')

    btn_frame = tk.Frame(root, bg=BG_DARK)
    btn_frame.pack(fill='x', padx=20, pady=5)

    def complete_task():
        sel = tree.selection()
        if not sel:
            return
        ok, err = logic.complete_task(sel[0])
        if not ok:
            mb.showerror('Ошибка', err)
        else:
            refresh_table()

    def delete_task():
        sel = tree.selection()
        if not sel:
            return
        ok, err = logic.delete_task(sel[0])
        if not ok:
            mb.showerror('Ошибка', err)
        else:
            refresh_table()
    
    def start_edit():
        nonlocal editing_task_id
        sel = tree.selection()
        if not sel:
            mb.showwarning('Внимание', 'Выберите задачу для редактирования')
            return
        
        task_id = sel[0]
        raw_values = tree.item(task_id, 'values')

        task_data = logic.prepare_task_data_for_edit(raw_values)
        if not task_data:
            return

        editing_task_id = task_id

        for ent in (title_ent, desc_ent, subject_ent):
            ent.delete(0, 'end')

        title_ent.insert(0, task_data['title'])
        desc_ent.insert(0, task_data['description'])
        subject_ent.insert(0, task_data['subject'])
        
        if task_data['deadline']:
            deadline.set_date(task_data['deadline'])

        if task_data['priority'] in prio_combo['values']:
            prio_combo.set(task_data['priority'])

        submit_btn.config(text='Сохранить изменения', bg=ACCENT_GOLD)

    tk.Button(btn_frame, text='Отметить как выполнено', font=('Segoe UI', 12), 
              bg=BG_CARD, fg=ACCENT_GREEN, 
              activebackground=BG_CARD, activeforeground=ACCENT_GREEN, 
              bd=1, relief='solid', highlightbackground=BORDER, 
              cursor='hand2', command=complete_task, 
              highlightthickness=0).pack(side='left', padx=5)
    
    tk.Button(btn_frame, text='Редактировать задачу', font=('Segoe UI', 12), 
              bg=BG_CARD, fg=TEXT_PRIMARY, 
              activebackground=BG_CARD, activeforeground=TEXT_PRIMARY, 
              bd=1, relief='solid', highlightbackground=BORDER, 
              cursor='hand2', command=start_edit, 
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
        fname, err = logic.create_backup()
        if err:
            status_lbl.config(text=f'Ошибка бэкапа: {err}')
        else:
            ts = datetime.now().strftime('%H:%M:%S')
            status_lbl.config(text=f'Бэкап создан: {fname}  ·  {ts}')

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