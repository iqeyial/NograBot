from discord.ext import commands
import discord, datetime, time
import pytz
from pytz import timezone
import asyncio


timeformat = "%Y-%m-%d %H:%M:%S"
durationformat = "%-dd %-Hh %-Mm %-Ss"
def timetosgtime(x):
    utctime = x
    sgttime = utctime.astimezone(timezone("Asia/Singapore"))
    return sgttime.strftime(timeformat)

start_time = time.time()
utcbootime = datetime.datetime.now(timezone("UTC"))

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog \"Moderation\" loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 800184970298785802:
            return
        if message.channel.id in [
        803662591690932235,
        813288124460826669,
        802581920886030406,
        804260533666578432,
        810007696057040906,
        810007702058565632,
        ]:
            await message.delete()
            if message.guild.id == 789840820563476482:
                channel = self.client.get_channel(804260533666578432)
                await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                    message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")
            elif message.guild.id == 796727833048645692:
                channel = self.client.get_channel(810007702058565632)
                await channel.send("**" + str(message.author.mention) + "**, if you continue to talk in <#" + str(
                    message.channel.id) + "> i'm gonna have to mute you <a:pik:801091998290411572>")

        if message.channel.id == 821640987003977778 and "roblox.com" not in message.content:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} this channel is for posting ROBLOX games only! :c\nIf you want to talk about the game, do it in <#818436261891014660> or <#821033003823923212>",
                delete_after=3.0)

    @commands.command(pass_context=True, name="clear", brief="Purges messages", description="purges messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, number=None):
        if number is None:
            await ctx.send("Try again, but do tell me how many messages do you want to clear.")
        else:
            number = int(number)
            await ctx.channel.purge(limit=number + 1, check=lambda msg: not msg.pinned)
            await ctx.send(str(number) + " messages were cleared in bulk. <a:Tick:796984073603383296>",
                           delete_after=3.0)
            # choosing a channel to send the ar.lear mod log if command is used in different servers

            if ctx.guild.id == 738632364208554095:
                channel = self.client.get_channel(762898168803229707)
            if ctx.guild.id == 781056775544635412:
                channel = self.client.get_channel(781064310758572063)
            if ctx.guild.id == 789840820563476482:
                channel = self.client.get_channel(802786241799651330)
            if ctx.guild.id == 818436261873844224:
                channel = self.client_get_channel(821042412624412733)
            # embed to be posted in modlogs
            timestamp = ctx.message.created_at
            clearembed = discord.Embed(title="`Clear` action done with Nogra", color=0xff0000)
            clearembed.set_author(name=str(ctx.author.name) + "#" + str(ctx.author.discriminator),
                                  icon_url=str(ctx.author.avatar_url))
            clearembed.add_field(name=str(number) + " messages deleted", value="in " + str(ctx.channel.mention),
                                 inline=False)
            clearembed.set_footer(text="ID: " + str(ctx.author.id) + " • " + str(timestamp))
            await channel.send(embed=clearembed)

    @commands.command(pass_context=True, name="uptime", brief="Uptime go brr", description="Shows you Nogra's uptime.")
    async def uptime(self, ctx):
        current_time = time.time()
        current_datetime = datetime.datetime.now(timezone("UTC"))
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.set_author(name=self.client.user.name, icon_url=str(self.client.user.avatar_url))
        embed.add_field(name="Time of last reboot", value=timetosgtime(utcbootime), inline=True)
        embed.add_field(name="Time now", value=timetosgtime(current_datetime), inline=True)
        embed.add_field(name="Uptime", value=text, inline=False)
        embed.set_footer(text="Time is in GMT+8 (Asia/Singapore)")
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

    @commands.command(name="invite", brief="Invite the bot", description="Gives you invite links for Nogra")
    async def invite(self, ctx):
        embed = discord.Embed(colour=0x00FF00)
        embed.set_author(name=f"Add {self.client.user.name} to your server!", icon_url=str(self.client.user.avatar_url))
        embed.add_field(name="Recommended Invite Link",
                        value="[Nogra with only necessary permissions](https://discord.com/oauth2/authorize?client_id=800184970298785802&permissions=1544416503&scope=bot)")
        embed.add_field(name="Admin Invite Link",
                        value="[Nogra with Admin Invite Permissoin](https://discord.com/api/oauth2/authorize?client_id=800184970298785802&permissions=8&scope=bot)")
        embed.set_thumbnail(url=str(self.client.user.avatar_url))
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send(f"Invite {self.client.user.name} to your server with only necessary permissions here **(Recommended): https://discord.com/api/oauth2/authorize?client_id=800184970298785802&permissions=8&scope=bot\n")

    @commands.command()
    @commands.has_permissions(manage_permissions=True)
    async def abuse(self, ctx, member:discord.Member=None):
        if member is None:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/797711768696651787/818796868758274059/unknown.png")
        else:
            var = discord.utils.get(ctx.guild.roles, name="admin")
            await member.add_roles(var)
            await ctx.send(
                f"{member.mention} {ctx.author.name} granted you the power of abuse here, have fun! <:nogracuteblush:806168390003064883>")

    @abuse.error
    async def abuse_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("lmfao no you need \"manage permissions\" to let people abuse")
        else:
            await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command()
    @commands.has_permissions(manage_permissions=True)
    async def stopabusing(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(
                "https://cdn.discordapp.com/attachments/797711768696651787/818796868758274059/unknown.png")
        else:
            await ctx.send(
                f"{member.mention} {ctx.author.name} felt that you weren't worthy of abusing. <:nograhahausuck:819085149525245962>")
            var = discord.utils.get(ctx.guild.roles, name="admin")
            await member.remove_roles(var)

    @stopabusing.error
    async def stopabusing_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("lmfao no you need \"manage permissions\" to stop people from wrecking the server")
        else:
            await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    '''@clear.error
    async def cog_command_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")'''

    @uptime.error
    async def uptime_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @clear.error
    async def clear_error(self, ctx, error):
        await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None or member == ctx.message.author:
            await ctx.send("You cannot ban yourself...")
            return
        if reason is None:
            reason = "no specified reason"
            message = f"You have been banned from {ctx.guild.name} for: no specified reason."
            try:
                await member.send(message)
            except discord.errors.Forbidden:
                pass
            await member.ban(reason=reason)
            await ctx.send(f"{member} is banned for: {reason}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def cban(ctx, member: discord.Member = None, duration=None, *, reason=None):
        if member is None or member == ctx.message.author:
            await ctx.send("You cannot ban yourself...")
            return
        if duration is None:
            await ctx.send(
                "You need to specify how long before " + member.name + " is banned. <:nograpepeuhh:803857251072081991>")
        else:
            if reason is None:
                reason = "no specified reason"
                timer = int(duration) * 60
                await ctx.send("Alright, I will ban " + member.name + " in " + duration + " minutes.")
                await asyncio.sleep(timer)
                message = f"You have been banned from {ctx.guild.name} for: no specified reason."
                try:
                    await member.send(message)
                except discord.errors.Forbidden:
                    pass
                await member.ban(reason=reason)
                await ctx.send(f"{member} is banned for: {reason}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("wheeze you don't even have permissions to ban people")
        else:
            await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")

    @cban.error
    async def cban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You don\'t have the permission to ban others.')
        else:
            await ctx.send(f"```diff\n- Error encountered!\n# erorr:\n+ {error}```")


def setup(client):
    client.add_cog(Moderation(client))
