import argparse
import multiprocessing
import time
from src.Files.files import Files

if __name__ == "__main__":
    t1 = time.time()

    parser = argparse.ArgumentParser()

    parser.add_argument("--remote_path", dest="remotePath", help="remote server path")
    parser.add_argument("--local_path", dest="localPath", help="local server path to save downloaded files")

    args = parser.parse_args()
    
    queue = multiprocessing.Queue()
   
    filesObj = Files(args.remotePath, args.localPath, queue)
    downloadProcess = multiprocessing.Process(target=filesObj.start_download_processes)
    insertProcess = multiprocessing.Process(target=filesObj.start_insert_processes)

    downloadProcess.start()
    insertProcess.start()

    downloadProcess.join()
    insertProcess.join()

    print "script finished in",time.time() - t1


    
