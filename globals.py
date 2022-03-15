from database import get_db

def initialize():
    global posts
    # 需要 sudo 密碼以存取檔案
    sudoPassword = 'uscc' # 0
    dir_path = '.'  # /var/ossec/logs/alerts
    client, posts = get_db.get_current_db(dir_path, sudoPassword)