from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Har request ke beech 1-3 sec wait

    @task
    def test_homepage(self):
        self.client.get("/")  # Homepage pe request

    @task
    def test_specific_page(self):
        self.client.get("/some-page")  # Koi aur page jo test karna chahta hai

# Agar login wali site hai, toh login task add kar sakta hai
# def on_start(self):
#     self.client.post("/login", {"username": "test", "password": "test"})