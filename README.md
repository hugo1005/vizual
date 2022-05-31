# Vizual
- A CLI and Web UI for making print statement based debugging makes it easy to manage large diagnostic outputs from complex dev systems.

- A @decorator based syntax for vizual won't leave you hunting for that last print() you still can't seem to spot hiding in your code! 

![Vizual](markdown_screenshots/screenshot.png?raw=true "Powerful web based print statement debugging environment for python")

### Features
- Command line interface + Web UI
- Multi channel console logs (+ Multi color)
- If statement condition met checks (Pings)
- Progress bars for tasks
- Code timing / performance metrics
- Unit test pass / fail
- Decorator syntax for python

## Installation

To install
```
pip install vizual
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
@vz.decorate(
 dev = [vz.debug("descriptive text for output: %s", color='#fff')]
 universal = [vz.label("channel_name")]
)
def f(...):
  return ...
```

We can also display pandas tables and matplotlib figures using the following options. 
Tables and figures may be placed on any channel.
Options for tables can be specified for the summary_fn used (default is a wrapper of df.head())
```
@vz.decorate(
    dev = [vz.table("Random Table Example")],
    universal = [vz.label('Tables')]
)
def make_table():
    return pd.DataFrame(np.random.normal(0,1, (100,10)))

@vz.decorate(
    dev = [vz.figure("example_fig")],
    universal = [vz.label('Figures')]
)
def make_figure():
    fig = plt.figure()
    
    x = np.linspace(0,10,50)
    err = np.random.normal(0,1, 50)
    y = 5 * x + err
    z = 10 * x * y + err
    plt.subplot2grid((1,2),(0,0))
    plt.plot(x,y)
    plt.subplot2grid((1,2),(0,1))
    plt.plot(x,z)
    return fig
```

### Unit Testing in here
![Vizual](markdown_screenshots/screenshot2.png?raw=true "Powerful web based print statement debugging environment for python")

We have 3 types of decorations in vizual, test, dev and universal. 
Decorators listed under test will be run in a seperate test environment to prevent side effects.
Universal decorators will be applied to both test run and development run. Thus it is important that the channel
label is always universal.

Unit testing accepts a list of test functions which accept the function to be tested as the only input.
Unit tests will then be visible in the web ui under the appropriate channel labels as either passing or failing.

```
@vz.decorate(
 test = [vz.unit_test([my_passing_test, my_failing_test])]
 dev = [vz.debug("descriptive text for output: %s", color='#fff')],
 universal = [vz.label("channel_name")]
)
def f(...):
  return ...
```



### Checking if a condition was met (Pinging)
We can wrap a boolean function in a ping decorator, the function will 'Ping!' every time the condition is true.
Note that pings will be made on the parent channel which may be several function calls higher.

```
@vz.decorate(
  dev = [vz.ping()]
)
def condition_met(...):
  return [True or False]
  
@vz.decorate(
 dev = [vz.debug("descriptive text for output: %s", color='#fff')],
 universal = [vz.label("channel_name")]
)
def f(...):
  
  if condition_met(...):
    ... this code gets triggered
```

### Loading bars
We can mark functions as tasks, naming the task and specifying any float or integer as the amount of work todo.
We can then label functions within the task with the task_progress decorator and specify the increment they contribute.

```
@vz.decorate(
 dev = [vz.task_progress(some_increment)],
)
def do_step(...):
  return ...

@vz.decorate(
 dev = [vz.task(task_name, total_iters)],
)
def f(...):
  do_step(...)
  return ...
```

### Performance Monitoring
We can register functions for performance monitoring using vz.time().
Please make sure that if you have multiple decorators that time() is the last one
otherwise you will also be measuring the performance of the wrapper which includes POST
requests to the flask server. 

Make sure that the function being timed is labelled with a debug channel or that some parent function call is a channel member otherwise you may experience strange behaviour.

```
@vz.decorate(
 dev = [vz.debug("descriptive text for output: %s", color='#fff'), vz.time()],
 universal = [vz.label("channel_name")]
)
def f(...):
  return ...
```

## Running Vizual

### Command Line Interaface
Navigate to your python file in the terminal and run

```
vizual --file file_to_debug.py
```

### Accessing the web app
Open http://0.0.0.0:8080 in your browser!

### Terminating CLI
Use ctrl-c as usual, note the termination is not particularly graceful currently but functional.

## Example application:
See example.py!