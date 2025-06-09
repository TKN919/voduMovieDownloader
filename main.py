import requests
from bs4 import BeautifulSoup
from time import sleep
from os import makedirs, walk
from re import sub
from tqdm import tqdm


class voduGeter:
    def __init__(self, url_):
        self.url = url_
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
            return print("Enter Vodu Show Or Movie Url Only.\n")

    def checkType(self):
        self.show = self.soup.find("div", {"class": "col-md-12 customtabs"})

        if self.show:
            self.completeMes = "Show Episodes Downloading Complete."
            return self.getShow()
        else:
            self.completeMes = "Moive Downloading Complete."
            return self.getMovie()

    def checkFile(self, filename, search_path):
        for root, dir, files in walk(search_path):
            if filename in files:
                return True
        return False

    def getShow(self):
        trs = self.show.find_all("a", {"class": "btn btn-success play"})
        epNamesTrs = self.show.find_all(
            "div", {"class": "col-md-7 col-xs-12 col-sm-8"})
        for index, ep in enumerate(epNamesTrs):
            print(f"{index+1} - {ep.getText()}")

        showName = self.soup.find(
            "div", {"class": "col-lg-5"}).find("h1").getText()

        showName = sub(r'[^a-zA-Z0-9]', ' ', showName)
        showName = showName.split(" ")
        while True:
            if bool(showName[-1]):
                break
            else:
                showName.pop()
        showName = " ".join(showName)
        epCount = len(epNamesTrs)
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
        makedirs(showName, exist_ok=True)

        for tr in trs[startPoint-1:]:
            for dataAtt in ["data-url1080", "data-url", "data-url360"]:
                vidUrl = tr.attrs.get(dataAtt)
                if vidUrl:
                    break

            vidSrt = tr.attrs.get("data-srt")
            fileName = vidUrl.split('/')[-1]
            filePath = showName + "/"

            self.getMp4File(mp4Url=vidUrl, file_Name=fileName,
                            file_Path=filePath)
            self.getSrtFile(srtUrl=vidSrt, file_Name=fileName,
                            file_Path=filePath)
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
        movieName = " ".join(movieName)

        makedirs(movieName, exist_ok=True)

        for dataAtt in ["data-url1080", "data-url", "data-url360"]:
            vidUrl = movie.attrs.get(dataAtt)
            if vidUrl:
                break

        vidSrt = movie.attrs.get("data-srt")
        fileName = vidUrl.split('/')[-1]

        filePath = movieName + "/"
        self.getMp4File(mp4Url=vidUrl, file_Name=fileName,
                        file_Path=filePath)
        self.getSrtFile(srtUrl=vidSrt, file_Name=fileName, file_Path=filePath)
        return print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<GoodBye>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    def getMp4File(self, mp4Url, file_Name, file_Path):
        try:
            if self.checkFile(filename=file_Name, search_path=file_Path):
                return print(f"{file_Name}\n Already Exist The File Will Be Skipped.")

            print(f"\nStart Downloading :- {file_Name} ")
            response = requests.get(mp4Url, stream=True)
            total_size = int(response.headers.get("content-length", 0))

            with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
                for data in response.iter_content(self.block_size):
                    progress_bar.update(len(data))
                    self.fileBuffer.extend(data)
                with open(file_Path+file_Name, "wb") as file:
                    file.write(self.fileBuffer)

            self.fileBuffer.clear()
            print(self.completeMes)
            if total_size != 0 and progress_bar.n != total_size:
                raise RuntimeError("Could not download file")
        except Exception as e:
            print(e)
        finally:
            sleep(1)

    def getSrtFile(self, srtUrl, file_Name, file_Path):
        try:
            srtName = file_Name.replace(".mp4", ".srt")
            if self.checkFile(filename=srtName, search_path=file_Path):
                return print(f"{srtName}\n Already Exist The File Will Be Skipped.")

            srt = requests.get(srtUrl).content
            with open(file_Path+srtName, 'wb') as file:
                file.write(srt)
            print(f"Srt File Downloading Complete.")
        except Exception as e:
            print(e)
        finally:
            sleep(1)

    def run(self):
        return self.checkUrl()


while True:
    url = input("Enter Vodu Url : ")
    voduGeter(url_=url).run()
