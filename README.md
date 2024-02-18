# youtube_stream_monitoring
## 需求說明
請製作一個監控網頁，輸入網址後可以，確認youtube的直播是否斷線  
### 建議規格
請使用django作為後端api框架 前端框架不拘，畫面上可輸入url進行監控，輸出目前直播狀態  
推薦使用chat_downloader這個lib https://github.com/xenova/chat-downloader 可以用來確認直播的狀態  
最後請將開發完成的程式上傳至github，並於readme提供必要的部署說明

### 補充說明
>該監控網頁的狀態刷新率為多少?

5分鐘抓一次即可

## Quick Start  
### 環境需求
- Python 3.10.11  
1. 下載專案原始碼

首先從 GitHub 下載專案的原始碼。請在命令列中輸入以下指令：

```bash
git clone https://github.com/Wayne40406130/youtube_stream_monitoring.git
```

2. 接著，進入到專案的目錄中：

```bash
cd youtube_stream_monitoring
```
接下來有兩種方式部署系統，任選一即可  
### 1.Docker  
請確保已經安裝[docker](https://www.docker.com/products/docker-desktop/)  
1. build image
在terminal執行以下的指令：  
`docker build -t docker_youtube_stream_monitoring .`  
等待執行完成後進入下一步  
2. 查看images  
在terminal執行以下的指令： 
`docker images`  
確認是否有叫`docker_youtube_stream_monitoring`的image  
```bash
REPOSITORY                         TAG       IMAGE ID       CREATED         SIZE  
docker_youtube_stream_monitoring   latest    3a92f26d64a2   7 minutes ago   298MB 
```
3. run container  
在terminal執行以下的指令： 
`docker run -p 8000:8000 docker_youtube_stream_monitoring`
### 2.傳統方式
1. 安裝必要的套件

然後，我們需要安裝專案中所需的 Python 套件。這些套件已經在 `requirements.txt` 檔案中列出。在命令列中輸入以下指令來進行安裝：

```bash
pip install -r requirements.txt
```

2. 遷移資料庫

在命令列中輸入以下指令來進行遷移：

```bash
./manage.py makemigrations
./manage.py migrate
```

3. 系統服務啟動

在終端機輸入以下指令以啟動後端服務：
```bash
python manage.py runserver
```

## 使用說明  
**以下全程預設保持runserver的狀態下**
### 文件  
在瀏覽器輸入`http://127.0.0.1:8000/swagger/`檢視swagger文件  
輸入`http://127.0.0.1:8000/redoc/`檢視redoc文件

### Endpoint  
```
http://localhost:8000/api/live/check-live-status/
```
### Method
- GET  

參數帶`youtube_url:<youtube url>` 或是`youtube_url:<video id>`
Example:  
以lofi girl為例，網址:
```json
{
  "youtube_url": "https://www.youtube.com/live/jfKfPfyJRdk?si=G99O-XzZ-tN1M8Kb"
}
```

video id:
```json
{
  "youtube_url": "jfKfPfyJRdk"
}
```

#### Response  
直播狀態以`live_status`的boolean為主  
如果 YouTube 直播正在進行：  
```json
{
    "title": "lofi hip hop radio 📚 - beats to relax/study to",
    "channel_name": "Lofi Girl",
    "channel_id": "UCSJ4gkVC6NrvII8umztf0Ow",
    "video_id": "jfKfPfyJRdk",
    "URL": "https://www.youtube.com/watch?v=jfKfPfyJRdk",
    "live_status": true
}
```  

如果 YouTube 直播未在進行或非直播影片(shorts、影片、直播存檔)，以公視直播存檔為例：  
```json
{
    "title": "新北跨河煙火秀 | #2024跨年煙火 #1314 #新北煙火 #淡水河岸 #八里 (感謝提供:新北市政府)",
    "channel_name": "公視 網路直播頻道",
    "channel_id": "UCXgIO9jJVsX5_2ideiSkfvA",
    "video_id": "l-v8B4GnIWc",
    "URL": "https://www.youtube.com/watch?v=l-v8B4GnIWc",
    "live_status": false
}
```  

#### 如何使用  
##### 從前端使用
打開`index.html`，在文字框中輸入直播網址，點選"Add Live Status"  
若直播正常則Live Status: Live，反之為Not Live  
可以按紅色X清除掉監控  
如果server有問題會顯示出來  
##### 呼叫API
例如使用 curl 命令列工具或使用類似 Postman 的工具。以下是使用 curl 的範例：

```bash
curl -X GET http://localhost:8000/api/live/check-live-status/?youtube_url=https://www.youtube.com/live/jfKfPfyJRdk?si=G99O-XzZ-tN1M8Kb
```

#### 測試
該專案用了[pytest](https://pytest-django.readthedocs.io/en/latest/tutorial.html) 進行測試  
1. 若使用的是docker  
需先在terminal輸入:
`docker container ls`  
查看執行中的container id是甚麼，例如:
```bash
CONTAINER ID   IMAGE      COMMAND                   CREATED              STATUS
     PORTS                    NAMES
015a84306c24   letmetry   "python manage.py ru…"   About a minute ago   Up About a minute   0.0.0.0:8000->8000/tcp   dazzling_goodall
```
`015a84306c24`就是該container的id  

接著執行:
`docker exec -it 015a84306c24 /bin/bash`  
進入docker shell當中。  

2. 若使用的是一般方法  
**保持runserver的狀態**  


在terminal輸入pytest來進行測試  
```bash
pytest
```
另外也可以帶一些參數
- -s: The -s parameter is just to allow your print statements to write to the console, if you want that, else you can just run pytest.
- -k <expression>: matches a file, class or function name inside the tests folder that contains the indicated expression.
- -m <marker>: will run all tests with the inputed marker.
- -m "not <marker>": will run all tests that don’t have the inputed marker.
- -x: stops running tests once a test fails, letting us stop the test-run right there so we can go back to debugging our test instead of waiting for the test suite to finish running.
- --lf: starts running the test suite from the last failed test, perfect to avoid continiously running tests we already know pass when debuggin.
- -vv: shows a more detailed version of a failed assertion.
- --cov: show % of tests covered by tests (depends on pytest-cov plugin).
- --reruns <num_of_reruns>: used for dealing with flaky tests, tests that fail when run in the test suite but pass when run alone.  

for example:
```bash
pytest -s -vv -x
```