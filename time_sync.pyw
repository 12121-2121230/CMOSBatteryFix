import subprocess
import time
import ctypes
import sys
import os
import msvcrt

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def setup_task_scheduler():
    script_path = os.path.abspath(__file__)
    task_name = "StealthTimeSync"
    # Use pythonw.exe to ensure it runs without a console window
    python_exe = sys.executable.replace("python.exe", "pythonw.exe")
    
    check_task = subprocess.run(['schtasks', '/query', '/tn', task_name], 
                                capture_output=True, creationflags=0x08000000)
    
    if check_task.returncode != 0:
        create_cmd = ['schtasks', '/create', '/f', '/tn', task_name, 
                      '/tr', f'"{python_exe}" "{script_path}"', 
                      '/sc', 'onlogon', '/rl', 'highest']
        subprocess.run(create_cmd, capture_output=True, creationflags=0x08000000)

        # Fix Battery Power settings via XML
        xml_path = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'task_config.xml')
        with open(xml_path, 'w') as f:
            subprocess.run(['schtasks', '/query', '/xml', '/tn', task_name], 
                           stdout=f, creationflags=0x08000000)
        
        with open(xml_path, 'r') as f:
            xml_data = f.read()
        
        xml_data = xml_data.replace('<StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>', '<StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>')
        xml_data = xml_data.replace('<DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>', '<DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>')
        
        with open(xml_path, 'w') as f:
            f.write(xml_data)
            
        subprocess.run(['schtasks', '/create', '/f', '/tn', task_name, '/xml', xml_path], 
                       creationflags=0x08000000)
        os.remove(xml_path)

def apply_registry():
    cmds = [
        ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Services\\W32Time\\TimeProviders\\NtpClient', '/v', 'SpecialPollInterval', '/t', 'REG_DWORD', '/d', '6', '/f'],
        ['reg', 'add', 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\TimeZoneInformation', '/v', 'RealTimeIsUniversal', '/t', 'REG_DWORD', '/d', '1', '/f']
    ]
    for cmd in cmds:
        subprocess.run(cmd, capture_output=True, creationflags=0x08000000)

def sync_time():
    subprocess.run(["w32tm", "/resync", "/force"], capture_output=True, creationflags=0x08000000)

if __name__ == "__main__":
    # 1. Check for Admin Rights
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 0)
        sys.exit()

    # 2. Single Instance Lock
    lock_file = os.path.join(os.environ.get('TEMP', 'C:\\Temp'), 'sync_service.lock')
    try:
        fp = open(lock_file, 'w')
        msvcrt.locking(fp.fileno(), msvcrt.LK_NBLCK, 1)
    except (IOError, OSError):
        sys.exit()

    # 3. Execution
    setup_task_scheduler()
    apply_registry()
    
    while True:
        sync_time()
        time.sleep(6)
