import os
import requests
import ctypes
import threading
import time
from colorama import Fore, init
import random
import string
from discord_webhook import DiscordWebhook
from core.localscommands import clear, pause, title

init()


def start():
	global webhookk
	clear()
	webhookk = ""
	webhookk = input("Webhook: ")
	if webhookk == "":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	elif webhookk == " ":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	clear()
	global extension
	extension = ""
	extension = input("Image Extension: ")
	if extension == "":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	elif extension == " ":
		print("The value you entered was null. Please try again.")
		pause()
		start()
		return
	if "." in extension:
		pass
	else:
		print(Fore.RED + "[!] Please enter a valid extension.")
		pause()
		clear()
		start()
		return
	clear()

available = 0
taken = 0 
total = 0
errorCodes = [100, 101, 103, 201, 202, 203, 204, 205, 206, 300, 301, 303, 304, 308, 400, 401, 402, 403, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 422, 425, 426, 428, 431, 451, 500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]

def getProxy():
	global proxList
	global proxList2
	prox = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=no&anonymity=all")
	if prox.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()	
		exit()
	proxyTxt = prox.text.splitlines()
	proxList = []
	for line in proxyTxt:
		proxList.append(line)
	prox2 = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=US&ssl=yes&anonymity=all")
	if prox2.text == "You have reached your hourly maximum API requests of 750.":
		print("Please wait an hour before running this script again.")
		pause()
		exit()
	proxyTxt2 = prox2.text.splitlines()
	proxList2 = []
	for line in proxyTxt2:
		proxList2.append(line)
	

def main():
	getProxy()
	while True:
		thread = threading.Thread(target=checkLink, daemon=True)
		thread.start()
		time.sleep(0.1)

def checkLink():
	global taken
	global available
	global total
	global randProxy
	global randProxySSL
	randProxy = random.choice(proxList)
	randProxySSL = random.choice(proxList2)
	lowerLetters = string.ascii_lowercase
	upperLetters = string.ascii_uppercase
	digits = string.digits
	randomCode = ''.join(random.choice(lowerLetters + upperLetters + digits) for i in range(7))
	code = randomCode
	try:
		imgurRequest = requests.get(f"https://i.imgur.com/{code}{extension}", proxies={"http": randProxy,"https": randProxySSL}, allow_redirects=True)
	except Exception as e:
		#print(e)
		return;
	if imgurRequest.url == "https://i.imgur.com/removed.png":
		taken += 1
		total += 1
		ctypes.windll.kernel32.SetConsoleTitleW("Imgur Generator | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.RED + f"[-] Link 'https://i.imgur.com/{code}{extension}' is invalid.")
	else:
		available += 1
		total += 1
		ctypes.windll.kernel32.SetConsoleTitleW("Imgur Generator | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.GREEN + f"[+] Link 'https://i.imgur.com/{code}{extension}' is valid.")
		webhook = DiscordWebhook(url=webhookk, content=f'Valid Link:\nhttps://i.imgur.com/{code}{extension}')
		try:
			response = webhook.execute()
		except Exception:
			print(Fore.YELLOW + "Invalid Webhook URL, saving invite to valid.txt")
			with open("valid.txt", "a") as f:
				f.writelines(f'i.imgur.com/{code}{extension}' + "\n")
	if imgurRequest.status_code == 429:
		total += 1
		ctypes.windll.kernel32.SetConsoleTitleW("Imgur Generator | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] You are being ratelimited, changing proxies.")
		#print(randProxy)
		checkLink()
	elif imgurRequest.status_code in errorCodes:
		total += 1
		ctypes.windll.kernel32.SetConsoleTitleW("Imgur Generator | arshan.xyz | Valid: " + str(available) +  " Invalid: " + str(taken) + " Total: " + str(total))
		print(Fore.YELLOW + "[!] An unexpected error has occured. Error Code: " + str(imgurRequest.status_code))

def menu():
	ctypes.windll.kernel32.SetConsoleTitleW("Imgur Generator | arshan.xyz")
	main()

if __name__ == "__main__":
	start()
	menu()
