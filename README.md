# Vodu Movie Downloader
> A Cli App use to download Movies and Show form vodu

## Installation

1. Install dependencies mentioned inside [requirements.txt](requirements.txt) by opening terminal in project's directory and enter command
    ```
    pip install -r requirements.txt
    ```

## Run Global Environment

Run The [main.py](main.py) or use the terminal in project's directory
    
    python main.py

## Run Virtual Environment
Run The [run.py](run.py) it wall run the App aftere create virtual environment and install the requirements if it not exeist, This wall happen at the firts time you run it after that it automatcle active the the VM and run the App.

## Usage
1. If it was A Movie it wall create folder named after the movie and save it with .srt file in the folder.
2. In case of Show it wall display the episodes to select the start point and save thame in folder named after the show.

## Notes
* The App wall install the highest resolution available.
* The App wall skip the movie or the show episodes if it exist.
* Some time at download filed do to server error.
* The App add file named "continueDownload" In The Series or Movie Folder run it to continue Downloading Without Needed to enter The URL.