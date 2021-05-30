import os
import glob
import subprocess
import re
import string
from statistics import mode

directory = "/home/shivam/Desktop/myExtracted Paper Folders/"
subprocess.call(['mkdir', '/home/shivam/Desktop/myCompleted Paper Folders/'])

def most_frequent(List): 
    dict = {} 
    count, itm = 0, '' 
    for item in reversed(List): 
        dict[item] = dict.get(item, 0) + 1
        if dict[item] > count : 
            count, itm = dict[item], item    
        if dict[item] ==count : 
            count, itm = dict[item], max(item,itm)
    return(itm) 

run_count = 1

# Benckmarking cleaned dataset: Adding specific tokens at the start and end of each table in .tex files
# Token before table : #THIS#IS#START#OF#TABLE#
# Token after table  : #THIS#IS#END#OF#TABLE#
for i in os.listdir(directory):
    print("Run Count = ", run_count)
    run_count = run_count + 1
    print(i)
    
    filelist = glob.glob(directory + i + "/" + "*.tex")
    
    for j in filelist:
        print(j)
        l = open(j,"r", encoding = "ISO-8859-1")
        z1 = l.read()
        l.close()
        l = open(j,"r", encoding = "ISO-8859-1")
        myList = list(l)

        # Removing all commented lines in .tex files
        k = 0
        while k < len(myList):
            myListk_after_removing_leading_spaces = myList[k].lstrip()
            if len(myListk_after_removing_leading_spaces) > 0:
                if myListk_after_removing_leading_spaces[0] == '%':
                    del myList[k]
                    k = k - 1
            k = k + 1

        k = 0
        while k < len(myList):   
            print("\n 1 myList[k] = ", myList[k], "\n")
            if(k < len(myList)): 
                include_graphics_flag = 0
                k_check = k
            
                if "\\begin{table" in myList[k_check] or "\\begin{SCtable" in myList[k_check] or "\\begin{sidewaystable" in myList[k_check]:
                    print("\n 2 myList[k_check] = ", myList[k_check], "\n")
                    if(k_check < len(myList)): 
                        while( ("\\end{" not in myList[k_check] or "table" not in myList[k_check]) ):
                            print("\n 3 myList[k_check] = ", myList[k_check], "\n")
                            k_check = k_check + 1
                            if(k_check < len(myList)): 
                                if("\\begin{tabular" in myList[k_check]):
                                    if(k_check < len(myList)):
                                        while("\\end{tabular" not in myList[k_check]):
                                            print("\n 4 myList[k_check] = ", myList[k_check], "\n")
                                            if k_check < len(myList):
                                                if("\\includegraphics" in myList[k_check]):
                                                    include_graphics_flag = 1
                                            k_check = k_check + 1
                                            if k_check >= len(myList):
                                                break
                            if k_check >= len(myList):
                                break
    
                if(include_graphics_flag == 0):                
                    column_count = []
                    
                    k_check = k
                    if "\\begin{table" in myList[k_check] or "\\begin{SCtable" in myList[k_check] or "\\begin{sidewaystable" in myList[k_check]:
                        if(k_check < len(myList)): 
                            while( ("\\end{" not in myList[k_check] or "table" not in myList[k_check]) ):
                                k_check = k_check + 1
                                if(k_check < len(myList)): 
                                    if("\\begin{tabular" in myList[k_check]):
                                        if(k_check < len(myList)):
                                            while("\\end{tabular" not in myList[k_check]):
                                                if k_check < len(myList):
                                                    s = myList[k_check]
                                                    my_z_to_find_no_of_columns = re.findall(r"[^\\]&", s, re.S)
                                                    column_count.append(len(my_z_to_find_no_of_columns) + 1)
                                                k_check = k_check + 1
                                                if k_check >= len(myList):
                                                    break
                                                    
                                if k_check >= len(myList):
                                    break
                   
                    column_count = list(filter(lambda a : a != 1, column_count))
                    
                    if len(column_count) > 0:
                        columns = most_frequent(column_count)
                    else:
                        columns = 0
                    
                    if "\\begin{table" in myList[k] or "\\begin{SCtable" in myList[k] or "\\sidewaystable" in myList[k]:
                        if(k < len(myList)): 
                            while( ("\\end{" not in myList[k] or "table" not in myList[k])):
                                if(k < len(myList)): 
                                    if("\\begin{tabular" in myList[k]):
                                        table_start_insert = "\\\\ \\multicolumn{" + str(columns) + "}{c}{\\#THIS\\#IS\\#START\\#OF\\#TABLE\\#}\\\\"
                                        myList.insert(k + 1 , table_start_insert)
                                        if(k < len(myList)):
                                            while("\\end{tabular" not in myList[k]):
                                                k = k + 1
                                                if k >= len(myList):
                                                    break
                                            table_end_insert = "\\\\ \\multicolumn{" + str(columns) + "}{c}{\\#THIS\\#IS\\#END\\#OF\\#TABLE\\#}\\\\"
                                            myList.insert(k,table_end_insert)
                                            k = k + 1                                 
            k = k + 1
        
        if "\\documentclass" in z1:
            edited_tex_file_name = directory + i + "/" + i + ".tex"
            print(edited_tex_file_name)
            with open(edited_tex_file_name,"w") as file:
                for line in myList:
                    file.write(line)
            
        else: 
            open(j, 'w').close()
            with open(j,"w") as file:
                for line in myList:
                    file.write(line)
        l.close()
            
    os.chdir("/home/shivam/Desktop/myExtracted Paper Folders/" + i + "/")
    
    # Converting .tex to .pdf
    subprocess.call(['pdflatex', i + ".tex"])
    source_folder = directory + str(i)
    destination_folder = "/home/shivam/Desktop/myCompleted Paper Folders/"
    subprocess.call(['mv', source_folder, destination_folder])


# Moving correctly generated PDFs to myGenerated PDFs
directory = "/home/shivam/Desktop/myCompleted Paper Folders/"
count = 1
total_pdfs_generated = 0
subprocess.call(['mkdir', '/home/shivam/Desktop/myGenerated PDFs/'])

for i in os.listdir(directory):
    print("Run Count = ",count)
    count = count + 1
    print(i)
    
    pdf_path = directory + i + "/" + i + ".pdf"
    print(os.path.exists(pdf_path))
    
    if (os.path.exists(pdf_path)):
        total_pdfs_generated = total_pdfs_generated + 1    
        source_folder = directory + i + "/" + i + ".pdf"
        destination_folder = "/home/shivam/Desktop/myGenerated PDFs/"
        subprocess.call(['cp', source_folder, destination_folder])
                            
print("Total PDFs generated = ", total_pdfs_generated)