from discord.ext import commands
from models.remindme import Reminder


class Remindme(commands.Cog):
    """Utility commands"""
    def __init__(self, bot):
        self.bot = bot
        self.reminder = Reminder()
        print("Reminder Loaded")

    @commands.command()
    async def remindme(self, ctx, time, reminder_text):
        """Sets a reminder"""
        sender_id = ctx.message.author.id
        if self.reminder.is_valid_reminder_time(time) is True:
            self.reminder.log_reminder(sender_id, time, reminder_text)
            await ctx.send('Setting a reminder for {} to {} at {}'
                           .format(ctx.message.author.mention, reminder_text, time))
        else:
            await ctx.send(self.reminder.is_valid_reminder_time(time))

    @commands.command()
    async def myreminders(self, ctx):
        """Lists your reminders"""
        sender_id = ctx.message.author.id
        task_list = self.reminder.get_reminders_by_sender_id(sender_id)
        if task_list:
            await ctx.send("```" + task_list + "```")
        else:
            await ctx.send("No reminders found for <@{}>".format(sender_id))

    @commands.command()
    async def delreminder(self, ctx, reminder_id):
        # sender_id = ctx.message.author.id
        task = self.reminder.get_reminder_by_id(reminder_id)
        if task:
            self.reminder.del_reminder_by_id(reminder_id)
            await ctx.send("Reminder was deleted")
        else:
            await ctx.send("No task with that ID found.")


def setup(bot):
    bot.add_cog(Remindme(bot))
