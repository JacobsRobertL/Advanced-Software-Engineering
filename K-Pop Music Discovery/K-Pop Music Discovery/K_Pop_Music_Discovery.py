from ui.app_window import AppWindow
from database.db_repository import DatabaseRepository

def main():
    db_repo = DatabaseRepository()
    db_repo.initialize_database()

    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    main()