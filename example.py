import random
from time import sleep
from vizual.client import Vizual
from example_unit_tests import gen_type_check, gen_range_check, len_output_check, failing_test
import numpy as np
import pandas as pd

vz = Vizual()

# Start Code
@vz.decorate(
    dev = [
        vz.debug("The random number is %s", color='#fff'),
        vz.time()
    ],
    universal = [vz.label('Random Number')]
)
def generate_number():
    return random.random()

@vz.decorate(
    dev = [
        vz.debug("The random string is %s", color='#FF0000'),
        vz.time()
    ],
    universal = [vz.label('Random String')]
)
def generate_string():
    return random.choice(['A','B','C'])

@vz.decorate(
 dev = [vz.ping()]
)
def choose_a_number():
    return random.choice([True, False])

@vz.decorate(
    test = [vz.unit_test([gen_type_check, gen_range_check])],
    dev = [
        vz.debug("Generating %s", color='#fff'),
        vz.task_progress(1), 
        vz.time()
    ],
    universal = [vz.label('Generator Function')]
)
def generate_once(gen_number = True):
    if gen_number:
        res = generate_number()
    else:
        res = generate_string()

    return res

@vz.decorate(
    test = [vz.unit_test([len_output_check, failing_test])],
    dev = [vz.task('Generating Random Numbers', 100),vz.time()]
)
def generator(n=100):
    l = []
    for i in range(n):
        l.append(generate_once(gen_number = choose_a_number()))

    return l

@vz.decorate(
    dev = [vz.task('Some more random numbers', 100),vz.time()]
)
def generator2(n=100):
    for i in range(n):
        generate_once(gen_number = choose_a_number())

@vz.decorate(
    dev = [vz.table("Random Table Example")],
    universal = [vz.label('Tables')]
)
def make_table():
    return pd.DataFrame(np.random.normal(0,1, (100,10)))

@vz.decorate(
    dev = [vz.debug("Done", color='#fff', display_output=False)],
    universal = [vz.entry_point(), vz.label('Main')]
)
def main():
    generator()
    generator2()
    make_table()

if __name__ == '__main__':
    main()
