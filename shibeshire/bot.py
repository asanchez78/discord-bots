from discord.ext import commands
from datetime import datetime
import config
import asyncio
from models.remindme import Reminder
from models.database import Database

bot = commands.Bot(description="This is my hello world bot", command_prefix="/")


@bot.event
async def on_ready():
    bot.load_extension("commands.Loader")
    bot.load_extension("commands.Commands")
    bot.load_extension("commands.Remindme")
    bot.loop.create_task(my_background_task(bot))


async def my_background_task(self):
    await self.wait_until_ready()
    channel = self.get_channel(config.reminders_channel)
    reminder = Reminder()
    db = Database()
    while not self.is_closed():
        reminders = reminder.get_all_reminders()
        for result in reminders:
            print(result)
            timestamp = result[1]
            if datetime.strptime(timestamp, '%m-%d-%Y %H:%M') < datetime.now():
                print("<@{}>, it's time to {}".format(result[2], result[3]))
                print(result[0])
                db.delete_reminder(result[0])
                await channel.send("<@{}>, it's time to {}".format(result[2], result[3]))
        await asyncio.sleep(5)  # task runs every 5 seconds

print('Initializing bot ' + str(datetime.now()))
bot.run(config.bot_token)
