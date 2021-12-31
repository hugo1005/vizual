# Vizual
Web based debug tools for easy cleant statement based debugging in python.

## Installation

To install
```
pip install git+https://github.com/hugo1005/vizual.git
```

To uninstall 
```
pip uninstall vizual
```

## User Guide
Import the client into your python file

```
from vizual.client import Vizual
vz = Vizual()
```

### Logging function outputs to a channel
Log the output of a function to a channel. Note if a function returns a tuple 
you must have enough %s in the format string.

If a function has no output the argumet display_output=False may be used.

```
@vz.debug("channel_name", "descriptive text for output: %s", color='#fff')
def f(...):
  return ...
```

### Checking if a condition was met (Pinging)
We can wrap a boolean function in a ping decorator, the function will 'Ping!' every time the condition is true.
Note that pings will be made on the parent channel which may be several function calls higher.

```
@vz.ping()
def condition_met(...):
  return [True or False]
  
@vz.debug("channel_name", "descriptive text for output: %s", color='#fff')
def f(...):
  
  if condition_met(...):
    ... this code gets triggered
```

### Loading bars
We can mark functions as tasks, naming the task and specifying any float or integer as the amount of work todo.
We can then label functions within the task with the task_progress decorator and specify the increment they contribute.

```
@vz.task_progress(some_increment)
def do_step(...):
  return ...

@vz.task(task_name, total_iters)
def f(...):
  do_step(...)
  return ...
```

### Accessing the web app
Open http://0.0.0.0:8080 in your browser!

## Example application:
```
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


```
