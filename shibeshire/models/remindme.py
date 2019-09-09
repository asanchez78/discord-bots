import time
from datetime import datetime
from models.database import Database
import threading


def main():
    reminder_time = "09-05-2019 19:58"
    reminder_text = "buy the thing"
    sender_id = 322817848894291968
    reminder = Reminder()
    reminder.log_reminder(sender_id, reminder_time, reminder_text)
    # reminders = reminder.get_reminders_by_sender_id()
    # reminder.del_reminder_by_db_id(5)
    # for result in reminders:
    #     print(result)
    #     timestamp = result[1]
    #     if datetime.strptime(timestamp, '%m-%d-%Y %H:%M') < datetime.now():
    #         print("{}, it's time to {}".format(result[2], result[3]))
    #         print(result[0])
    #         # reminder.del_reminder_by_db_id(result[0])
    # reminder.log_reminder()

    def reminder_watcher_thread():
        while True:
            reminder.get_all_reminders()
            time.sleep(5)
            print(reminder.get_reminders_by_sender_id(322817848894291968))
    reminder_watcher = threading.Thread(target=reminder_watcher_thread)
    reminder_watcher.start()
    print("I'm still doing stuff while the thread goes on")


class Reminder:

    def __init__(self):
        self.current_date = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)
        self.current_time = datetime.now()

    @staticmethod
    def get_reminders_by_sender_id(sender_id):
        db = Database()
        reminders = db.get_reminders_by_sender_id(sender_id)
        return reminders

    @staticmethod
    def is_valid_reminder_time(reminder_time):
        try:
            time.strptime(str(reminder_time), '%m-%d-%Y %H:%M')
            if datetime.strptime(reminder_time, '%m-%d-%Y %H:%M') < datetime.now():
                return "Reminder time is in the past."
            return True
        except ValueError:
            return False

    def log_reminder(self, sender_id, reminder_time, reminder_text):
        if self.is_valid_reminder_time(reminder_time):
            print(reminder_time)
            db = Database()
            db.log_reminder(str(sender_id), str(reminder_time), reminder_text)
            print("Reminder Logged for {} to {} at {}".format(sender_id, reminder_text, reminder_time))
            return "Reminder Logged for {} to {} at {}".format(sender_id, reminder_text, reminder_time)
        else:
            print("Invalid timestamp")
            return "Invalid timestamp"

    @staticmethod
    def get_all_reminders(delete=False):
        db = Database()
        reminders = db.get_all_reminders()
        past_reminders = []
        for result in reminders:
            timestamp = result[1]
            if datetime.strptime(timestamp, '%m-%d-%Y %H:%M') < datetime.now():
                past_reminders.append(result)
                print("{}, it's time to {}".format(result[2], result[3]))
                if delete:
                    db.delete_reminder(result[0])
        return past_reminders


if __name__ == '__main__':
    main()
