# python-paramiko
python paramiko


## example
````
#! python
from paramiko import SSHClient, AutoAddPolicy
from time import sleep


with SSHClient() as client:
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(
        hostname='172.16.1.5',
        username='user1',
        password='pass1234',
        look_for_keys=False
    )
    session = client.invoke_shell()
    session.send('ls -la' + '\n')
    sleep(1)
    output = session.recv(65535).decode('utf-8')
    print(output.strip())
````        
