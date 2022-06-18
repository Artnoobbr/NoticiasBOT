#Pacotes 
import discord
from discord import message
from discord.ext import commands
from discord.ext.commands.core import cooldown
from datetime import datetime
from newsapi import NewsApiClient
import newsapi
import asyncio


#Client(bot)
client = commands.Bot(command_prefix='n!', help_command=None)
newsapi = NewsApiClient (api_key='API_KEY')


async def status_bot():
    while True:
        await client.change_presence(activity=discord.Game(name='n!help'))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game(name='Notícias da Globo e da BBC'))
        await asyncio.sleep(30)
        await client.change_presence(activity=discord.Game(name='Versão 1.0! com a API: "Newsapi"'))
        await asyncio.sleep(30)

@client.event
async def on_ready():
    print('Online')
    client.loop.create_task(status_bot())

#Comandos

#Ping command
@client.command(name="ping")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def ping(context):
    if context.author.bot:
        return
    await context.send(f"**Pong!** {context.author.mention} `{round(client.latency * 1000)}ms`")
    await context.message.delete()

@client.command(name='help')
async def help(context):
    if context.author.bot:
        return
    embed = discord.Embed(title='Comandos básicos', description='n!CovidGlobo [Notícias recentes da Globo sobre o Covid-19], n!CovidBBC [Notícias recentes da BBC sobre o Covid-19(Estão em inglês)]', color=0x3498db, timestamp=datetime.utcnow())
    embed.set_footer(text='Versão 1.0 Com a API Newsapi')
    await context.send(embed=embed)


@client.command(name="CovidGlobo")
@commands.cooldown(1, 60, commands.BucketType.guild)
async def CovidGlobo(context):
    topo_noticias = newsapi.get_top_headlines(q='Covid-19',sources='globo', language='pt')
    for article in topo_noticias['articles']:
        titulo = article['title']
        descricao = article['description']
        Fonte = article['source']['name']
        embed = discord.Embed(title=f'Título: {titulo}', description=f'Descrição: {descricao}', color=0x3498db, timestamp=datetime.utcnow())
        embed.set_footer(text=f'Versão 1.0, Newsapi, Fonte: {Fonte}')
        await context.send(embed=embed)
        await context.message.delete()

@client.command(name="CovidBBC")
@commands.cooldown(1, 60, commands.BucketType.guild)
async def CovidBBC(context):
    topo_noticias = newsapi.get_top_headlines(q='Covid',sources='bbc-news', language='en')
    for article in topo_noticias['articles']:
        titulo = article['title']
        descricao = article['description']
        Fonte = article['source']['name']
        embed = discord.Embed(title=f'Título: {titulo}', description=f'Descrição: {descricao}', color=0xe74c3c, timestamp=datetime.utcnow())
        embed.set_footer(text=f'Versão 1.0, Newsapi, Fonte: {Fonte}')
        await context.send(embed=embed)
        await context.message.delete()
    
# Error handling

@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.MissingPermissions):
        await context.send(f"{context.author} não tem permissão para executar o comando")
        await context.message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        await context.send("Você não esqueceu de algo no comando?")
        await context.message.delete()
    elif isinstance(error, commands.MemberNotFound):
        await context.send(f"Membro Não foi encontrado")
        await context.message.delete()
    elif isinstance(error, commands.CommandNotFound):
        await context.send("O comando não existe")
        await context.message.delete()
    elif isinstance(error, commands.CommandOnCooldown):
        await context.send("**Aguarde:** `{:.2f}s` Para executar o comando!".format(error.retry_after))

client.run('TOKEN')
