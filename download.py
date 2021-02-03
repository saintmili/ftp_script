from ftplib import FTP
from config import host, username, password, download_from_dir, download_to_dir



def download(host, username, password, download_from_dir, download_to_dir):
    session = FTP(host)
    if session.login(user=username, passwd=password):
        print(f'{username} logged in successfully.')
        session.cwd(download_from_dir)
        files = []
        session.retrlines('LIST', lambda x: files.append(x.split()))
        for info in files:
            ls_type, name = info[0], info[-1]
            if ls_type.startswith('d'):
                print(f'{name} is a directory!')
            else:
                f = open(f'{download_to_dir}/{name}', 'ab')
                f.close()
                f = open(f'{download_to_dir}/{name}', 'wb')
                session.retrbinary("RETR " + name, f.write)
                print('hi')
                f.close()
        session.quit()
        print(f'{username} logged out successfully.')
    else:
        print('Username or password incorrect!')


download(host, username, password, download_from_dir, download_to_dir)