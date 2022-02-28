import subprocess
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import cpumem
import atexit
from datetime import datetime
import sys
from typer import style, colors
from PIL import Image


srv_ip = sys.argv[1].split(':')[0] if len(sys.argv) > 1 else '127.0.0.1'
srv_port = sys.argv[1].split(':')[1] if len(sys.argv) > 1 else '8000'

def merge_results():
    cpu_mem_df = pd.read_csv('reports/cpumem.csv', index_col='Time')
    locust_df = pd.read_csv('reports/locust_test_stats_history.csv', index_col='Timestamp')
    locust_df.index.rename('Time', inplace=True)

    # Convert timestamps to time
    locust_df.index = locust_df.index.map(lambda timestamp: datetime.fromtimestamp(timestamp).strftime("%H:%M:%S"))

    # merge cpu_mem_df and locust_df
    start_time = locust_df.index[0]
    end_time = locust_df.index[-1]
    cpu_mem_df = cpu_mem_df.loc[start_time:end_time]
    df = locust_df.join(cpu_mem_df)

    # Create %Failure column
    df['%Failure'] = [
        df.iloc[i]['Failures/s'] / df.iloc[i]['Requests/s'] * 100 for i in range(len(df.index))
    ]

    # Add some units
    df.rename(columns={
        'Total Average Response Time': 'Total Average Response Time (ms)',
        'Total Median Response Time': 'Total Median Response Time (ms)',
        'Total Min Response Time': 'Total Min Response Time (ms)',
        'Total Max Response Time': 'Total Max Response Time (ms)'},
              inplace=True)

    # save final data
    df.to_csv('reports/performance.csv')
    print(style(f'Performance data saved at {"reports/performance.csv"}', fg=colors.GREEN))
    df[
        ['Requests/s', 'Failures/s']
    ].plot(kind='line', title='Requests and Failure rates depending on user load', figsize=(18, 6)).get_figure().savefig('reports/Req-Fail Rate.jpg')
    df[
        ['Total Average Response Time (ms)', 'Total Median Response Time (ms)']
    ].plot(kind='line', title='Response time depending on user load', figsize=(18, 6)).get_figure().savefig('reports/Response Time.jpg')
    df[
        ['%Failure', '%CPU', '%MEM']
    ].plot(kind='line', title='% Metrics', figsize=(18, 6)).get_figure().savefig('reports/% Metrics.jpg')

    images = [
        Image.open("reports/" + f)
        for f in ["Req-Fail Rate.jpg", "Response Time.jpg", "% Metrics.jpg"]
    ]
    images[0].save(
        'reports/Charts.pdf', "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )
    print(style(f'Performance chart saved at {"reports/Charts.pdf"}', fg=colors.GREEN))
    print(style('DONE.', fg=colors.CYAN))


atexit.register(merge_results)
executor = ThreadPoolExecutor()
executor.submit(cpumem.run, 'reports/cpumem.csv', srv_port)
print(style('Starting locust ...', fg=colors.CYAN))
print(f'Click {style("http://127.0.0.1:8089", fg=colors.GREEN)} for real time stats and UI')
executor.submit(subprocess.Popen,
                f'locust --autostart -f locustfile.py --logfile log/locust.log \
                --csv reports/locust_test\
                --html reports/locust_report.html \
                --print-stats \
                --host {srv_ip}:{srv_port} \
                --users 10000 \
                --spawn-rate 2 \
                -T pretty minimal\
                BrowserUser \
                TerminalUser'
                .split())
