import sqlite3

def main():
    database = Database()
    #database.log_reminder(4643453, "08-05-2019 13:00", "Do Something")
    database.delete_reminder(7)


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()

    def log_reminder(self, sender_id, timestamp, reminder_text):
        query = "INSERT INTO reminders VALUES (NULL,?,?,?)"
        try:
            self.cursor.execute(query, (timestamp, sender_id, reminder_text))

            self.connection.commit()
        except Exception as err:
            print(err)


    def get_reminders_by_sender_id(self, sender_id):
        query = "SELECT * FROM reminders where sender_id={}".format(sender_id)
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as err:
            print(err)


    def get_all_reminders(self):
        query = "SELECT * FROM reminders"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as err:
            print(err)


    def delete_reminder(self, reminder_id):
        delete_query = "DELETE FROM reminders WHERE id={}".format(reminder_id)
        print(delete_query)
        try:
            self.cursor.execute(delete_query)
            self.connection.commit()
            query = "SELECT * FROM reminders where id={}".format(reminder_id)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if not result:
                print("Record deleted")
        except Exception as err:
            print(err)


if __name__ == '__main__':
    main()