import subprocess
import time
from typer import style, colors

def run(outfile, server_port):
    # The server port is needed to find the pid of the server

    print(style('Starting the %CPU/%Mem capture ...', fg=colors.CYAN))

    # Create outfile
    f = open(outfile, 'w')
    f.write('Time,%CPU,%MEM\n')
    f.close()

    # Get pid of the server so we can see its resource usage
    server_pid = subprocess.getoutput(f'lsof -i :{server_port}').split('\n')[1].split()[1].strip()

    while True:
        cpu, mem = tuple(x for x in subprocess.getoutput(f'ps -p {server_pid} -o %cpu,%mem').split('\n')[1].split(' ') if not x == '')
        t = time.strftime("%H:%M:%S")
        with open(outfile, 'a') as f:
            f.write(f'{t},{cpu},{mem}\n')
            f.close()
        time.sleep(1)
