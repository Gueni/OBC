import psutil

def kill_all_plecs_processes():
    # Flag to check if any processes were found
    processes_killed = False
    
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # Check if process name matches 'PLECS.exe'
            if proc.info['name'] == 'PLECS.exe':
                # Kill the process
                proc.kill()
                print(f"Process {proc.info['name']} with PID {proc.info['pid']} has been killed.")
                processes_killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if not processes_killed:
        print("No instances of PLECS.exe were found.")
    else:
        print("All instances of PLECS.exe have been killed.")

# Call the function
kill_all_plecs_processes()
