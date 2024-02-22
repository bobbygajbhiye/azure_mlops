import requests

url = "http://540ef4cb-5bc6-4fa5-a9ac-6e9be943cfcd.eastus.azurecontainer.io/score"

payload="{\"input\": 'I see the letter B on my car'}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
#print(response.content)
print(response.text)
