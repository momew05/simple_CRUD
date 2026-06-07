import tkinter as tk
import tkinter.messagebox as mb
import logic
from utils import BG_DARK, BG_CARD, BG_INPUT, ACCENT, TEXT_PRIMARY, TEXT_SECONDARY, log_ui, log_sys_info, log_sys_err

def show_auth_window(on_success):
    win = tk.Tk()
    win.title('Вход в систему')
    win.geometry('2560x1440')
    win.minsize(2560, 1440)
    win.configure(bg=BG_DARK)

    first_run = logic.is_first_run()
    log_sys_info(f'Запуск окна авторизации. Первый запуск: {first_run}')

    frame = tk.Frame(win, bg=BG_CARD, bd=1, relief='solid', highlightbackground=BG_INPUT)
    frame.place(relx=0.5, rely=0.5, anchor='center', width=1280, height=1280)

    content = tk.Frame(frame, bg=BG_CARD)
    content.place(relx=0.5, rely=0.5, anchor='center', width=900, height=900)

    title_text = 'Создание пароля' if first_run else 'Авторизация'
    tk.Label(content, text=title_text, font=('Segoe UI', 24, 'bold'), bg=BG_CARD, fg=TEXT_PRIMARY).pack(anchor='center', pady=30)

    tk.Label(content, text='Введите пароль:', font=('Segoe UI', 14), bg=BG_CARD, fg=TEXT_SECONDARY).pack(anchor='w', padx=60, pady=(10, 5))
    pass_entry = tk.Entry(content, font=('Segoe UI', 14), show='•', highlightthickness=0, bg=BG_INPUT, fg=TEXT_PRIMARY, insertbackground=TEXT_PRIMARY, bd=1, relief='solid')
    pass_entry.pack(fill='x', padx=60, pady=5)

    def handle_action():
        success, message, is_reg = logic.process_auth(pass_entry.get())

        if not success:
            mb.showerror('Ошибка', message)
            if not is_reg:
                pass_entry.delete(0, 'end')
            return

        if is_reg and message:
            mb.showinfo('Успех', message)

        win.destroy()
        on_success()

    btn_text = 'Зарегистрировать' if first_run else 'Войти'
    tk.Button(content, text=btn_text, font=('Segoe UI', 14, 'bold'), 
              bg=ACCENT, fg=TEXT_PRIMARY, activebackground=ACCENT, 
              highlightthickness=0, activeforeground=TEXT_PRIMARY, 
              cursor='hand2', command=handle_action).pack(fill='x', padx=60, pady=30)

    win.mainloop()