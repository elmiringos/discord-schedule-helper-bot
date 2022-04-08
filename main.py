import discord    
from discord.ext import commands
from time_table import get_schedule
import datetime
from discord_components import DiscordComponents, Button, ButtonStyle   #Импортируем все необходимые библиотеки и модули
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix='!') #Создаем тело бота и добавляем префик для наших команд


@client.event #Создаем события, которая выполнеяет при каждом включении бота
async def on_ready():
    DiscordComponents(client) #Используем эту функцию, для добавления кнопок в бота
    print('We have logged in as {0.user}'.format(client)) #Чтобы отслеживать включение, добавляем эту строку

 
async def schedule(ctx, arg):  #Функция для распечатывания расписания. Получает на вход два аргумента,
    await ctx.send(f"------{datetime.datetime.now()}-------") #Первой строкой выводим сегодняшнюю дату и время
    table = get_schedule(arg) #Используем функцию из модуля и получаем расписание
    if table == "Выходной": #Делаем проверку на выходной
        await ctx.send("Сегодня выходной, занятий нет")
        return 0
    for item in get_schedule(arg): #выводим каждый элемент массива(занятие)
        await ctx.send(item)


async def clear(ctx, amount : int): #Функция для удаления сообщений в чате 
    await ctx.channel.purge(limit = int(amount)) #Используем встроенный метод "purge", и устанавливаем limit


@client.command()  #Включаем использование команды для бота
async def menu(ctx): #функция для использваония меню
    await ctx.send( 
        embed=discord.Embed(title = "Команды и функции"),  #Создаем кнопки
        components = [
            Button(style = ButtonStyle.green, label = "Расписание на сегодня"), #Для каждой кнопки добавлем цвет и название
            Button(style = ButtonStyle.red, label = "Начать занятие"),
            Button(style = ButtonStyle.blue, label = "Очистить чат")                
        ]
    )
    response = await client.wait_for("button_click") #создаем реакцию на нажатие кнопки
    if response.channel == ctx.channel: #проверяем на какую кнопку нажал пользователь
        if response.component.label == "Расписание на сегодня": 
            await response.respond(content = "Напишите название группу") #Спрашиваем у пользователя название группы
            group = await client.wait_for('message', check = lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id) #считываем название группы из чата
            await schedule(ctx, group.content) #Используя функцию, выводим расписание
        if response.component.label == "Начать занятие":
            await ctx.channel.send(content = "@everyone Преподователь начал занятие") #используем упоминание всех пользователей
        elif response.component.label == "Очистить чат":
            await response.respond(content = "Напишите количество сообщений для удаления") #Спрашиваем у пользователя сколько сообщений нужно удалить
            amount = await client.wait_for('message', check = lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id) #получаем число из чата
            await clear(ctx, int(amount.content)) #Используя функцию, удаляем сообения в чате

    
token = os.getenv("DISCORD_TOKEN") #из перменной окружения берем токен
client.run(token) #запускаем бота