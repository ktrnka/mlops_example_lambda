from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(0.5, 5)

    @task
    def sports(self):
        self.client.post("/", json={"text": "The Seattle Seahawks crushed the Cleveland Browns on Thursday 52-7"})

    @task
    def politics(self):
        self.client.post("/", json={"text": "Obama criticized Russia's air strikes on Syria last night"})

    @task
    def science(self):
        self.client.post("/", json={"text": "SpaceX SN11 had an unsuccessful launch from Boca Chica last night"})
