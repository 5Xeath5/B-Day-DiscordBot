from time import localtime, time
import random

import FileManipulation as FM
import hikari
import lightbulb
from lightbulb.ext import tasks

bot = lightbulb.BotApp(token='OTcyNjU4OTk0NTQxODkxNjM0.Gv4BqK.f92vxriun58x72N-rBYvzjOTfAoTKc3r9hJunY', prefix= "!", intents = hikari.Intents.ALL)
Time = localtime(time())

gif_list = ['https://c.tenor.com/Wgd0wN0SJOwAAAAC/happy-birthday-to-you-spreading-confetti.gif', 'https://c.tenor.com/ol9MSbL43VgAAAAC/happy-birthday.gif', 
'https://c.tenor.com/UkupQudNMoAAAAAC/happy-birthday-hbd.gif', 'https://c.tenor.com/x6fVglJTSEIAAAAC/love-valentines-day.gif', 'https://c.tenor.com/Q05T-lTqBjEAAAAC/adorable-cat.gif',
'https://c.tenor.com/Hl0fMeHscqYAAAAC/happy-birthday-pusheen-cat.gif', 'https://c.tenor.com/sIJ5qlYSUmcAAAAd/happy-birthday-birthday.gif', 'https://c.tenor.com/xbGXZvT_tI0AAAAM/happy-birthday-sing.gif',
'https://c.tenor.com/UwRRdD3mCQ0AAAAC/love-sis.gif', 'https://c.tenor.com/pb5cuuusCKUAAAAC/nico-yazawa-love.gif']

say_lst = FM.saying_file()

tasks.load(bot)

@tasks.task(h=1, auto_start= True)
async def check():
    await message()


async def message():
    guild_channel_dic = FM.guild_channel()
    nested_data = FM.bdaylist()
    flag = False

    for i in nested_data:
        if len(i) > 1 and Time[1] == int(i[0]) and Time[2] == int(i[1]):
            flag = True
            random_int = random.randint(0,29)
            set_channel = guild_channel_dic[i[3]]
            await bot.rest.create_message(set_channel, f'<@{i[2]}> 🎉{say_lst[random_int]}🎉', user_mentions= True)
    
    if flag:
        random_gif = random.randint(0, len(gif_list))
        await bot.rest.create_message(set_channel, gif_list[random_gif])
        flag = False        


@bot.command
@lightbulb.option('month', "Birth Month (mm)")
@lightbulb.option('day', 'Birth Day (dd)')
@lightbulb.option('user', 'Whose birth day (User ID)')
@lightbulb.command('bday', 'Add a new birthdate')
@lightbulb.implements(lightbulb.SlashCommand)
async def bday(ctx):
    guild_channel_dic = FM.guild_channel()
    current_channel = ctx.get_channel()
    if not str(ctx.get_guild().id) in guild_channel_dic:
        await bot.rest.create_message(current_channel, "Error: Server not set up")
        await ctx.respond("...") 
        return

    if not bot.cache.get_member(ctx.get_guild(), ctx.options.user):
        await bot.rest.create_message(current_channel, "Error: User not found in server")
        await ctx.respond("...")
        return
    
    try:
        int(ctx.options.day) and int(ctx.options.day)
    except:
        await bot.rest.create_message(current_channel, "Error: Please input numbers")
        await ctx.respond("...") 
        return

    if int(ctx.options.month) > 12 or int(ctx.options.day) > 31:
        await bot.rest.create_message(current_channel, "Error: Invalid month or day")
        await ctx.respond("...")
        return

    if len(ctx.options.month) < 2 or len(ctx.options.day) < 2:
        await bot.rest.create_message(current_channel, "Error: Please follow mm/dd format")
        await ctx.respond("...")
        return

    set_channel = guild_channel_dic[str(ctx.get_guild().id)]

    file = open('B-DayList', 'a')
    file.write(f'{ctx.options.month} {ctx.options.day} {ctx.options.user} {ctx.get_guild().id}\n')
    await ctx.respond("Yay!")
    await bot.rest.create_message(set_channel, "Birthdate added")
    file.close()

@bot.command
@lightbulb.option('channel', 'Input channel ID')
@lightbulb.command('setup', 'For new servers (required)')
@lightbulb.implements(lightbulb.SlashCommand)
async def setup(ctx):
    guild_channel_dic = FM.guild_channel()
    current_channel = ctx.get_channel()

    if str(ctx.get_guild().id) in guild_channel_dic:
        await bot.rest.create_message(current_channel, "Error: Server already set up")
        await ctx.respond("...")
        return

    channels_in_guild = bot.cache.get_guild_channels_view_for_guild(ctx.get_guild()).keys()
    lst = [i for i in channels_in_guild]
    if not int(ctx.options.channel) in lst:
        await bot.rest.create_message(ctx.get_channel(), "Error: Channel not found in server")
        await ctx.respond("...") 
        return
    
    FM.guild_write(ctx.get_guild().id)
    FM.channel_write(ctx.options.channel)

    await ctx.respond("Yay!")
    await bot.rest.create_message(ctx.get_channel(), "Setup complete")

@bot.command
@lightbulb.option('user', "Input user ID")
@lightbulb.command('delete', 'Delete user bday')
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_user(ctx):
    FM.delete(ctx.options.user)

    await ctx.respond("Yay!")
    await bot.rest.create_message(ctx.get_channel(), "User deleted")

@bot.command
@lightbulb.option('channel', 'new channel ID')
@lightbulb.command('reset', 'set new channel')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx):
    guild_channel_dic = FM.guild_channel()

    if not str(ctx.get_guild().id) in guild_channel_dic:
        await bot.rest.create_message(ctx.get_channel(), "Error: Server not set")
        await ctx.respond("...")
        return

    current = guild_channel_dic[str(ctx.get_guild().id)]
    FM.re(ctx.get_guild().id, ctx.options.channel, current)

    await ctx.respond("Yay!")
    await bot.rest.create_message(ctx.get_channel(), "New channel set")

@bot.command
@lightbulb.command('list', "shows a list of registered users in your server")
@lightbulb.implements(lightbulb.SlashCommand)
async def xlist(ctx):
    nested_data = FM.bdaylist()

    await ctx.respond("Yay!")
    for whole_data in nested_data:
        if str(ctx.get_guild().id) in whole_data and len(whole_data) > 1:
            user = bot.cache.get_user(int(whole_data[2]))
            await bot.rest.create_message(ctx.get_channel(),f"Month: {int(whole_data[0])} Day: {int(whole_data[1])} User: {user.username}")    

#implement reactions?
bot.run()