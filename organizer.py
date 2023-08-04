import os,sys,requests,xml.etree.ElementTree as ET, shutil, hashlib, pathlib
from zipfile import ZipFile; from colorama import Fore

print('Make sure the games that you want to scan are not in file archives as the tool can not verify content inside them.\n\n')

debug = 0

def debugmode(input):
    if debug == 1:
        f = open('log.txt','a')
        f.write(input)
        return(print(input))

def download(url: str, fileName: str):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    length = response.headers.get('content-length')
    block_size = 1000000  # default value
    if length:
        length = int(length)
        block_size = max(4096, length // 20)
    filesize = length*10**-6
    filesize = round(filesize, 2)
    print(Fore.BLUE+f"{fileName}"+Fore.RESET+' size: '+Fore.CYAN+f"{filesize} MB"+Fore.RESET)
    with open(fileName, 'wb') as f:
        size = 0
        for buffer in response.iter_content(block_size):
            if not buffer:
                break
            f.write(buffer)
            size += len(buffer)
            if length:
                percent = int((size / length) * 100)
                print(Fore.RESET+"Downloading "+Fore.BLUE+f"{fileName}"+': '+Fore.CYAN+f"{percent}%", end='\r')
    print(Fore.GREEN+"\nDone Downloading: "+Fore.CYAN+f"{fileName}"+Fore.RESET+'\n')

def unzip(file, dir='/'):
    with ZipFile(file, 'r') as f:
        f.extractall(dir)

def romcheck(filedir,exportdir):
    if os.path.isdir(exportdir) == False:
        os.mkdir(exportdir)
        debugmode(Fore.RED+exportdir+'\n'+Fore.RESET)
    for filename in os.listdir(filedir):
        f = os.path.join(filedir, filename)
    # checking if it is a file
        if os.path.isfile(f):
            debugmode(Fore.RED+f+'\n'+Fore.RESET)
            romMD5 = hashlib.md5(open(f,'rb').read()).hexdigest()
            debugmode(Fore.RED+romMD5+'\n'+Fore.RESET)
            for filename in os.listdir('Dat-Files'):
                d = os.path.join('Dat-Files', filename)
                if os.path.isfile(d):
                    debugmode(Fore.RED+d+'\n'+Fore.RESET)
                    tree = ET.parse(d)
                    root = tree.getroot()
                    system = root[0][2].text
                    for rom in root.iter('rom'):
                        if rom.get('md5') == romMD5:
                            name = str(f)
                            name = name.replace(filedir,'')
                            name = name.replace('/','')
                            file = name
                            suffix = pathlib.Path(f).suffix
                            name = name.replace(suffix,'')
                            if os.path.isfile(exportdir+'/'+system+'/'+file) == True:
                                os.remove(exportdir+'/'+system+'/'+file)
                            print('Verified '+name+' is an official '+system+' rom\nNow Moving\n')
                            if os.path.isdir(exportdir+'/'+system) == False:
                                os.mkdir(exportdir+'/'+system)
                            shutil.move(f,exportdir+'/'+system)


if os.path.isdir('Dat-Files') == False:
    os.mkdir('Dat-Files')


#* Rom validity checker function
nointrourl = 'https://github.com/hugo19941994/auto-datfile-generator/releases/latest/download/no-intro.zip'

download(nointrourl,'Dat-Files/no-intro.zip')

unzip('Dat-Files/no-intro.zip','Dat-Files/')

if os.path.isfile('Dat-Files/no-intro.zip') == True:
    os.remove('Dat-Files/no-intro.zip')


#romcheck('roms','Games')

romdir = input('Please specify the directory that contains your ROMS *They can not be in file archives*\nPath = ')
output = input('Please specify the path that you want your ROMS to be organized into.\nPath = ')

if os.path.isdir(romdir) == True and os.path.isdir(output) == True:
    romcheck(romdir,output)
if os.path.isdir(romdir) == False or os.path.isdir(output) == False:
    print('Please Specify a Valid directory')













