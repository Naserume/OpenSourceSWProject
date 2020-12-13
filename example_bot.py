import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('Nzg3NTk2OTE1MDA0ODAxMDI0.X9XQyQ.k8j8gvAsqtj3qTZzi4ebRCj2kqw')
