from ftplib import FTP
from config import host, username, password, download_from_dir, download_to_dir
from tqdm import tqdm


def open_or_create_file(path, name):
    try:
        file = open(f'{path}/{name}', 'wb')
        return file
    except EOFError:
        file = open(f'{path}/{name}', 'ab')
        file.close()
        file = open(f'{path}/{name}', 'wb')
        return file




def download(host, username, password, download_from_dir, download_to_dir):
    session = FTP(host)
    if session.login(user=username, passwd=password):
        print(f'{username} logged in successfully.')
        session.cwd(download_from_dir)
        files = []
        session.retrlines('LIST', lambda x: files.append(x.split()))
        i = 1
        succeed_downloads = 0
        session.sendcmd('TYPE I') 
        for info in files:
            ls_type, name = info[0], info[-1]
            if ls_type.startswith('d'):
                if name == '.' or name == '..':
                    pass
                else:
                    print(f'{name} is a directory!')
            elif ls_type.startswith('l'):
                pass
            else:
                print(f'Downloading {name} ...')
                filesize = session.size(session.pwd() + name)
                f = open_or_create_file(download_to_dir, name)
                with tqdm(unit='blocks', unit_scale=True, leave=False, miniters=1, desc=f'Downloading {name}({i}/{len(files)}).....', total=filesize) as pb:
                    def callback_(data):
                        l = len(data)
                        pb.update(l)
                        f.write(data)
                    if session.retrbinary("RETR " + name, callback_):
                        print(f'{name} downloaded successfully.')
                        succeed_downloads += 1
                    i += 1
                f.close()
        session.quit()
        print(f'{username} logged out successfully.')
    else:
        print('Username or password incorrect!')


download(host, username, password, download_from_dir, download_to_dir)