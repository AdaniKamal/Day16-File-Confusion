#The OS library provides different functionality that interfaces with an operating system. Examples include viewing file permissions,
#interacting with processes & various other operating system functions.
from os import path, chdir, listdir, getcwd, system
from zipfile import ZipFile
import sys

workingPath = getcwd()
#set our current working directory
#this is one of the functions that we imported from the os library

#Check if Exiftool is installed and install it if not.
exif_installed = system("exiftool >>/dev/null")
if exif_installed != 0:
    install = input("You don't have exiftool installed, would you like to install it? (Y/n): ")
    if install.lower() == "n":
        print("Program can't work without exiftool installed. Exiting...")
        sys.exit()
    
    system("sudo apt-get install exiftool -y")
    exif_installed = system("exiftool >>/dev/null")
    if exif_installed != 0:
        print("Fatal Error -- Couldn't install Exiftool. Check your repositories. Exiting...")
        sys.exit()
    print("\n\n\n\n\nProgram Starting Now:\n\n")

#have a look at the system arguments to see where our zipfile can be found
#~~if statement~~ we’re checking to see if there are less than two arguments
#(i.e. the user hasn’t supplied a zipfile to read & has called the program with no arguments).
#If no file has been specified then the program will print a help message then exit
#~~elif statement~~ - checking to see if the filename exists, and also that it’s a zipfile.
#If it isn’t the program gives an error message and exits.
    
if len(sys.argv) < 2:
    print("Wrong arguments\nSyntax: python3 extract.py [filename] OPTIONAL -C")
    sys.exit()
elif path.exists(sys.argv[1])!=True or sys.argv[1][-4:] != ".zip":
    print ("Invalid Filename!")
    sys.exit()

#Open file and extract the files into a subdirectory
#This opens up the specified zipfile in a readable format (r),then creates the subdirectory [extracted_zips] & extracts all of the zipfiles contained in the downloaded zipfile into it.
with ZipFile(workingPath+"/"+sys.argv[1], 'r') as zipfile:
    zipfile.extractall(workingPath+"/extracted_zips")

#This is going through all of the files in our extracted_zips subdirectory (using another of the os library imports to get a listing for the file in conjunction with a for loop)
#then opening each in turn and extracting the contents into a new [extracted_files] subdirectory.
for zfile in listdir(workingPath + "/extracted_zips"):
    with ZipFile(workingPath+"/extracted_zips/"+zfile) as zipfile:
            zipfile.extractall(workingPath+"/extracted_files")

#First answer:
#copied every file into a single subdirectory. Following code is to print out the answer
print("The number of files is: ",len(listdir(workingPath+"/extracted_files")))

#For Second:
#Handle Wait Times, loading message. Waiting for exiftool.
print("Working...", end="\r")

#get the exifdata for each of the files
#store this as text in a .txt file
#easily extract the data line by line later.
directory = "extracted_files"
for i in listdir(directory):
    system(f"exiftool {directory}/{i} >> exiftool.txt")

#open the exiftool.txt file and parse the data into an array called metadata
with open("exiftool.txt") as etresults:
    metadata = etresults.readlines()
system("rm exiftool.txt")

#This section first initialises our number of files that match the criteria as being zero.
#It then loops through every line in the metadata array (i.e. every line in the exifdata for every file we extracted).
#If it finds a line containing both “Version” and “1.1” it adds one to the counter
#Outside the loop we then print the value of the counter
counter = 0
for line in metadata:
    if "Version" in line and "1.1" in line:
        counter += 1
        
#Second answer:
print("The number of files containing Version: 1.1 is: ",counter)

#looking for “password” (as in a questions)
chdir("extracted_files")
for filename in listdir():
    try:
        with open(filename, "r") as f:
            data = f.read()
            if "password" in data:
                print("Filename is: ", filename)
    except:
        continue

#cleanup
if "-C" in sys.argv:
    chdir(workingPath)
    system("rm -rf extracted_files extracted_zips")
