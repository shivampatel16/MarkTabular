import os
import glob
import tarfile
import subprocess

directory = "/home/shivam/Desktop/myExtracted Paper Folders/"
count = 0

# Removing folders containing no .tex files within them
for i in os.listdir(directory):
    filelist = glob.glob(directory + "/" + i + "/" + "/*.tex")
    if(len(filelist)) == 0:
        subprocess.call(['rm','-r', directory + "/" + i + "/"])
        count = count + 1   
    print("Count = ",count)      
print("Count = ", count)

directory = "/home/shivam/Desktop/myExtracted Paper Folders/"
total_removed = 0
run_count = 1

# Removing folders (having .tex files) containing no tables withing them
for i in os.listdir(directory):
    print(i)
    print("Run Count = ",run_count)
    run_count = run_count + 1
    
    filelist = glob.glob(directory + "/" + i + "/" + "/*.tex")
    
    for j in filelist:
        print(j)
        table_present_in_tex_check = 1
        begin_tabular_present = 1
        end_tabular_present = 1
        
        l = open(j,"r", encoding = "ISO-8859-1")
        myList = list(l)
        
        k = 0
        while k < len(myList):    
            myListk_after_removing_leading_spaces = myList[k].lstrip()
            
            if len(myListk_after_removing_leading_spaces) > 0:
                if myListk_after_removing_leading_spaces[0] != '%':
                    if "\\begin{tabular" in myList[k]:
                        begin_tabular_present = 0
            
            if len(myListk_after_removing_leading_spaces) > 0:
                if myListk_after_removing_leading_spaces[0] != '%':
                    if "\\end{tabular" in myList[k]:
                        end_tabular_present = 0
            k = k + 1
            
        table_present_in_tex_check = begin_tabular_present or end_tabular_present
            
    if table_present_in_tex_check == 1:
        subprocess.call(['rm','-r', directory + "/" + i + "/"])
        total_removed = total_removed + 1

print("Total Removed = ", total_removed)

directory = "/home/shivam/Desktop/myExtracted Paper Folders/"
total_removed = 0
run_count = 1

# Removing folders having: i) multiple .tex files with '\documentclass', and ii) no .tex files with '\documentclass'
for i in os.listdir(directory):
    print(i)
    print("Run Count = ",run_count)
    run_count = run_count + 1
    
    filelist = glob.glob(directory + "/" + i + "/" + "/*.tex")
    document_class_present_in_tex_check = 0
    
    for j in filelist:
        print(j)
        l = open(j,"r", encoding = "ISO-8859-1")
        z = l.read()
        
        if "\\documentclass" in z:
            document_class_present_in_tex_check = document_class_present_in_tex_check + 1
            
    print("Doc Classes = ", document_class_present_in_tex_check)
            
    if document_class_present_in_tex_check == 0 or document_class_present_in_tex_check > 1:
        subprocess.call(['rm','-r', directory + "/" + i + "/"])
        total_removed = total_removed + 1
        
print("Total Removed = ", total_removed)    