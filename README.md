# Deploy
1- Clone the repository

    git clone https://github.com/midnight-repo/PerfTest.git && cd PerfTest

2- Create virtual environment if needed:

    python3 -m venv venv
    source venv/bin/activate
    
3- Install dependencies

    pip3 install -r requirements.txt 

4- Before running the test, please open and read the jupyter notebooks (don't forget to run the codes : click "Kernel" on the menu bar, and select "Restart & Run All") as they contain useful information about the test, tools, configuration tips, and analysis of the data sample.

    jupyter notebook # /!\  Please make sure to run this command from the PerfTest directory /!\ 

5- Run the server :

    python3 serv.py # /!\ Please make sure you run this command from the part1 directory /!\
    
6- Run the performance test for the server

    python3 run.py # /!\ Please make sure you run this command from the part2 directory /!\

