
from locust import HttpUser, task
import random

numbers = [1, 0, 3456, 311313, 455356356, 52525, 66547, 77577, 90800897]

class WebsiteUser(HttpUser):

    @task
    def getdate(self):
        self.client.get(url='date/', headers={"Authorization": "token"})

        #headers = {"username": "user1", "password": "123456qwerty"

    @task
    def prime(self):
        number_choice = random.choice(numbers)
        self.client.get(url='prime/' + str(number_choice))

    @task
    def pictureInvert(self):
        in_file = open("ludzie.jpg", "rb")
        data = in_file.read()
        self.client.post(url='picture/invert/', files={'file': data})
