from discord.ext import commands, tasks
from zmq import Context, REP, Poller, POLLIN, NOBLOCK
import discord
import json

context = Context()
socket = context.socket(REP)
socket.bind("tcp://*:5555")

poller = Poller()
poller.register(socket, POLLIN)


class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents, self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents, self_bot=self_bot)
        self.P = command_prefix

        self.add_commands()

    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{self.P}help"))

        self.test.start()

        print("Bot ready!")

    def add_commands(self):
        @self.command(pass_context=True)
        async def teste(ctx):
            await ctx.send('testado')

    @tasks.loop(seconds=0.3)
    async def test(self):
        if poller.poll(10):
            message = socket.recv(NOBLOCK).decode('ascii')
            print(f'Recieved from server: {message}')

            if message == 'servers':
                # guilds = ''
                # for guild in self.guilds:
                #     guilds += str(guild.icon_url) + ', '

                guids = {}
                for guild in self.guilds:
                    guids[guild.id] = [guild.name, guild.id, str(guild.icon_url)]

                socket.send_string(json.dumps(guids))
            elif 'guild_' in message:
                guild_id = int(message.split('_')[1])
                guild = self.get_guild(guild_id)

                channels = {'text': [], 'voice': []}
                for text_channel in guild.text_channels:
                    channels['text'].append((text_channel.name, text_channel.id, 'text'))

                for voice_channel in guild.voice_channels:
                    channels['voice'].append((voice_channel.name, voice_channel.id, 'voice'))

                socket.send_string(json.dumps(channels))
            elif 'users_' in message:
                guild_id = int(message.split('_')[1])
                guild = self.get_guild(guild_id)

                members = {'members': []}
                for member in guild.members:
                    members['members'].append([member.name, str(member.avatar_url)])

                socket.send_string(json.dumps(members))

            elif 'channel_' in message:
                channel_id = int(message.split('_')[1])
                channel = self.get_channel(channel_id)

                messages = await channel.history(limit=30).flatten()

                show = {'message': []}
                for sent_message in messages:
                    try:
                        nick = sent_message.author.nick
                        if nick is None:
                            raise AttributeError
                    except AttributeError:
                        nick = sent_message.author.name
                    show['message'].append((sent_message.content, nick))

                socket.send_string(json.dumps(show))
            elif 'send_' in message:
                _, channel_id, text = message.split('_', 2)
                channel = self.get_channel(int(channel_id))

                await channel.send(text)

                socket.send(b'ok')


def content(ctx):
    try:
        message = ctx.content
        return message
    except:
        message = ctx.message.content

    if message.count(" ") > 0:
        return message.split(" ", 1)[1]
    else:
        return ''


if __name__ == '__main__':
    print('initializing bot...')
    bot = MyBot(command_prefix="!", intents=discord.Intents.all(), self_bot=False)
    bot.run(INSERT BOT TOKEN HERE)  # bot de teste
