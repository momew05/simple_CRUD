import database
from gui_auth import show_auth_window
from gui_main import show_main_window
from utils import log_sys_info

def main():
    log_sys_info('Инициализация и запуск приложения')
    database.init_db()
    
    def start_app():
        show_main_window()

    show_auth_window(start_app)

if __name__ == '__main__':
    main()