#!python
import paramiko

def fetch_logs_via_ssh(hostname, port, username, password):
    # 1. สร้าง SSH Client
    ssh = paramiko.SSHClient()
    
    # 2. ตั้งค่าให้ยอมรับ Host Key แบบอัตโนมัติ (ป้องกัน Error กรณีเชื่อมต่อครั้งแรก)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Connecting to {hostname}...")
        ssh.connect(hostname, port=port, username=username, password=password)
        print("Connected successfully!\n")

        # 3. คำสั่งที่ต้องการรัน (ใส่ -S เพื่อรอรับ password จาก stdin)
        command = "sudo -S tail -n 10 /var/log/kern.log /var/log/auth.log"
        
        # 4. รันคำสั่ง
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # 5. ส่งรหัสผ่านเข้าไปให้ sudo และสั่งทำงาน (flush)
        stdin.write(password + '\n')
        stdin.flush()

        # 6. อ่านผลลัพธ์ที่ได้
        result = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if result:
            print("=== RESULTS ===")
            print(result)
            
        # หมายเหตุ: sudo จะพ่นข้อความเตือนให้ใส่รหัสผ่านออกมาทาง stderr เสมอ
        # ถ้ามี error อื่นๆ ก็จะออกมาตรงนี้ด้วย
        if error:
            print("=== MESSAGES / ERRORS ===")
            print(error)

    except paramiko.AuthenticationException:
        print("Authentication failed: รหัสผ่านหรือ Username ไม่ถูกต้อง")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        # 7. ปิดการเชื่อมต่อเสมอ
        ssh.close()

# กำหนดข้อมูลเครื่องเซิร์ฟเวอร์ของคุณตรงนี้
HOST = "172.31.70.228"
PORT = 22
USER = "wachira"
PASS = "xxxx"

# เรียกใช้งานฟังก์ชัน
fetch_logs_via_ssh(HOST, PORT, USER, PASS)
