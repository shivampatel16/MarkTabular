import os
import glob
import tarfile
import subprocess

os.chdir("/home/shivam/Desktop/cs_papers_final/")
directory = "/home/shivam/Desktop/cs_papers_final/"
subprocess.call(['mkdir', '/home/shivam/Desktop/myExtracted Paper Folders/'])

count = 1

# Extracting compressed folders for all research articles
for src_name in glob.glob(directory+'*.gz'):
    count = count + 1
    print(src_name)
    a = src_name.rsplit('/',1)[1]
    print(a)
    
    subprocess.call(['mkdir', '/home/shivam/Desktop/myExtracted Paper Folders/' + a[:-3]])
    print("tar -xf " + a + " -C /home/shivam/Desktop/myExtracted Paper Folders/" + a[:-3])
    w = subprocess.call(['tar', '-xf', a, '-C', '/home/shivam/Desktop/myExtracted Paper Folders/' + a[:-3]])
    print(w)
    
    subprocess.call(['rm','-r', src_name])     