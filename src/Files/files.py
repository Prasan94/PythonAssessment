"""
"""
import shutil
import pathlib
import os
import csv
import multiprocessing
import threading
from src.Files.abstract.files import Files as absFiles
from src.RemoteServer.connection import FtpConnection
from src.DB.db import MongoDB
from src.utils.helper import get_cpu_count

class Files(absFiles):
    """
    """
    def __init__(self, remotePath, localPath, downloadQueue):
        self.remotePath = remotePath
        self.localPath = localPath
        self.downloadQueue = downloadQueue
        self.serverConnection = FtpConnection()
        self.dbConnection = MongoDB()

    @property
    def localPath(self):
        """
        """
        return self._localPath

    @localPath.setter
    def localPath(self, path):
        """
        """
        if not os.path.exists(path):
            raise Exception("Error occurred: local path %s does not exist"%path)
        self._localPath = path

    def download(self, fileName, ):
        """
        """
        try:
            print "downloading file", fileName #Replace with actul function
            shutil.copy(self.remotePath, self.localPath)
            #time.sleep(1)
            self.downloadQueue.put(fileName)
        except Exception as err:
            raise Exception("Error while downloading the file %s\n%s"%(fileName, err))

    @staticmethod
    def validate(fileName):
        """
        """
        if fileName.find(".csv") > -1:
            return True

    def start_download_processes(self):
        """
        """
        noOfProcessesToBeSpawned = get_cpu_count() - 3
        with self.serverConnection.connect() as conn:
            dirObj = pathlib.Path(self.remotePath).iterdir()
            while True:
                try:
                    pList = []
                    for _ in range(noOfProcessesToBeSpawned):
                        fileName = next(dirObj)
                        if Files.validate(fileName):
                            p = multiprocessing.Process(target=self.download, args=(fileName,))
                            pList.append(p)
                    for p in pList:
                        p.start()
                    for p in pList:
                        p.join()
                except StopIteration:
                    for p in pList:
                        p.start()
                    for p in pList:
                        p.join()
                    print "All download Completed"
                    self.downloadQueue.put("completed")
                    break
                except Exception as err:
                    print "Error while preparing for the download",err
                    self.downloadQueue.put("error")
                    break

    def parse_csv(self, fileName):
        """
        """
        header = True
        try:
            with open(fileName) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                while True
                    if header:
                        keys = next(reader).split(",")
                    else:
                        yield dict(zip(keys, next(reader).split(",")))
        except StopIteration:
            pass
        except Exception as err:
            print "Error while parsing the file %s\n%s"%(fileName, err)

    def insert_files(self, fileName):
        """
        """
        try:
            documentObj = self.parse_csv(fileName)
            while True:
                document = next(documentObj)
                query = "" #prepare query
                print document
        except StopIteration:
            print "%s inserted into DB"%fileName
        except Exception as err:
            print "Error while inserting file %s into DB"%err
        finally:
            Files.delete(fileName)
        

    @staticmethod
    def delete(fileName):
        """
        """
        try:
            os.remove(fileName)
        except Exception as err:
            print "Error while deleting the file %s\n%s"%(fileName, err)

    def start_insert_processes(self):
        """
        """
        noOfThreadsToBeSpawned = 2
        breakMainLoop = False
        while True:
            tList = []
            for _ in range(noOfThreadsToBeSpawned):
                fileName = self.downloadQueue.get()
                if not (fileName == "completed" or fileName == "error"):
                    t = threading.Thread(target=self.insert_files, args=(fileName,))
                    tList.append(t)
                else:
                    print "all files recieved"
                    for t in tList:
                        t.start()
                    for t in tList:
                        t.join()
                    breakMainLoop = True
                    break
            if breakMainLoop:
                break
            for t in tList:
                t.start()
            for t in tList:
                t.join()

   


                




    
