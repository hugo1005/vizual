#(trap 'kill 0' SIGINT; python3 `pwd`/$1 & python3 `dirname $0`/server.py)

import os
import docopt

def main():
    args = docopt.docopt(__doc__)
    print(args)
    target = args['--exec'] # something.py filepath relative to the terminal.
    server = os.path.dirname(__file__) + '/server.py'

    cmd = "(trap 'kill 0' SIGINT; python3 " + target + " & python3 " + server + ")"

    os.system(cmd)

if __name__ == '__main__':
    main()