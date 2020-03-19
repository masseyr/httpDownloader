from secrets import password, user
import time
import random
import requests
import sys
import os


__author__ = 'github.com/masseyr'
__all__ = "Downloader"


class Downloader:
    """
    Downloader class to retrieve file lists from HTTPS urls with user/passwd auth
    """
    def __init__(self,
                 username,
                 password,
                 urls=None,
                 folder=None,
                 listfile=None,
                 chunk_size=1024):
        """
        Downloader class instance
        :param username: HTTP(S) auth username
        :param password: HTTP(S) auth password
        :param urls: list of files as urls to retrieve
        :param folder: Folder to download the files to
        :param chunk_size: Chunk size (kb) for data stream
        """

        self.username = username
        self.password = password

        if listfile is not None:
            with open(listfile, 'r') as listfileptr:
                self.urls = [url.strip() for url in listfileptr.readlines()]
        elif urls is not None:
            if type(urls) not in (list, tuple):
                self.urls = list(urls)
            else:
                self.urls = urls

        self.stream = None

        if folder is None:
            self.folder = ""
        else:
            self.folder = folder

        self.chunk_size = chunk_size

        self.filenames = [self.folder + os.path.sep + os.path.basename(url) for url in self.urls]

    def get_stream(self,
                   url):
        """
        Method to open a connection to the file over http(s)
        :param url: URL to open
        :return: requests file stream
        """
        return requests.get(url,
                            auth=(self.username, self.password),
                            stream=True)

    def download(self,
                 random_requests=True,
                 verbose=True):
        """
        Method to download files by opening auth urls
        :param random_requests: If the requests should be pseudo-randomized
        :param verbose: if the downloaded file names should be displayed
        :return: None
        """

        for url_idx, url in enumerate(self.urls):

            if random_requests:
                time.sleep(random.random()*10.0)

            stream = self.get_stream(url)

            with open(self.filenames[url_idx], 'wb') as file_handl:
                for chunk in stream.iter_content(chunk_size=self.chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        file_handl.write(chunk)

            if verbose:
                sys.stdout.write('File written: {}'.format(self.filenames[url_idx]))
