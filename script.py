from downloader import Downloader
from secrets import user, password


if __name__ == '__main__':

    listfile = "/tmp/url-list.txt"

    dlr = Downloader(user,
                     password,
                     listfile=listfile,
                     folder="/data/files/")

    dlr.download()
