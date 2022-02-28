import time
from locust import HttpUser, task, tag, between
import random, string
from urllib.parse import quote_plus


homepage = 'http://127.0.0.1:8000'
pretty_endpoint = homepage + '/pretty_echo'
minimal_endpoint = homepage + '/echo'


def random_name(length):
    name_length = length
    name = ''.join(
        [random.choice(list(string.ascii_letters + ' ')) for i in range(name_length)]
    )
    return name



class BrowserUser(HttpUser):
    # The weight is the probability to be chosen. 3 for User1 and 1 for User2 would mean 3/4 of total users will be User1 and 1/4 User2
    # This can be done with "task" decorators too : task(3)
    weight = 3
    # time in seconds between every task
    wait_time = between(1, 5)

    # ============= PRETTY ECHO ================
    @tag('pretty')
    @task
    def pretty_from_homepage(self):
        self.client.get(homepage)
        time.sleep(random.uniform(0.5, 3))
        self.client.get(url=pretty_endpoint)
        time.sleep(random.uniform(0.5, 5))
        self.client.post(url=pretty_endpoint,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data=f'name={quote_plus(random_name(random.randint(2, 50)))}')

    @tag('pretty')
    @task
    def pretty_from_endpoint(self):
        self.client.get(url=pretty_endpoint)
        time.sleep(random.uniform(0.5, 3))
        self.client.post(url=pretty_endpoint,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data=f'name={quote_plus(random_name(random.randint(2, 50)))}')


    # ============= MINIMAL ECHO ================
    @tag('minimal')
    @task
    def minimal_from_homepage(self):
        self.client.get(homepage)
        time.sleep(random.uniform(0.5, 3))
        self.client.get(url=minimal_endpoint)
        time.sleep(random.uniform(0.5, 5))
        self.client.post(url=minimal_endpoint,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data=f'name={quote_plus(random_name(random.randint(2, 50)))}')

    @tag('minimal')
    @task
    def minimal_from_endpoint(self):
        self.client.get(url=minimal_endpoint)
        time.sleep(random.uniform(0.5, 3))
        self.client.post(url=minimal_endpoint,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data=f'name={quote_plus(random_name(random.randint(2, 50)))}')


class TerminalUser(HttpUser):
    weight = 1
    wait_time = between(1, 5)
    @tag('pretty')
    @task
    def pretty_direct_post(self):
        self.client.post(url=pretty_endpoint,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data=f'name={quote_plus(random_name(random.randint(2, 50)))}')

    @tag('minimal')
    @task
    def minimal_direct_post(self):
        self.client.post(url=minimal_endpoint,
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data=f'name={quote_plus(random_name(random.randint(2, 50)))}')