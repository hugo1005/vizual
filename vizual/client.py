from time import time, sleep
import requests

# Todo Add Testing and Performance Metrics!

class Vizual:
    def __init__(self, server_ip='http://0.0.0.0:8080'):
        sleep(1)
        self._ip = server_ip
        self._channel_context = ''
        self._context_stack = []
        self._is_test = True

    def entry_point(self):
        def entry_wrapper(entry_func):
            def modified_func(*args, **kwargs):
                # Run Test Mode
                entry_func(*args, **kwargs)
                self._is_test = False

                # Run Dev Mode
                return entry_func(*args, **kwargs)
            return modified_func
        return entry_wrapper

    def _apply_decorators(self, f, d_fns):
        f_prime = f
        
        for i in range(len(d_fns) - 1,-1,-1):
            decorator = d_fns[i]
            f_prime = decorator(f_prime)

        return f_prime

    def decorate(self, test = [], dev = [], universal = []):
        def decorate_inner(f):
            _test_f = self._apply_decorators(f, test)
            _dev_f = self._apply_decorators(f, dev)

            def modified_function(*args, **kwargs):
                if self._is_test:
                    return _test_f(*args, **kwargs)
                else:
                    return _dev_f(*args, **kwargs)

            return self._apply_decorators(modified_function, universal)

        return decorate_inner

    def _register_channel(self, channel):
        requests.post(self._ip + '/channels/%s' % channel, json=None)

    def _send_debug_message(self, channel, msg):
        requests.post(self._ip + '/channels/%s' % channel, json=msg)

    def _set_channel_context(self, channel):
        self._context_stack.append(channel)

    def _get_channel_context(self):
        return self._context_stack[-1]

    def _pop_channel_context(self):
        self._context_stack.pop(-1)

    def label(self, channel):
        self._register_channel(channel)

        def label_decorator(func):
            def modified_func(*args, **kwargs):
                self._set_channel_context(channel)
                evaluation = func(*args, **kwargs)
                self._pop_channel_context()

                return evaluation
            return modified_func
        return label_decorator

    def debug(self, template, color='#fff', display_output=True): 
        def debug_decorator(func):
            def wrapper(*args, **kwargs):
                # Frist set the context
                evaluation = func(*args, **kwargs)
                content = template % evaluation if display_output else template

                msg = {
                    'timestamp': time(),
                    'message': content,
                    'format': {'color': color}
                }

                self._send_debug_message(self._get_channel_context(), msg)
                
                return evaluation
            
            return wrapper

        return debug_decorator

    def task(self, task_name, total_iters): 
        def task_decorator(func):
            def wrapper(*args, **kwargs):
                msg = {
                    'task_name': task_name,
                    'total_iters': total_iters,
                }

                requests.post(self._ip + '/task/new', json=msg)

                # Pass thru the intercepted value
                return func(*args, **kwargs)
            
            return wrapper

        return task_decorator

    def task_progress(self, increment): 
        def task_progress_decorator(func):
            def wrapper(*args, **kwargs):
                msg = {
                    'increment': increment,
                }

                requests.post(self._ip + '/task/update', json=msg)

                # Pass thru the intercepted value
                return func(*args, **kwargs)
            
            return wrapper

        return task_progress_decorator

    def ping(self, color='rgb(211,183,124)'):
        # Note pings must be run inside a @debug scope
        # Pings must wrap functions which return boolean expr.
        def ping_decorator(func):
            def wrapper(*args, **kwargs):
                criteria_met = func(*args, **kwargs)

                if criteria_met:
                    msg = {
                        'timestamp': time(),
                        'message': 'Ping!',
                        'format': {'color': color}
                    }
                    
                    requests.post(self._ip + '/channels/%s' % self._get_channel_context(), json=msg)

                return criteria_met
            return wrapper
        return ping_decorator

    def unit_test(self, unit_test_fns):
        # unit_test_fns: list of functions which accept the decorated function
        # as the only argument and returns a boolean true = passed

        def unit_test_decorator(func):
            tests = [] # Trick to ensure we only run the tests once.
            # Only wrapper gets called on each call of func()

            def wrapper(*args, **kwargs):
                if len(tests) == 0:
                    for test_fn in unit_test_fns:
                        msg = {
                            'function': func.__name__,
                            'test_name': test_fn.__name__,
                            'is_passing': test_fn(func)
                        }

                        tests.append(msg)

                    requests.post(self._ip + '/tests/%s' % self._get_channel_context(), json=tests)

                return func(*args, **kwargs)

            return wrapper
        return unit_test_decorator

    def time(self):
        def time_decorator(func):
            def wrapper(*args, **kwargs):
                channel = self._get_channel_context()
                
                a = time()
                eval = func(*args, **kwargs)
                b = time()

                msg = {
                    'function': func.__name__,
                    'duration': b - a,
                }
                    
                requests.post(self._ip + '/timing/%s' % channel, json=msg)

                return eval
            return wrapper
        return time_decorator