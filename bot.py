# Inicio importaciones
import json
import os
import random
import re
import time
import urllib.parse
import urllib.request
from urllib.request import urlopen as spyder

import aiohttp
import discord
import requests
from bs4 import BeautifulSoup as soup
from discord.ext import commands

# Fin importaciones

############################ declaraciones de cabecera ###################################
DEBUG = True

clockwerk      = commands.Bot(command_prefix='/cw ', case_insensitive=True) # Dándole prefijo a sus comandos

game          = discord.Game('DOTA 2') # Qué juego juega el bot
sepa          = "************************************"  # Un separador para la consola


print('Arranca el script')
clockwerk.remove_command('help')

############################ fin declaraciones de cabecera ############################################



############################################ mis funciones ############################################
#
async def escribir(canal_, server_): # escribe los datos a un archivo json

    datos_  = ("{" + " server" + ":" " " + server_ + "," + " " + "canal" + ":" + " " + canal_ + "}")
    print('nuevos datos guardados\n' + datos_)
    with open('ClockwerkBOT/db2.json', 'a') as guardar:
        json.dump(datos_, guardar.read['datos'])

########################################## fin mis funciones #########################################

with open('respuestas.json', 'r') as array: # frases de clockwerk
    data = json.load(array) 

######################################################## Eventos ####################################

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

######################################## fin eventos #############################################



######################################### Comandos ################################################
@clockwerk.command()
async def init(ctx, cnl: str):
    canal = discord.utils.get(clockwerk.get_all_channels(), name = cnl)
    
    if canal is None:
        await ctx.send('Uhmmm,' + ' ' + '¿'+ cnl + '?' + ' ' + 'No encuentro ese canal...')
        print('Error humano, canal no encontrado')
    else: 
        await canal.send(random.choice(data['spawning']))

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

@clockwerk.command() # Devuelve los 3 mejores y el peor héroe del tiempo solicitdo, según dotabuff
async def op(ctx, tiempo = None, hero = None ):
    # La araña
        
    if tiempo == 'month' or tiempo == 'mes':
        my_url = 'https://es.dotabuff.com/heroes/winning?date=month'
    else: 
        tiempo = 'week'

    if tiempo == 'genesis':
        my_url = 'https://es.dotabuff.com/heroes/winning?date=all'
    else:
        tiempo = 'week'
    
    if tiempo == None or tiempo == 'week' or tiempo == 'semana':
        my_url = 'https://es.dotabuff.com/heroes/winning?date=week'

    if tiempo == None or tiempo == 'week' or tiempo == 'semana':
        tiempo_ = 'esta semana '
    if tiempo == 'month' or tiempo == 'mes':
        tiempo_ = 'este mes '
    if tiempo == 'genesis':
        tiempo_ = 'todos los tiempos '

    try:
       
        headers  = {}
        headers['User-Agent'] =  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        req      = urllib.request.Request(my_url, headers=headers)
        resp     = spyder(req)
        respData = resp.read()
        resp.close()
            #parser

        page_soup  = soup(respData, 'html.parser')
        valor   = []
        for tr in page_soup.find_all('tr'):
            valores = [td.text for td in tr.find_all('td')]
            valor.append(valores)
            with open('tablaOP.txt', 'w') as tabla:
                    json.dump(valor, tabla)
            with open('tablaOP.txt', 'r') as original:
                texto = original.readlines()
                fase1 = [string.replace('["", ', "")for string in texto]
                fase2 = [string.replace('[[],', "") for string in fase1]
                fase3 = [string.replace("], ", "\n") for string in fase2]
                fase4 = [string.replace("]", "") for string in fase3]
                fase5 = [string.replace("]", "\n") for string in fase4]
                fase6 = [string.replace(",", '\n') for string in fase5]
                fase7 = [string.replace(' ', '') for string in fase6]
                final = [string.replace('"', "") for string in fase7]

                with open('tablaOP.txt', 'w') as nuevo:
                  nuevo.writelines(final)
                with open('tablaOP.txt', 'r') as tablaFinal:
                    valores = tablaFinal.readlines()

        if hero is None:
            await ctx.send('Los héroes más op de ' + tiempo_ +  ' son: ' + '**'+valores[0]+'**' + 'Porcentaje de victoria: '+ valores[1] + 'tasa de elección: ' + valores[2] + 'y radio de KDA: ' + valores[3]) 
            await ctx.send('Le sigue: ' + '**'+valores[4]+'**' +'Porcentaje de victoria: '+ valores[5] +'tasa de elección: ' + valores[6] +'y radio de KDA: ' + valores[7])
            await ctx.send('Y por último: ' + '**'+valores[8]+'**' +'Porcentaje de victoria: '+ valores[9] +'tasa de elección: ' + valores[10] +'y radio de KDA: ' + valores[11])
            await ctx.send('El peor evaluado es: ' + '**'+valores[460]+'**' +'Porcentaje de victoria: '+ valores[461] +'tasa de elección: ' + valores[462] +'y radio de KDA: ' + valores[463])
        else:
            rank = valores.index(hero+'\n')
            if rank == 0:
                rank = 1 
            else:
                rank = 3*rank - rank
            await ctx.send(hero + ' está en el lugar ' + str(rank) + ' de los héroes de ' + tiempo_ )
            
    except Exception as e:
        print(str(e))
        await ctx.send('Recibí un error intentando realizar tu solicitud: ' + str(e))

    
@clockwerk.command() # Mata al robot, no le duele
async def shutdown(ctx):
    await ctx.send(random.choice(data['dying']))
    await clockwerk.logout()

######################################## fin comandos ###########################################
if DEBUG:
    with open('c:\\Users/filax/Desktop/secret.txt') as token:
        debug_token = token.read()
    clockwerk.run(debug_token)
else:    
    clockwerk.run(os.environ['TOKEN'])
