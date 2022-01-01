from time import time, sleep
import requests

# Todo Add Testing and Performance Metrics!

class Vizual:
    def __init__(self, server_ip='http://0.0.0.0:8080'):
        sleep(1)
        self._ip = server_ip
        self._channel_context = ''
        self._context_stack = []

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

    def debug(self, channel, template, color='#fff', display_output=True): 
        self._register_channel(channel)

        def debug_decorator(func):
            def wrapper(*args, **kwargs):
                # Frist set the context
                self._set_channel_context(channel)
                evaluation = func(*args, **kwargs)
                self._pop_channel_context()

                content = template % evaluation if display_output else template

                msg = {
                    'timestamp': time(),
                    'message': content,
                    'format': {'color': color}
                }

                self._send_debug_message(channel, msg)
                
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

    def time(self):
        def time_decorator(func):
            def wrapper(*args, **kwargs):
                channel = self._get_channel_context()
                
                a = time()
                eval = func(*args, **kwargs)
                b = time()

                msg = {
                    'channel': channel,
                    'function': func.__name__,
                    'duration': b - a,
                }
                    
                requests.post(self._ip + '/timing', json=msg)

                return eval
            return wrapper
        return time_decorator