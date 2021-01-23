from ftplib import FTP
from os import listdir
from os.path import isfile, join
from data import host, username, password, upload_from_dir, upload_to_dir



"""returns a list of files from given directory"""
def list_dir_files(path):
    try:
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files
    except FileNotFoundError:
        return("given directory doesn't exist!")



"""Upload from given upload_from_dir to upload_to_dir"""
def upload(host, username, password, upload_to_dir, upload_from_dir):
    session = FTP(host)
    if session.login(user=username, passwd=password):
        print(f'{username} successfully loged in.')
        files = list_dir_files(upload_from_dir)
        if type(files)==list:
            print(f'{len(files)} files detected.')
            session.cwd(upload_to_dir)
            i = 1
            succeed_uploads = 0
            for file in files:
                f = open(f'{upload_from_dir}/{file}', 'rb')
                print(f'uploading {file}.({i}/{len(files)})')
                if session.storbinary("STOR " + file, f):
                    print(f'{file} uploaded succesfully.')
                    succeed_uploads += 1
                else:
                    print('something happened and {file} didnt upload!')
                i += 1
                f.close()
            print(f'{succeed_uploads}/{len(files)} files uploaded successfully.')
        else:
            print(files)
        session.quit()
        print(f'{username} logged out.')
    else:
        print('ur username or password is wrong!')



        

upload(host,username,password,upload_to_dir,upload_from_dir)