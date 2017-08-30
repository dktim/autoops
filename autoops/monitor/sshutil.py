import paramiko

def ssh_connection(ip,user):
    try:
        ssh=paramiko.SSHClient()
        pkey="/root/.ssh/id_rsa"
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        key=paramiko.RSAKey.from_private_key_file(pkey)                       
        ssh.connect(ip,22,user,pkey=key)
        return ssh
    except:
        return "connection fail"
