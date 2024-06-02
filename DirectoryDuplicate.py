import os
import hashlib
import time
from sys import argv, exit

def DeleteFiles(duplicates):
    results = list(filter(lambda x: len(x) > 1, duplicates.values()))

    if len(results) > 0:
        for result in results:
            for i, subresult in enumerate(result):
                if i >= 1:  
                    os.remove(subresult)
    else:
        print("No duplicate files found")

def hashfile(path, blocksize=1024):
    hasher = hashlib.md5()
    with open(path, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()

def findDup(path):
    if not os.path.isabs(path):
        path = os.path.abspath(path)

    if not os.path.isdir(path):
        print("Invalid Path")
        return {}

    dups = {}
    for dirName, subDirs, fileList in os.walk(path):
        print("current folder is: " + dirName)
        for filename in fileList:
            filePath = os.path.join(dirName, filename)
            file_hash = hashfile(filePath)
            if file_hash in dups:
                dups[file_hash].append(filePath)
            else:
                dups[file_hash] = [filePath]

    return dups

def printResults(duplicates):
    results = list(filter(lambda x: len(x) > 1, duplicates.values()))

    if len(results) > 0:
        print("Duplicates found: ")
        print("The following files are duplicate")
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
    else:
        print("No duplicate files found")

def main():
    print("----Directory Duplication----")
    print("Application name: " + argv[0])

    if len(argv) != 2:
        print("Error: Invalid number of arguments")
        exit()
    
    if argv[1] == "-h" or argv[1] == "-H":
        print("This Script is used to traverse a specific directory and delete duplicate files")
        exit()

    if argv[1] == "-u" or argv[1] == "-U":
        print("Usage: ApplicationName AbsolutePath_of_Directory")
        exit()

    try:
        startTime = time.time()
        duplicates = findDup(argv[1])
        printResults(duplicates)
        DeleteFiles(duplicates)
        endTime = time.time()
        print("Took %s seconds to evaluate." % (endTime - startTime))
    
    except ValueError:
        print("Error: Invalid datatype of input")
    
    except Exception as E:
        print("Error: Invalid input", E)

if __name__ == "__main__":
    main()
