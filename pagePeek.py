#!/usr/bin/env python3

import os
import sys
import uuid
import requests
import subprocess
from urllib.parse import urlparse, urlsplit

requests.packages.urllib3.disable_warnings()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36"}


webhook_url = ""


def notify(domain, file_location=False):
	if file_location:
		with open(file_location, "rb") as file:
			data = {
				"payload_json": "{\"embeds\":[{\"description\":\"" + domain + "\", \"image\":{\"url\":\"attachment://" + file_location.split("/")[-1] + "\"}, \"color\":5298687}]}"
			}
			files = {
				"file": file
			}
			response = requests.post(webhook_url, data=data, files=files)

	else:
		data = {
			"payload_json": "{\"embeds\":[{\"description\":\"" + domain + "\", \"color\":5298687}]}"
		}
		response = requests.post(webhook_url, data=data)

	return response.status_code


def peek(url):
	uid = str(uuid.uuid4())
	file_name = f"{uid}.png"

	command = f"gowitness single {url} --fullpage -o {file_name}"
	result = subprocess.run(command, shell=True, capture_output=True, text=True)

	return file_name


def process(domain):
	if "*" in domain:
		notify(domain)

	else:
		filename = peek(f"https://{domain}")

		if os.path.exists(f"./screenshots/{filename}"):
			notify(domain, f"./screenshots/{filename}")
			os.remove(f"./screenshots/{filename}")

		else:
			notify(domain)


def main():
	for line in sys.stdin:
		process(line.strip())
		print(line.strip())

	if os.path.exists("./gowitness.sqlite3"):
		os.remove("./gowitness.sqlite3")	

if __name__ == "__main__":
	main()