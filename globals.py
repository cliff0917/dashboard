from database import connect

def initialize(): 
    global posts, update_next_clicks, update2_next_clicks
    # 需要 sudo 密碼以存取檔案
    sudoPassword = 'uscc' # 0
    dir_path = '.'  # /var/ossec/logs/alerts
    update_next_clicks = 1
    update2_next_clicks = 1
    client, posts = connect.connect_db(dir_path, sudoPassword)