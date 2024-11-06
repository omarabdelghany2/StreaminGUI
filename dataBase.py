import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='data.db'):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY,
                        month INTEGER,
                        day INTEGER,
                        hour INTEGER,
                        minute INTEGER,
                        am_pm TEXT,
                        platform TEXT,
                        url TEXT,
                        duration INTEGER)''')
        self.conn.commit()

    def add_task(self, month, day, hour, minute, am_pm, platform, url,duration):
        current_datetime = datetime.now()
        self.c.execute("INSERT INTO tasks (month, day, hour, minute, am_pm, platform, url,duration) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
                    (month, day, hour, minute, am_pm, platform, url,duration))
        self.conn.commit()
        print("Task added successfully.")

    def _reorder_ids(self, deleted_id):
        self.c.execute("UPDATE tasks SET id = id - 1 WHERE id > ?", (deleted_id,))
        self.conn.commit()
        print("IDs reordered successfully.")

    def delete_task(self, task_id):
        self.c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self._reorder_ids(task_id)
        print("Task deleted successfully.")

    def get_all_tasks(self):
        self.c.execute("SELECT * FROM tasks")
        tasks = self.c.fetchall()
        return tasks

    def close_connection(self):
        self.conn.close()

# # Example usage
# database_manager = DatabaseManager()
# database_manager.add_task(1, 1, 1, 1, "AM", "youtube", "https://www.youtube.com")
# database_manager.add_task(1, 1, 1, 1, "PM", "youtube", "https://www.youtube.com")

# for task in database_manager.get_all_tasks():
#     print(task)

# database_manager.close_connection()
