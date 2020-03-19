from downloader import Downloader
from secrets import user, password


if __name__ == '__main__':

    listfile = "/tmp/url-list.txt"
    folder = "/data/files/"

    dlr = Downloader(user,
                     password,
                     listfile=listfile,
                     folder=folder)

    dlr.download()
