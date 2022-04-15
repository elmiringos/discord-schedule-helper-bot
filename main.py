import discord    
from discord.ext import commands
from discord.utils import get
from discord_components import DiscordComponents, Button, ButtonStyle

from time_table import get_schedule
import datetime
  
import os
from dotenv import load_dotenv  #Импортируем все необходимые библиотеки и модули

load_dotenv()

client = commands.Bot(command_prefix='!') #Создаем тело бота и добавляем префик для наших команд


@client.event #Создаем события
async def on_ready(): #навзвание "on_ready" обозначает, что данная функция будет выполняться при каждом включении бота
    DiscordComponents(client) #Используем эту функцию, для добавления кнопок в бота
    print('We have logged in as {0.user}'.format(client)) #Чтобы отслеживать включение, добавляем эту строку


@client.event #Создаем события
async def on_member_join(ctx, member): #навзвание "on_member_join" обозначает, что данная функция будет выполняться при каждом заходе нового пользователя на сервер
    channel = client.get_channel(802427814154207255) #находим нужный голосовой канал по id
    role = ctx.guild.get_role(961990701741133834) #находим нужную роль
    await member.add_roles(role) #добавляем роль новому пользователю
    user_id = member.id #получаем id нового пользователя 
    await user_id.send("Напишите свое имя и фамилию") #Спрашиваем Имя и Фамилию пользователя
    new_nickname = await client.wait_for('message', check = lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id) #получаем Имя и Фамилию пользователя
    await member.edit(nick=new_nickname) #изменяем ник пользователю на  Имя и Фамилию 
    await ctx.send(f'Nickname was changed for {member.mention} ') 


def check_audience(ctx): #функция для проверки количества отсутсвующих
    channel = client.get_channel(962426692796825621) #находим нужный голосовой канал по id
    members_of_channel = channel.members #получаем количество пользователей, находящихся в голосовом канале
    role = ctx.guild.get_role(961990701741133834) #находим нужную роль
    members_of_guild = role.members #получаем количество пользователей нужной роли
    if len(members_of_channel) == 0: # провереям количество пользователей, если =0, то просто выводим количество всей участников выбранной роли
        return (f"Количество отсутствующих - {len(members_of_guild)}")
    diff = len(members_of_guild) - (len(members_of_channel) - 1) #сохраняем в переменную "diff" количество отсутсвующих
    return (f"Количество отсутствующих - {diff}") #возвращаем f строкой


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
            Button(style = ButtonStyle.blue, label = "Очистить чат"),
            Button(style = ButtonStyle.blue, label = "Количество отсутствующих")                
        ]
    )
    response = await client.wait_for("button_click") #создаем реакцию на нажатие кнопки
    if response.channel == ctx.channel: #проверяем на какую кнопку нажал пользователь
        if response.component.label == "Расписание на сегодня": 
            await response.respond(content = "Напишите название группу") #Спрашиваем у пользователя название группы
            group = await client.wait_for('message', check = lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id) #считываем название группы из чата
            await schedule(ctx, group.content) #Используя функцию, выводим расписание
        elif response.component.label == "Начать занятие":
            await ctx.channel.send(content = "@everyone Преподователь начал занятие") #используем упоминание всех пользователей
        elif response.component.label == "Очистить чат":
            await response.respond(content = "Напишите количество сообщений для удаления") #Спрашиваем у пользователя сколько сообщений нужно удалить
            amount = await client.wait_for('message', check = lambda m: m.channel == ctx.channel and m.author.id == ctx.author.id) #получаем число из чата
            await clear(ctx, int(amount.content)) #Используя функцию, удаляем сообения в чате
        elif response.component.label == "Количество отсутствующих": 
            answer = check_audience(ctx) #вызываем функция для проверки количества отсутсвующих
            await response.respond(content = answer) #выводим количества отсутсвующих в личное сообщение

    
token = os.getenv("DISCORD_TOKEN") #из переменной окружения берем токен
client.run(token) #запускаем бота