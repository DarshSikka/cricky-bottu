from urllib import request
from bs4 import BeautifulSoup
from flask import Flask
app=Flask(__name__)
import os
from load_matches import load_matches
from load_stats import load_players, load_teams
from load_score import load_score
import discord
from discord import Client, Intents, Embed
bot = Client(intents=Intents.default())
prefix='c!'
@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="cricket!help"))
@bot.event
async def on_message(msg):
    if(msg.content.startswith(f'{prefix}!rankings')):
        data=msg.content.split(" ")
        if(data[1].lower()=="test" or data[1].lower()=="odi" or data[1].lower()=="t20i"):
            ans=load_teams(data[1])
            msg_text=""
            for a in range(len(ans)):
                msg_text+=f"\n{a+1}. {ans[a]}"
            emb=Embed(title=f"Cricket Rankings for {data[1].lower()} cricket", description=msg_text)
            await msg.channel.send(embed=emb)
    elif msg.content.startswith(f'{prefix}players'):
        args=msg.content.split(" ")[1]
        job, format=args.split(":")
        players=load_players(job=job, format=format)
        msg_text=""
        for a in range(len(players)):
            msg_text+=f"\n{a+1}. {players[a]}"
        emb=Embed(title=f"Cricket Rankings for {job} in {format} cricket", description=msg_text)
        await msg.channel.send(embed=emb)
    elif msg.content.startswith(f"{prefix}score"):
        print(f'used score with {msg.content.split(" ")[1]}')
        try:
            data=load_score(int(msg.content.split(" ")[1]))
            emb=Embed(title=f"Match between {data['team1']['name']} and {data['team2']['name']}",
            description=f'''The score is 
            {data['team1']['name']} making ```{data['team1']['score']}```
            and 
            {data['team2']['name']} making ```{data['team2']['score']}```

            Current batting: 
            {data['batting-info']}
            Current bowling: 
            {data['bowling-info']}
        ''')
            await msg.channel.send(embed=emb)
        except:
            await msg.channel.send("Match not started yet")
    elif msg.content.startswith(f'''{prefix}matches'''):
        matches=load_matches()
        emb=Embed(title="Current matches", description=matches)
        await msg.channel.send(embed=emb)
    elif msg.content.startswith('cricket!help'):
        emb=Embed(title="Cricky bottu help", description='''
        Commands: 
            live score: cricket!score
            rankings(team): cricket!rankings <format> eg. cricket!rankings test
            rankings(players): cricket!players <role>:<format> eg. cricket!players batting:odi
        ''')
        await msg.channel.send(embed=emb)
bot.run(os.getenv('TOKEN'))