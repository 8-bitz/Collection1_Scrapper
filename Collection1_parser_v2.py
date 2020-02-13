import os
import tarfile
import shutil
import time

results = []
ext_dir = "/Users/xxx/Desktop/Collection 1 parse test (v2)/ext"
root_dir = "/Volumes/xxx/xxx/Collection2-5"

searchTerms = ["test@hotmail.com","@gmail.com"]

def extract_archive(file_path, extraction_path):
    files = []
    tar = tarfile.open(file_path,"r:gz")
    tar.extractall(extraction_path)
    for dirName, subdirList, fileList in os.walk(extraction_path):
        pass
    for fname in fileList:
        files.append(dirName + "/" + fname)
    return files

def search_file(file_path):
    if ".txt" in file_path:
        filereader = open(file_path,"r",errors="ignore")
        while True:
            l = filereader.readline()
            if not l:
                break
            for item in searchTerms:
                if item in l:
                    print("[" + file_path + "]")
                    print("    " + l.replace("\n",""))
                    results.append((l.replace("\t","")).replace("\n","") + "   -->  " + file_path)
        filereader.close()
    else:
        print("Not a txt file:   " + file_path)
    return

def get_collection_files(root_dir):
    print(root_dir)
    files = []
    for r, d, f in os.walk(root_dir):
        for file in f:
            if '.tar.gz' in file:
                files.append(os.path.join(r, file))
    return files

coll1_files = get_collection_files(root_dir)
try:
    print("deleting existing extraction directory")
    shutil.rmtree(ext_dir)
except:
    print(ext_dir + " not found")
time.sleep(2)
try:
    print("creating new extraction directory")
    os.mkdir(ext_dir)
except:
    print(ext_dir + " already exists")
log = open("parser.log", "w")
log.close()
for coll1_file in coll1_files:
    log = open("parser.log", "a")
    print("processing:\t" + coll1_file)
    try:
        log.writelines("extracting " + coll1_file + "\n")
        log.flush()
        files = extract_archive(coll1_file, ext_dir)
    except:
        print("error extracting " + coll1_file)
        log.writelines("\tError extracting " + coll1_file + "\n")
        log.flush()
        files = []
    for f in files:
        log.writelines("\tSearching through " + f + "\n")
        log.flush()
        search_file(f)
    shutil.rmtree(ext_dir)
    time.sleep(2)
    os.mkdir(ext_dir)
    log.close()
print("******************************")
print("******************************")
for l in results:
    print(l)
final_output = open("final_results.txt","w")
print("WRITING TO FINAL_RESULTS.TXT")
for l in results:
    final_output.writelines(l + "\n")
    final_output.flush()
final_output.close()
