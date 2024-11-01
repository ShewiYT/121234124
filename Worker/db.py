import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `workers` WHERE `id` = ?", (id,)).fetchall()
            return bool(len(result))

    def add_user(self, id, referrer_id):
        with self.connection:
            if referrer_id != None:
                return self.cursor.execute("INSERT INTO `workers` (`id`, `referrer_id`) VALUES (?,?)", (id, referrer_id,))
            else:
                return self.cursor.execute("INSERT INTO `workers` (`id`) VALUES (?)", (id,))

    def count_reeferals(self, id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(`id`) as count FROM `workers` WHERE `referrer_id` = ?", (id,)).fetchone()[0]