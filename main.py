import random
from time import sleep
from vizual.client import Vizual

vz = Vizual()

# Start Code
@vz.debug('Random Number', "The random number is %s", color='#fff')
def generate_number():
    return random.random()

@vz.debug('Random String', "The random string is %s", color='#FF0000')
def generate_string():
    return random.choice(['A','B','C'])

@vz.ping()
def choose_a_number():
    return random.choice([True, False])

@vz.debug('Generator Function', "Generating %s", color='#fff')
@vz.task_progress(1)
def generate_once():
    if choose_a_number():
        res = generate_number()
    else:
        res = generate_string()
    
    sleep(2)

    return res


@vz.task('Generating Random Numbers', 100)
def generator():
    for i in range(100):
        generate_once()

@vz.task('Some more random numbers', 100)
def generator2():
    for i in range(100):
        generate_once()

generator()
generator2()