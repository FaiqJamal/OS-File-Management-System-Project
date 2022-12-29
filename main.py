# imports
import math
from structlinks.LinkedList import LinkedList
import pickle
import json

class memoryBlock():
    def __init__(self):
        self.id = None
        self.size = 10

    def setID(self, file):
        self.id = file

    def removeID(self):
        self.id = None


class File():
    def __init__(self, name, path, content):
        self.name = name
        self.path = path
        self.content = content

    def Read_from_file(self):
        print(self.content, '\n')

    def Read_from_file1(self, start, size):
        print(self.content[start:start+size], '\n')

    def Write_to_file(self, text):
        self.content += text

    def Write_to_file1(self, writeAt, text):
        self.content = self.content[0:writeAt-1] + \
            text + self.content[writeAt-1:]

    def Move_within_file(self, start, size, target):
        moveStr = self.content[start:start+size]
        newContent = ''
        if (start != 0):
            newContent = self.content[0:start-1]
        self.content = newContent+self.content[start+size:]
        self.Write_to_file1(target, moveStr)

    def truncate_file(self, size):
        self.content = self.content[0:size]


def Open(fileName):
    file = findFile(fileName, rootDirectory['root'])
    openMenu()
    while file is not None:
        mode = input("Enter your Option Here:")
        match mode:
            case "1":
                file.Read_from_file()
            case "3":
                text = input("Enter data to be Appended:")
                file.Write_to_file(text)
            case "2":
                start = input("Enter reading position:")
                size = input("Enter length of data to be read:")
                file.Read_from_file1(int(start), int(size))
            case "4":
                start = input("Enter writing Position:")
                text = input("Enter data to be Written:")
                file.Write_to_file1(int(start), text)
            case "5":
                start = input("Enter starting position of data to be moved:")
                size = input("Enter length of data to be moved:")
                target = input("Enter new position of data to be moved:")
                file.Move_within_file(int(start), int(size), int(target))
            case "6":
                size = input("Enter the size to be truncated:")
                file.truncate_file(size)
            case "7":
                file = close(fileName)
            case _:
                print("Invalid mode. Try again.\n")


def close(fileName):
    return None


def mkdir(newDirName):
    newDir = {newDirName: LinkedList()}
    currentDirectory[0].append(newDir)
    print(f'Directory -{newDirName}- added successfully.\n')


def chdir(path):
    global currentDirectory
    if path == '$':
        currentDirectory = (rootDirectory['root'], "")
    elif path == "..":
        path = currentDirectory[1]
        dirList = path.split('/')
        dirList.pop(-1)
        path = ''.join(map(str, dirList))
        currentDirectory = (findDir(dirList), path)
    else:
        path = currentDirectory[1]+path
        dirList = path.split('/')
        print(findDir(dirList))
        if findDir(dirList) is None:
            raise Exception("The system could not find the path specified.")
        else:
            currentDirectory = (findDir(dirList), path)


def findDir(dirList):
    dir = rootDirectory['root']
    for i in dirList:
        for object in dir:
            if isinstance(object, dict) and i in object:
                dir = object[i]
    return dir


def create(newFileName, content):
    newFile = File(newFileName, currentDirectory[1], content)
    currentDirectory[0].append(newFile)
    print(f'File {newFileName} added successfully.')
    putInMemory(newFile)


def putInMemory(file):
    noOfBlocks = math.ceil(len(file.content)/10)
    for i in range(noOfBlocks-1):
        block = next((x for x in Memory if x.id == None), None)
        if block is None:
            print("Memory of File Management Sytem is Full.\n")
            break
        else:
            block.setID(file)


def delete(fileName):
    try:
        targetFile = findFile(fileName, rootDirectory['root'])
        targetDir = findDir(targetFile.path.split('/'))
        ans = input(f"Are you sure you want to delete -{fileName}-?(y/n):")
        match ans:
            case 'y':
                targetDir.remove(targetFile)
                removeFromMemory(targetFile)
                print(
                    f"The file -{fileName}- has been Deleted Successfully.\n")
            case 'n':
                pass
            case _:
                print(
                    f"Invalid Option. The file -{fileName}- was not Deleted.\n")
    except:
        print(f"The File -{fileName}- does not exist.")


def removeFromMemory(file):
    block = "Not Null"
    block = next((x for x in Memory if x.id == file), None)
    while block is not None:
        block.removeID()
        block = next((x for x in Memory if x.id == file), None)


def findFile(filename, dir):

    for object in dir:
        if isinstance(object, dict):
            for i in object:
                tempDir = object[i]
            if (len(tempDir) == 0):
                pass
            else:
                if (findFile(filename, tempDir)) is None:
                    pass
                else:
                    return (findFile(filename, tempDir))
        elif isinstance(object, File) and object.name == filename:
            return object


