import requests

url = "http://540ef4cb-5bc6-4fa5-a9ac-6e9be943cfcd.eastus.azurecontainer.io/score"

payload="{\"SepalLengthCm\": 6.6, \"SepalWidthCm\": 3, \"PetalLengthCm\": 4.4, \"PetalWidthCm\": 1.4}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
#print(response.content)
print(response.text)