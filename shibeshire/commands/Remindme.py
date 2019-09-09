from discord.ext import commands
from models.remindme import Reminder


class Remindme(commands.Cog):
    """Utility commands"""
    def __init__(self, bot):
        self.bot = bot
        print("Reminder Loaded")

    @commands.command()
    async def remindme(self, ctx, time, reminder_text):
        """Sets a reminder"""
        sender_id = ctx.message.author.id
        reminder = Reminder()
        if reminder.is_valid_reminder_time(time) is True:
            reminder.log_reminder(sender_id, time, reminder_text)
            await ctx.send('Setting a reminder for {} to {} at {}'
                           .format(ctx.message.author.mention, reminder_text, time))
        else:
            await ctx.send(reminder.is_valid_reminder_time(time))

    @commands.command()
    async def myreminders(self, ctx):
        """Lists your reminders"""
        sender_id = ctx.message.author.id
        reminder = Reminder()
        reminders = reminder.get_reminders_by_sender_id(sender_id)
        reminder_list = []
        if reminders:
            for reminder in reminders:
                id = str(reminder[0])
                time = reminder[1]
                task = reminder[3]
                reminder_list.append(id + '. ' + time + ' ' + task)
            task_list = '\n'.join(reminder_list)
            await ctx.send("```" + task_list + "```")
        else:
            await ctx.send("No reminders found for <@{}>".format(sender_id))

    @commands.command()
    async def delreminder(self, ctx, reminder_id):
        sender_id = ctx.message.author.id
        reminder_id = reminder_id
        reminder = Reminder()
        task = reminder.get_reminder_by_id(reminder_id)
        if task:
            reminder.del_reminder_by_id(reminder_id)
            await ctx.send("Reminder was deleted")
        else:
            await ctx.send("No task with that ID found.")


def setup(bot):
    bot.add_cog(Remindme(bot))
