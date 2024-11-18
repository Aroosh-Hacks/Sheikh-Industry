import requests

url = input('Enter the URL: ')

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print('Error:', response.status_code)