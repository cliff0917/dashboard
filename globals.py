from database import get_db

def initialize():
    global posts, update_next_clicks, update2_next_clicks, initalization
    # 需要 sudo 密碼以存取檔案
    sudoPassword = 'uscc' # 0
    dir_path = '.'  # /var/ossec/logs/alerts
    update_next_clicks = 1
    update2_next_clicks = 1
    initalization = 1
    client, posts = get_db.get_current_db(dir_path, sudoPassword)