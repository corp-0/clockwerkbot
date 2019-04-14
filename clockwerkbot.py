#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
"""Clockwerkbot is a Discord bot that gives you Dota2 Stats."""
 
# imports
import json
import os
import random
import re
import urllib.parse
import urllib.request
from urllib.request import urlopen as spyder
from collections import defaultdict

import aiohttp
import discord
import requests
from bs4 import BeautifulSoup as soup
from discord.ext import commands

# global variables
DEBUG = True
clockwerk     = commands.Bot(command_prefix='/cw ', case_insensitive=True) # Dándole prefijo a sus comandos
game          = discord.Game('Dota 2') # Qué juego juega el bot
sepa          = "************************************"  # Un separador para la consola
with open('respuestas.json', 'r') as array: # frases de clockwerk
    data = json.load(array)

# events
@clockwerk.event
async def on_ready(): # Al estar listo el bot
    print('El bot ha iniciado sesión')
    if (clockwerk.is_ready()):
        print(sepa)
        print('Nombre: ' + clockwerk.user.name)
        print('ID: ' + str(clockwerk.user.id))
        print(sepa)
        conexiones = clockwerk.guilds
        nConexiones = len(conexiones)
        print('Estoy conectado en ' + str(nConexiones) + ' servidores: ')
        print(conexiones)
        print(sepa)
        print('mi ping es ' + str(clockwerk.latency))
        await clockwerk.change_presence(status=discord.Status.online, activity=game, afk=False)
        print(sepa)
        try:
            canal = discord.utils.get(clockwerk.get_all_channels(), name = "dota2")
            await canal.send(random.choice(data['spawning']))
        except: 
            pass

# Commands
@clockwerk.command() # Devuelve los 3 mejores y el peor héroe del tiempo solicitado, según dotabuff
async def op(ctx, tiempo = None, hero = None ):
    # La araña
    if tiempo == None:
        await ctx.send('El tiempo es un argumento requerido')
        await ctx.send('Posibles valores: genesis, mes, semana')
        return False
    elif tiempo == 'genesis':
        my_url = 'https://es.dotabuff.com/heroes/winning?date=all'
        tiempo_str = 'Todos los tiempos' 
      
    elif tiempo == 'month' or tiempo == 'mes':
        my_url = 'https://es.dotabuff.com/heroes/winning?date=month'
        tiempo_str = 'este mes'

    elif tiempo == 'week' or tiempo == 'semana':
        my_url = 'https://es.dotabuff.com/heroes/winning?date=week'
        tiempo_str = 'esta semana'
    else:
        await ctx.send('No entendí el tiempo que me pides.')
        await ctx.send('Posibles valores: genesis, mes, semana')
        return False

    try:
        headers  = {}
        headers['User-Agent'] =  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        req      = urllib.request.Request(my_url, headers=headers)
        resp     = spyder(req)
        respData = resp.read()
        resp.close()
        page_soup  = soup(respData, 'html.parser')
        valor = []
        for tr in page_soup.find_all('tr'):
            valores = [td.text for td in tr.find_all('td')]
            valor.append(valores)
        valor.pop(0)

        illu = defaultdict(list)
        rank = 0
        for heroes in valor:
            rank = rank + 1
            heroes.pop(0)
            illu[rank].append(heroes)
        
        dd = defaultdict(list)
        for x,y in illu.items():
            hero_name     = y[0][0]
            hero_name     = hero_name.replace(" ", "")
            hero_victory  = y[0][1]
            hero_pickrate = y[0][2]
            hero_kda      = y[0][3]
            dd[x].append(hero_name)
            dd[x].append(hero_victory)
            dd[x].append(hero_pickrate)
            dd[x].append(hero_kda)
        
        first_hero = dd.get(1)
        second_hero = dd.get(2)
        third_hero = dd.get(3)
        last_hero = list(dd.keys())[-1]
        last_hero = dd.get(last_hero)

        if hero != None:
            for x,y in dd.items():
                if hero in y:
                    this_hero_rank = x
                    this_hero_data = dd.get(this_hero_rank)

            if hero != None:
                await ctx.send('**'+hero+'**' + ' está en el lugar ' + str(this_hero_rank) + ' de los héroes de ' + tiempo_str )
                await ctx.send("con un porcentaje de victoria de: " + this_hero_data[1] + ', tasa de elección:  '+ this_hero_data[2] + ', y radio de KDA:  '+ this_hero_data[3])
                return False

        if hero == None:
            await ctx.send('Los héroes más op de ' + tiempo_str +  ' son: ' + '**'+ first_hero[0] +'**' + ', Porcentaje de victoria: '+ first_hero[1] + ', tasa de elección: ' + first_hero[2] + ', y radio de KDA: ' + first_hero[3]) 
            await ctx.send('Le sigue: ' + '**'+ second_hero[0] +'**' +', Porcentaje de victoria: '+ second_hero[1] +', tasa de elección: ' + second_hero[2] +', y radio de KDA: ' + second_hero[3])
            await ctx.send('Y por último: ' + '**'+ third_hero[0] +'**' +', Porcentaje de victoria: '+ third_hero[1] +', tasa de elección: ' + third_hero[2] +', y radio de KDA: ' + third_hero[3])
            await ctx.send('El peor evaluado es: ' + '**'+ last_hero[0] +'**' +', Porcentaje de victoria: '+ last_hero[1] +', tasa de elección: ' + last_hero[2] +', y radio de KDA: ' + last_hero[3])
            return True

    except Exception as e:
        await ctx.send(str(e))
        await ctx.send('Recibí un error intentando realizar tu solicitud: ' + str(e))

@clockwerk.command()
async def say(ctx, msg: str, cnl = None):
    if cnl == None:
        canal = ctx
        await ctx.send(msg)
    else:
        canal = discord.utils.get(clockwerk.get_all_channels(), name = cnl)
        if canal is None:
            await ctx.send('Uhmmm... No encuentro el canal ' + cnl)
        else:
            await canal.send(msg)

@clockwerk.command()
async def sayAloud(ctx, msg: str, cnl = None):
    if cnl == None:
        canal = ctx
        await ctx.send(msg, tts=True)
    else:
        canal = discord.utils.get(clockwerk.get_all_channels(), name = cnl)
        if canal is None:
            await ctx.send('Uhmmm... No encuentro el canal ' + cnl, tts=True)
        else:
            await canal.send(msg, tts=True)
    
@clockwerk.command() # Mata al robot, no le duele
async def shutdown(ctx):
    await ctx.send(random.choice(data['dying']))
    await clockwerk.logout()
  
######################################## run ###########################################
if DEBUG:
    with open('E:\\filax\\Documents\\secret.txt') as token:
        debug_token = token.read()
    clockwerk.run(debug_token)
else:    
    clockwerk.run(os.environ['TOKEN'])