def move(source, target):
    dir = rootDirectory['root']
    sourceFile = findFile(source, dir)
    sourceDir = findDir(sourceFile.path.split('/'))
    targetFile = findFile(target, dir)
    targetDir = findDir(targetFile.path.split('/'))
    targetDir.append(sourceFile)
    sourceDir.remove(sourceFile)





def showMap(dir, tab):
    for object in dir:
        if isinstance(object, dict):
            for i in object:
                dir = object[i]
            print(tab*'\t', ">", i)
            tab += 1
            showMap(dir, tab)
            tab -= 1
        elif isinstance(object, File):
            print(tab*'\t', '-', object.name)


def menu():
    print(2*'\t', 6*'-', "Main Menu", 6*'-')
    print(2*'\t', 'a.', 'Make Directory', '\n',
          2*'\t', 'b.', 'Change Current Directory', '\n',
          2*'\t', 'c.', 'Create new File', '\n',
          2*'\t', 'd.', 'Delete File', '\n',
          2*'\t', 'e.', 'Open File', '\n',
          2*'\t', 'f.', 'Show Memory Map', '\n',
          2*'\t', 'g.', 'Exit', 2*'\n',
          2*'\t', "* Type 'menu' to view menu again.", '\n')


def openMenu():
    print('\n', 2*'\t', 6*'-', "File Menu", 6*'-')
    print(2*'\t', '1.', 'Read File', '\n',
          2*'\t', '2.', 'Read File from specified Position', '\n',
          2*'\t', '3.', 'Append File', '\n',
          2*'\t', '4.', 'Write File from specified Position', '\n',
          2*'\t', '5.', 'Move content within File', '\n',
          2*'\t', '6.', 'Truncate', '\n',
          2*'\t', '7.', 'Exit', 2*'\n',
          2*'\t', "* Type 'menu' to view menu again.", '\n')


def chdirMenu():
    print("$  -> Return to root.\n.. -> Return to previous Directory.\n/DirectoryName1/... -> Go to specific Directory.\n")


Memory = [memoryBlock() for i in range(100)]  # total of 10kb
rootDirectory = {'root': LinkedList()}
currentDirectory = (rootDirectory['root'], "")


def create_dat_file():
    with open(b"memory.dat", "wb") as f:
        pickle.dump(rootDirectory, f)

def read_dat_file():
    with open("memory.dat", "rb") as f:
        fs = pickle.load(f)
        print(fs)
        #print(json.dumps(fs.Memory, indent=4, sort_keys=True, default=str))

# Just for Sampling, Delete before submitting
print("\nWelcome to File Management System by Faiq and Misbah.\n")
menu()
print("\nSelect any option to continue.")
# mkdir("Dir1")
# mkdir("Dir2")
# mkdir("Dir3")
# try:
#     chdir("Dir3")
# except:
#     print("The system could not find the path specified.\n")
# create("file1", "I like cats.")
# mkdir("Dir4")
# try:
#     chdir("..")
# except:
#     print("The system could not find the path specified.\n")
# create("file2", "This is Misbah and Faiq's File Management Sytem")
#
# # Menu Starts from here
# print("\nWelcome to File Management System by Faiq and Misbah.\n")

feature = None
while feature != "exit":
    feature = input(f"Faiq & Misbah:root{currentDirectory[1]}>")
    match feature:
        case "a":
            mkdir(input("Enter Name for new Directory:"))
        case "b":
            chdirMenu()
            path = input(f"Faiq & Misbah: root{currentDirectory[1]} > chdir >")
            try:
                chdir(path)
            except:
                print("The system could not find the path specified.\n")
        case "c":
            name = input("Enter Name for new File:")
            content = input(f"Enter content for {name} File:")
            create(name,content)
        case "d":
            delete(input("Enter name for file you want to Delete:"))
        case "e":
            Open(input("Enter name for file you want to Open:"))
            print('\n')
            menu()
        case "f":
            if (len(rootDirectory['root']) == 0):
                print(
                    "The File Management System is Empty. Add Directories and/or Files to view Memory Map.\n")
            else:
                print('\n', 6*'-', "Memory Map", 6*'-')
                showMap(rootDirectory['root'], 0)
                print('\n')
        case "g":
            feature = "exit"
        case "menu":
            menu()
        case _:
            print("Invalid Function. Try Again.\n")

create_dat_file()
print("\nFollowing is the output of memory.dat file. \nIt shows the complete hiarchial structure of objects in our system")
read_dat_file()
