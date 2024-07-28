import requests
import argparse
import zipfile
import os

# GLOBAL VARIABLES
programName = "proPkg"
programDesc = "a simple packagemanager"
reposLink = "https://led-reamer.github.io/libs/"
libsFile = "libs.txt"
libList = []

#ARGUMENTS
argParser = argparse.ArgumentParser(prog=programName, description=programDesc, epilog="")

#argParser.add_argument("mode", choices=["list", "find", "get"], type=str, help="list all packages, search for specific names, download a package")
argParser.add_argument("-l", "--list", action='store_true', required=False)
argParser.add_argument("-f", "--find", type=str, required=False)
argParser.add_argument("-g", "--get", type=str, required=False)
args = argParser.parse_args()


def getList():
    global libList
    libList = requests.get(reposLink + libsFile).text.splitlines()


getList()

if(args.list):
    for library in libList:
        print(library)
    exit()

if(args.find):
    if(args.find == None):
        print(libList)
        exit()

    for hit in libList:
        if(args.find in hit):
            print(hit)
    exit()

def download_and_extract(file):
    print("Downloading \"" + file + "\"")
    open(file, 'wb').write(requests.get(reposLink + file, allow_redirects=True).content)
    
    if(file.endswith(".zip")):
        print("Extracting \"" + file + "\"")
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(".")
        os.remove(file)
    exit()

if(args.get):
    if(not args.get in libList):
        num_hits = 0
        success = ""
        for hit in libList:
            if args.get in hit:
                num_hits += 1
                success = hit

        if(num_hits == 1):
            download_and_extract(success)
        
        print("Could not find \"" + args.get + "\"")
        for library in libList:
            print(library)
        exit()
    

#if no accepted mode was detected
argParser.print_help()
