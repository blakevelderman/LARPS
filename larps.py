import paramiko
import random

def send_to_vault(hostname, password):
    key = paramiko.RSAKey.from_private_key_file("vault-key.pem")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="vault.ncsa.tech",
                        username='ubuntu',
                        pkey=key)
    cmd = "vault kv put Systems-Team/" + hostname + "-root password=" + password
    stdin, stdout, stderr = ssh_client.exec_command(cmd)

def set_root_pass(hostname, password):
    passphrase = ''
    key = paramiko.RSAKey.from_private_key_file(".ssh/id_rsa", password=passphrase)
    hostname = hostname + '.ncsa.tech'
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,
                        username='LARPS',
                        pkey=key)
    cmd = "sudo usermod -p $(openssl passwd -1 " + password + ") root"
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    out=stderr.read().decode()
    print(out)


f = open('servers.txt', 'r')
f = f.read()
f = f.split('\n')
for server in f:
    if len(server) < 2:
        continue
    x = 0 
    password = ""
    while x < 16:
        type = random.randint(1,3)
        x = x + 1
        if type == 1:
            let = random.randint(65,90)
            let = chr(let)
            password = password + let
        elif type == 2:
            let = random.randint(97,122)
            let = chr(let)
            password = password + let
        elif type == 3:
            let = random.randint(0,9)
            password = password + str(let)

    print(server)
    print(password)

    send_to_vault(server, password)
    set_root_pass(server, password)
