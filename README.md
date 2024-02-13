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

接著，進入到專案的目錄中：

```bash
cd youtube_stream_monitoring
```

2. 安裝必要的套件

然後，我們需要安裝專案中所需的 Python 套件。這些套件已經在 `requirements.txt` 檔案中列出。在命令列中輸入以下指令來進行安裝：

```bash
pip install -r requirements.txt
```

3. 遷移資料庫

在命令列中輸入以下指令來進行遷移：

```bash
./manage.py makemigrations
./manage.py migrate
```

### 系統服務啟動

當系統建置完成後，我們需要啟動後端和前端的服務。以下是詳細的操作步驟：

#### 後端服務
請在終端機輸入以下指令以啟動後端服務：
```bash
python manage.py runserver
```

#### Endpoint  
```
http://localhost:8000/api/live/check-live-status/
```
#### Method
- POST  

#### Request Body
請求內容應以 JSON 格式提交，並包含 YouTube網址或影片id。

Example:  
以lofi girl為例
```json
{
  "youtube_url": "https://www.youtube.com/live/jfKfPfyJRdk?si=G99O-XzZ-tN1M8Kb"
}
```

#### Response
如果 YouTube 直播正在進行：
```json
{
  "live_status": true
}
```  

如果 YouTube 直播未在進行或非直播影片(shorts、影片、直播存檔)：  
```json
{
  "live_status": false
}
```  

#### 如何使用
您可以使用不同的方法來調用此 API，例如使用 curl 命令列工具或使用類似 Postman 的工具。以下是使用 curl 的範例：

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"youtube_url\": \"https://www.youtube.com/live/jfKfPfyJRdk?si=G99O-XzZ-tN1M8Kb\"}" http://localhost:8000/api/live/check-live-status/
```

