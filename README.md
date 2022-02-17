# dashboard
## 環境安裝
```
sudo apt-get install mongodb
conda create -y -n dashboard python=3.7
conda activate dashboard
pip install -r requirements.txt
python main.py
```

## 常見問題
oserror: [errno 98] address already in use

使用以下指令
```
sudo lsof -t -i tcp:8050 | xargs kill -9
```
