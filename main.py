import requests
from bs4 import BeautifulSoup
from time import sleep
from os import makedirs, walk
from re import sub
from tqdm import tqdm
from sys import argv
from base64 import urlsafe_b64decode, urlsafe_b64encode
import sys


class voduGeter:
    def __init__(self, url_):
        self.url = url_
        self.mediaName = ""
        self.file_path = ""
        self.block_size = 16384
        self.fileBuffer = bytearray()

    def checkUrl(self):
        site = r"https://movie.vodu.me/index.php?do=view&type=post&id="
        if site in self.url:
            req = requests.get(url=self.url)
            if not req.ok:
                return print(self.url, 'Not Ok')
            self.soup = BeautifulSoup(req.content, 'html.parser')
            return self.checkType()
        else:
            return print("Enter Vodu Series Or Movie Url Only.\n")

    def checkType(self):
        self.series = self.soup.find("div", {"class": "col-md-12 customtabs"})

        if self.series:
            self.completeMes = "Series Episodes Downloading Complete."
            return self.getSeries()
        else:
            self.completeMes = "Moive Downloading Complete."
            return self.getMovie()

    def checkFile(self, filename, search_path):
        for root, dir, files in walk(search_path):
            if filename in files:
                return True
        return False

    def createFolder(self):
        makedirs(self.mediaName, exist_ok=True)
        self.createInfoFile()

    def getSeries(self):
        trs = self.series.find_all("a", {"class": "btn btn-success play"})
        epNamesTrs = self.series.find_all(
            "div", {"class": "col-md-7 col-xs-12 col-sm-8"})
        for index, ep in enumerate(epNamesTrs):
            print(f"{index+1} - {ep.getText()}")

        seriesName = self.soup.find(
            "div", {"class": "col-lg-5"}).find("h1").getText()

        seriesName = sub(r'[^a-zA-Z0-9]', ' ', seriesName)
        seriesName = seriesName.split(" ")
        while True:
            if bool(seriesName[-1]):
                break
            else:
                seriesName.pop()
        self.mediaName = " ".join(seriesName)
        epCount = len(epNamesTrs)
        self.file_path = self.mediaName + "/"

        while True:
            try:
                startPoint = int(input("\nStart From EP Num:- "))
                if startPoint > epCount:
                    print(
                        "The Number you Enter Is Greater Than The Number Of The Episodes .\nEnter again.")
                    continue
                break
            except:
                print("Enter Number Only")
        self.createFolder()

        for tr in trs[startPoint-1:]:
            for dataAtt in ["data-url1080", "data-url", "data-url360"]:
                vidUrl = tr.attrs.get(dataAtt)
                if vidUrl:
                    break

            vidSrt = tr.attrs.get("data-srt")
            fileName = vidUrl.split('/')[-1]

            self.getMp4File(mp4Url=vidUrl, file_Name=fileName)
            self.getSrtFile(srtUrl=vidSrt, file_Name=fileName)
        return print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<GoodBye>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def getMovie(self):
        movie = self.soup.find(
            "a", {"class": "btn btn-success btn-block play"})
        movieName = movie.attrs.get("data-title")
        movieName = sub(r'[^a-zA-Z0-9]', ' ', movieName)
        movieName = movieName.split(" ")
        while True:
            if bool(movieName[-1]):
                break
            else:
                movieName.pop()
        self.mediaName = " ".join(movieName)

        self.createFolder()

        for dataAtt in ["data-url1080", "data-url", "data-url360"]:
            vidUrl = movie.attrs.get(dataAtt)
            if vidUrl:
                break

        vidSrt = movie.attrs.get("data-srt")
        fileName = vidUrl.split('/')[-1]

        self.file_path = self.mediaName + "/"
        self.getMp4File(mp4Url=vidUrl, file_Name=fileName)
        self.getSrtFile(srtUrl=vidSrt, file_Name=fileName)
        return print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<GoodBye>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def getMp4File(self, mp4Url, file_Name):
        try:
            if self.checkFile(filename=file_Name, search_path=self.file_path):
                return print(f"{file_Name}\n Already Exist The File Will Be Skipped.")

            print(f"\nStart Downloading :- {file_Name} ")
            response = requests.get(mp4Url, stream=True)
            total_size = int(response.headers.get("content-length", 0))

            with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
                for data in response.iter_content(self.block_size):
                    progress_bar.update(len(data))
                    self.fileBuffer.extend(data)
                with open(self.file_path+file_Name, "wb") as file:
                    file.write(self.fileBuffer)

            self.fileBuffer.clear()
            print(self.completeMes)
            if total_size != 0 and progress_bar.n != total_size:
                raise RuntimeError("Could not download file")
        except Exception as e:
            print(e)
        finally:
            sleep(1)

    def getSrtFile(self, srtUrl, file_Name):
        try:
            srtName = file_Name.replace(".mp4", ".srt")
            if self.checkFile(filename=srtName, search_path=self.file_path):
                return print(f"{srtName}\n Already Exist The File Will Be Skipped.")

            srt = requests.get(srtUrl).content
            with open(self.file_path+srtName, 'wb') as file:
                file.write(srt)
            print(f"Srt File Downloading Complete.")
        except Exception as e:
            print(e)
        finally:
            sleep(1)

    def createInfoFile(self):
        try:
            if getattr(sys, 'frozen', False):
                with open(f"{self.file_path}continueDonwload.bat", "w") as f:
                    f.write(f"""
@echo off
cd .. 
main.exe "{urlsafe_b64encode(self.url.encode()).decode()}"
exit
""")
            else:

                with open(f"{self.file_path}continueDonwload.py", "w") as f:
                    f.write(f"""
import subprocess
import platform
import os
venv_dir = ".venv"
system = platform.system()
if system == "Windows":
    venv_activate = os.path.join(venv_dir, "Scripts", "activate.bat")
elif system in ["Linux", "Darwin"]:  # macOS/Linux
    venv_activate = os.path.join(venv_dir, "bin", "activate")
else:
    print("Unsupported OS")
    exit()
def open_terminal(command, title):
    if system == "Windows":
        full_command = f'start cmd /k "cd.. && title {{title}} && {{venv_activate}} && {{command}}"'
        subprocess.Popen(full_command, shell=True)
    elif system == "Linux":
        full_command = f"gnome-terminal -- bash -c 'cd.. && source {{venv_activate}} && {{command}}; exec bash'"
        subprocess.Popen(full_command, shell=True)
    elif system == "Darwin":  # macOS
        full_command = f'osascript -e \\'tell application "Terminal" to do script "cd.. && source {{venv_activate}} && {{command}}"\\''
        subprocess.Popen(full_command, shell=True)

url="{urlsafe_b64encode(self.url.encode()).decode()}"
open_terminal(f"main.py {{url}}", "Vodu Dow")
""")
        except Exception as e:
            print(e)
        finally:
            sleep(1)

    def run(self):
        return self.checkUrl()


while True:
    match len(argv):
        case 1:
            url = input("Enter Vodu Url : ")
            media = voduGeter(url_=url)
            media.run()
        case _:
            media = voduGeter(url_=urlsafe_b64decode(
                argv[1].encode()).decode())
            media.run()
            break
