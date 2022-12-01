from locust import HttpUser, task
import random
import requests
import json
from time import sleep

numbers = [1, 0, 3456, 311313, 455356356, 52525, 66547, 77577, 90800897]


class WebsiteUser(HttpUser):

    def on_start(self):
        ret_val = self.client.post(f"token",
                         headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
                         data='grant_type=&username=user1&password=123456qwerty&scope=&client_id=&client_secret='
                         )
        self.token = ret_val.json()

    @task
    def getdate(self):
        self.client.get("date", headers={'accept': 'application/json', 'Authorization': f"Bearer {self.token}"})

    # headers = {"username": "user1", "password": "123456qwerty"

    @task
    def prime(self):
        number_choice = random.choice(numbers)
        self.client.get(url='prime/' + str(number_choice))

    @task
    def pictureInvert(self):
        in_file = open("ludzie.jpg", "rb")
        data = in_file.read()
        self.client.post(url='picture/invert/', files={'file': data})
