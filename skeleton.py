import multiprocessing
import threading
import time
import os

def dummy_directory():
    files = ["f1.csv", "f2.csv", "f3.csv", "f4.csv", "f5.csv", "f6.csv", "f7.csv", "f8.csv","f9.csv", "f10.csv"]
    for f in files:
        yield f
        
def get_cpu_count():
    return multiprocessing.cpu_count()
    
class RemoteServer(object):
    def __init__(self, q):
        self.parallelProcessLimit = get_cpu_count() - 3
        self.q = q
        
    @staticmethod
    def filterFile(fileName):
        return True if fileName.find(".csv") > -1 else False  #Replace with actual condition
        
    def start_download_processes(self):
        dirObj = dummy_directory()  #Replace with the actual modules to fetch from remote server
        while True:
            try:
                pList = []
                for _ in range(self.parallelProcessLimit):
                    fileName = next(dirObj)
                    if RemoteServer.filterFile(fileName):
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
                self.q.put("completed")
                break
            except Exception as err:
                print "Error while preparing for download",err
                self.q.put("error")
                break
        
    def download(self, fileName):
        try:
            print "downloading file", fileName #Replace with actul function
            time.sleep(1)
            self.q.put(fileName)
        except Exception as err:
            print "Error while downloading the file",fileName
            
class Db(object):
    def __init__(self, q):
        self.q = q
        self.parallelProcessLimit = 3  #Can be decided based on the perfomance test
        
    def start_insert_processes(self):
        breakMainLoop = False
        while True:
            tList = []
            for _ in range(self.parallelProcessLimit):
                fileName = self.q.get()
                if not (fileName == "completed" or fileName == "error"):
                    t = threading.Thread(target=self.insert, args=(fileName,))
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
    
    def insert(self, fileName):
        try:
            print "parsing and insering", fileName  #Replace with the actual parsinf and inserting functionality
            time.sleep(1)
        except Exception as err:
            print "Failed to insert file", fileName
            
if __name__ == "__main__":
    t1 = time.time()
    
    q = multiprocessing.Queue()
    rsObj = RemoteServer(q)
    dbObj = Db(q)
    
    remoteServerProcess = multiprocessing.Process(target=rsObj.start_download_processes)
    dbProcess = multiprocessing.Process(target=dbObj.start_insert_processes)
    
    remoteServerProcess.start()
    dbProcess.start()
    
    remoteServerProcess.join()
    dbProcess.join()
    
    print "Script finished in",time.time()-t1 
        
                    
                
            
            
    
                    
            
            
        
