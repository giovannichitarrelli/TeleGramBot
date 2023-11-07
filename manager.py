import requests
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle, pyfiglet
from colorama import init, Fore
import os, random
from time import sleep
import time
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.messages import SendMessageRequest
import csv


init()

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]

info = lg + '[' + w + 'i' + lg + ']' + n
error = lg + '[' + r + '!' + lg + ']' + n
success = w + '[' + lg + '*' + w + ']' + n
INPUT = cy + '[' + cy + '~' + lg + ']' + n
plus = lg + '[' + w + '+' + lg + ']' + n


def banner():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram')
    print(f'{random.choice(colors)}{banner}{n}')
    print(r+'  Version: 1.2 | Author: Giovanni'+n+'\n')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True:
    clr()
    #print(r)
    banner()
    #print(n)
    print(f'{ye}[1] {lg}Add new accounts'+n)
    print(f'{ye}[2] {lg}Filter all banned accounts'+n)
    print(f'{ye}[3] {lg}List out all the accounts'+n)
    print(f'{ye}[4] {lg}Delete specific accounts'+n)
    print(f'{ye}[5] {lg}Extract Contacts from group'+n) ##aqui
    #print(lg+'[5] Update your Genisys'+n)
    print(f'{ye}[6] {lg}Send Messages'+n) ##aqui
    print(f'{ye}[7] {lg}Add contacts on channel'+n) #aqui
    print(f'{ye}[8] {lg}Quit')
    a = int(input(f'\nEnter your choice: {r}'))
    if a == 1:
        with open('vars.txt', 'ab') as g:
            newly_added = []
            while True:
                a = int(input(f'\n{lg}Enter API ID: {r}'))
                b = str(input(f'{lg}Enter API Hash: {r}'))
                c = str(input(f'{lg}Enter Phone Number: {r}'))
                p = ''.join(c.split())
                pickle.dump([a, b, p], g)
                newly_added.append([a, b, p])
                ab = input(f'\nDo you want to add more accounts?[y/n]: ')
                if 'y' in ab:
                    pass
                else:
                    print('\n'+lg+'[i] Saved all accounts in vars.txt'+n)
                    g.close()
                    sleep(3)
                    clr()
                    print(lg + '[*] Logging in from new accounts...\n')
                    for added in newly_added:
                        c = TelegramClient(f'sessions/{added[2]}', added[0], added[1])
                        try:
                            c.start()
                            print(f'n\n{lg}[+] Logged in - {added[2]}')
                            c.disconnect()
                        except PhoneNumberBannedError:
                            print(f'{r}[!] {added[2]} is banned! Filter it using option 2')
                            continue
                        print('\n')
                    input(f'\n{lg}Press enter to goto main menu...')
                    break
        g.close()
    elif a == 2:
        accounts = []
        banned_accs = []
        h = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
        if len(accounts) == 0:
            print(r+'[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            for account in accounts:
                api_id = int(account[0])
                api_hash = str(account[1])
                phone = str(account[2])
                client = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        client.sign_in(phone, input('[+] Enter the code: '))
                    except PhoneNumberBannedError:
                        print(r+str(phone) + ' is banned!'+n)
                        banned_accs.append(account)
            if len(banned_accs) == 0:
                print(lg+'Congrats! No banned accounts')
                input('\nPress enter to goto main menu')
            else:
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Id = a[0]
                        Hash = a[1]
                        Phone = a[2]
                        pickle.dump([Id, Hash, Phone], k)
                k.close()
                print(lg+'[i] All banned accounts removed'+n)
                input('\nPress enter to goto main menu')
    elif a == 3:
        display = []
        j = open('vars.txt', 'rb')
        while True:
            try:
                display.append(pickle.load(j))
            except EOFError:
                break
        j.close()
        print(f'\n{lg}')
        print(f'API ID  |            API Hash              |    Phone')
        print(f'==========================================================')
        i = 0
        for z in display:
            print(f'{z[0]} | {z[1]} | {z[2]}')
            i += 1
        print(f'==========================================================')
        input('\nPress enter to goto main menu')  
    elif a == 4:
        accs = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}[i] Choose an account to delete\n')
        for acc in accs:
            print(f'{lg}[{i}] {acc[2]}{n}')
            i += 1
        index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
        phone = str(accs[index][2])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
        del accs[index]
        f = open('vars.txt', 'wb')
        for account in accs:
            pickle.dump(account, f)
        print(f'\n{lg}[+] Account Deleted{n}')
        input(f'{lg}Press enter to goto main menu{n}')
        f.close()
    elif a == 5:
        import scraper
        scraper.init()
    elif a == 6:

        init()
        users = []
        input_file = 'members/members.csv'  # Adjust the file path as needed

        # Load member data from CSV
        with open(input_file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f, delimiter=',', lineterminator='\n')
            next(reader, None)
            for row in reader:
                user = {}
                user['username'] = row[0]
                user['user_id'] = row[1]
                user['access_hash'] = row[2]
                user['group'] = row[3]
                user['group_id'] = row[4]
                users.append(user)

        # # Create a session for each account and send messages
        # accounts = []
        # f = open('vars.txt', 'rb')
        # while True:
        #     try:
        #         accounts.append(pickle.load(f))
        #     except EOFError:
        #         break
        # f.close()

        # # Iterate through the user accounts
        # for account in accounts:
        #     f = open('vars.txt', 'rb')
        #     accs = []
        #     while True:
        #         try:
        #             accs.append(pickle.load(f))
        #         except EOFError:
        #             f.close()
        #             break
        #     print(f'{INPUT}{cy} Choose an account to send message members\n')
        #     i = 0
        #     for acc in accs:
        #         print(f'{lg}({w}{i}{lg}) {acc[2]}')
        #         i += 1
        #     ind = int(input(f'\n{INPUT}{cy} Enter choice: '))
        #     api_id = accs[ind][0]
        #     api_hash = accs[ind][1]
        #     phone = accs[ind][2]

        #     c = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
        #     c.connect()

        #     # Check if the client is authorized
        #     if not c.is_user_authorized():
        #         try:
        #             c.send_code_request(phone)
        #             code = input(f'{INPUT}{cy} Enter code for {w}{phone}{cy} (s to skip): {r}')
        #             if 's' in code:
        #                 continue

        #             client.sign_in(phone, code)
        #         except PhoneNumberBannedError:
        #             print(f'{error}{w}{phone} {r}is banned!{n}')
        #             continue

        #     message_count = 0   
        #     tempo_inicial = 30
        #     tempo_ban = 180
        #     for user in users:
        #         try:
        #             # Enviar sua mensagem aqui
        #             message = open('message.txt', 'r', encoding='utf-8').read()
        #             input_peer = InputPeerUser(int(user['user_id']), int(user['access_hash']))
        #             c(SendMessageRequest(input_peer, message))
        #             print(f'{success}{lg} Message sent from {phone} to {cy}{user["username"]} {user["user_id"]}{n}')
                    
        #             message_count = message_count + 1 
        #             print(f"contador: {message_count}")

        #             if message_count % 6 == 0:
        #                 # print(f"{r}Waiting 180 seconds...")
        #                 # time.sleep(180)  
        #                 while tempo_inicial > 0:
        #                     print(f"{ye}Aguarde {tempo_ban} segundos para prevenir banimentos...")
        #                     time.sleep(1)  # Espera 1 segundo
        #                     tempo_inicial -= 1
        #             else:
        #                 # print(f"{r}Waiting 40 seconds...")
        #                 # time.sleep(40)  
        #                 while tempo_inicial > 0:
        #                     print(f"{ye}Aguarde {tempo_inicial} segundos...")
        #                     time.sleep(1)  # Espera 1 segundo
        #                     tempo_inicial -= 1


        #         except Exception as e:
        #             print(f'{error}{r} Error sending message to {w}{user["username"]}: {str(e)}{n}')
        #             # break
        #             time.sleep(10)

                
        #     c.disconnect()
        # print(f'{info} All messages sent successfully!{n}')










        import time
        from telethon.sync import TelegramClient
        from telethon.tl.functions.messages import SendMessageRequest
        from telethon.tl.types import InputPeerUser
        import pickle

        # Load user accounts from vars.txt
        accounts = []
        with open('vars.txt', 'rb') as f:
            while True:
                try:
                    accounts.append(pickle.load(f))
                except EOFError:
                    break

        # Iterate through the user accounts
        # for account in accounts:
        #     api_id, api_hash, phone = account
        #     c = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
        #     c.connect()

        #     # Check if the client is authorized
        #     if not c.is_user_authorized():
        #         try:
        #             c.send_code_request(phone)
        #             code = input(f'Enter code for {phone} (s to skip): ')
        #             if 's' in code:
        #                 continue

        #             c.sign_in(phone, code)
        #         except PhoneNumberBannedError:
        #             print(f'{phone} is banned!')
        #             continue

        for account in accounts:
            f = open('vars.txt', 'rb')
            accs = []
            while True:
                try:
                    accs.append(pickle.load(f))
                except EOFError:
                    f.close()
                    break
            print(f'{INPUT}{cy} Choose an account to send message members\n')
            i = 0
            for acc in accs:
                print(f'{lg}({w}{i}{lg}) {acc[2]}')
                i += 1
            ind = int(input(f'\n{INPUT}{cy} Enter choice: '))
            api_id = accs[ind][0]
            api_hash = accs[ind][1]
            phone = accs[ind][2]

            c = TelegramClient(f'sessions\\{phone}', api_id, api_hash)
            c.connect()

            # Check if the client is authorized
            if not c.is_user_authorized():
                try:
                    c.send_code_request(phone)
                    code = input(f'{INPUT}{cy} Enter code for {w}{phone}{cy} (s to skip): {r}')
                    if 's' in code:
                        continue

                    client.sign_in(phone, code)
                except PhoneNumberBannedError:
                    print(f'{error}{w}{phone} {r}is banned!{n}')
                    continue

            message_count = 0
            
            

            for user in users:
                try:
                    # Enviar sua mensagem aqui
                    message = open('message.txt', 'r', encoding='utf-8').read()
                    input_peer = InputPeerUser(int(user['user_id']), int(user['access_hash']))
                    c(SendMessageRequest(input_peer, message))
                    print(f'{lg}SUCESSO! Message sent from {cy}{phone} to {user["username"]} {user["user_id"]}')

                    message_count = message_count + 1
                    print(f"contador: {message_count}")

                    if message_count % 5 == 0:
                        tempo_ban = 180
                        while tempo_ban > 0:
                            print(f"{ye}Aguarde {tempo_ban} segundos para prevenir banimentos...", end='\r')
                            time.sleep(1)
                            tempo_ban -= 1
                    else:
                        tempo_inicial = 30
                        while tempo_inicial > 0:
                            print(f"{ye}Aguarde {tempo_inicial} segundos...", end='\r')
                            time.sleep(1)
                            tempo_inicial -= 1
                        print(" " * 40, end='\r')  # Limpa a linha após a contagem regressiva
                    print()  # Para imprimir uma nova linha após a conclusão

                except Exception as e:
                    print(f'{r}Error sending message to {user["username"]}: {str(e)}')
                    time.sleep(10)

            c.disconnect()

        print(f'{info} All messages sent successfully!{n}')




    elif a == 7:
        import tsadder
        tsadder.init()
    elif a == 8:
        clr()
        banner()
        quit()