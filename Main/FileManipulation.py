def guild_channel():
    guild_file = open('GuildList', 'r')
    guild_read = guild_file.read()
    guild_lst = guild_read.split('\n')

    channel_file = open('ChannelList', 'r')
    channel_read = channel_file.read()
    channel_lst = channel_read.split('\n')

    guild_file.close()
    channel_file.close()
    return dict(zip(guild_lst, channel_lst))

def saying_file():
    sayings = open('Sayings','r')
    saying = sayings.read()
    say_lst = saying.split("\n")

    sayings.close()
    return say_lst

def bdaylist():
    file =  open('B-DayList', 'r')
    data = file.read()
    data_lst = data.split("\n")
    nested_data = [i.split(' ') for i in data_lst]

    file.close()
    return nested_data

def guild_write(text):
    guild_file = open('GuildList', 'a')
    guild_file.write(f'{text}\n')
    guild_file.close()

def channel_write(text):
    channel_file = open('ChannelList', 'a')
    channel_file.write(f'{text}\n')
    channel_file.close()

def delete(text):
    with open('B-DayList', 'r') as f:
        lines = f.readlines()
    with open('B-DayList', 'w') as f:
        for line in lines:
            if not str(text) in line:
                f.write(line)
    f.close()

def re(guild, channel, current):
    with open('GuildList', 'r') as f:
        lines = f.readlines()
    with open('GuildList', 'w') as f:
        for line in lines:
            if not str(guild) in line:
                f.write(line)
        f.write(f'{guild}\n')  
        f.close()

    with open('ChannelList', 'r') as f:
        lines = f.readlines()
    with open('ChannelList', 'w') as f:
        for line in lines:
            if not current in line:
                f.write(line)
        f.write(f'{channel}\n')
        f.close()