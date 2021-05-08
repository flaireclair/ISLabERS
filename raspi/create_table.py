from database_manager import DatabaseManager

if __name__ == '__main__':
    with DatabaseManager() as dm:
        dm.create()