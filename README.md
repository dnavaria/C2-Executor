# C2 - Executor

- Clone repository: `https://github.com/dnavaria/C2-Executor`

## Server - API Server & Supabase

- To Setup API Server & Supabase, you need to have docker compose installed
    - Change directory to `deployment/`
    - Run `docker compose up -d`
    - Supabase will be accessible on `http://localhost:8000`
    - API Server Docs are available on `http://localhost:11999`


## BG - Worker 
- Clone the git repository where you want the commands to be executed
- To setup BG - Worker
    - You need to have pip3 and pytohn3 on your system
    - Install Dependency: `pip3 install -r requirements.txt`
    - Run the worker using following command: `python3 run_worker.py`
    - If API Server is running on different machine, then make sure to change the config in .env file inside `bg-worker` diretory

## Client - UI

- To setup client ui on local machine:
    - Change Directory to client
    - Install dependency: `npm install .`
    - To run UI Server:
        - `npm run dev`