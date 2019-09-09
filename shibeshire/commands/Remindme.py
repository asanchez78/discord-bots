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


def setup(bot):
    bot.add_cog(Remindme(bot))
