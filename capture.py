from PIL import ImageGrab, Image
import paramiko
import sys
import os


def main():
    if len(sys.argv) <= 1:
        image_folder = "images01"
    else:
        image_folder = sys.argv(1)

    if len(sys.argv) <= 2:
        scale_factor = 5
    else:
        scale_factor = sys.argv(2)

    i = 0
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('vac5', username='root', password='!bootstrap',
                   allow_agent=False, look_for_keys=False, timeout=5000)

    transport = paramiko.Transport(('vac5', 22))
    transport.connect(username='root', password='!bootstrap')

    sftp = paramiko.SFTPClient.from_transport(transport)

    os.system("mkdir im")
    local_path = 'im/%d.jpg'
    file_path = '/root/%s/%d.jpg'

    num_storage = 'store.txt'
    client.exec_command('mkdir -p /root/%s' % image_folder)
    while True:
        try:
            im = ImageGrab.grab()
            size = int(im.width/scale_factor), int(im.height/scale_factor)
            im.resize(size, Image.ANTIALIAS).save(local_path % i, 'JPEG')
            sftp.put(local_path % i, file_path % (image_folder, i))  # send via SSH to vac5
            with open(num_storage, 'w') as f:
                f.write(str(i))
                print(i)
            sftp.put(num_storage, '/root/%s/store.txt' % image_folder)
        except Exception as e:
            print(e)
            pass
        i += 1
    sftp.close()
    client.close()

if __name__ == '__main__':
    main()
