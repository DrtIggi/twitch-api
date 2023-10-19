import asyncio
import socket
import ssl
import random
import sqlite3
import messages


async def join_stream(access_token, nickname=''):
    server = 'irc.chat.twitch.tv'
    port = 6697
    irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_socket = ssl.wrap_socket(irc_socket)

    token = access_token
    channel = '' 

    while True:
        await asyncio.sleep(10)
        irc_socket.connect((server, port))
        irc_socket.send(f'PASS oauth:{token}\n'.encode())
        irc_socket.send(f'NICK {nickname}\n'.encode())
        irc_socket.send(f'JOIN #{channel}\n'.encode())

        message = random.choice(messages.words)
        irc_socket.send(f'PRIVMSG #{channel} :{message}\n'.encode())
        irc_socket.close()
        await asyncio.sleep(10)


async def main():
    db = sqlite3.connect("db.db")
    cursor = db.cursor()
    cursor.execute("SELECT token FROM tokens")
    tokens = cursor.fetchall()
    tasks = []

    for token in tokens:
        task = asyncio.create_task(join_stream(token))
        tasks.append(task)

    await asyncio.gather(*tasks)

asyncio.run(main())