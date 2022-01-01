import random
from time import sleep
from vizual.client import Vizual

vz = Vizual()

# Start Code
@vz.debug('Random Number', "The random number is %s", color='#fff')
@vz.time()
def generate_number():
    return random.random()

@vz.debug('Random String', "The random string is %s", color='#FF0000')
@vz.time()
def generate_string():
    return random.choice(['A','B','C'])

@vz.ping()
def choose_a_number():
    return random.choice([True, False])

@vz.debug('Generator Function', "Generating %s", color='#fff')
@vz.task_progress(1)
@vz.time()
def generate_once():
    if choose_a_number():
        res = generate_number()
    else:
        res = generate_string()
    
    sleep(0.05)

    return res

@vz.task('Generating Random Numbers', 100)
@vz.time()
def generator():
    for i in range(100):
        generate_once()

@vz.task('Some more random numbers', 100)
@vz.time()
def generator2():
    for i in range(100):
        generate_once()

@vz.debug('Main', "Main call", color='#fff', display_output=False)
def main():
    generator()
    generator2()

if __name__ == '__main__':
    main()