import json
import os
from datetime import datetime

class StatsDatabase:
    def __init__(self):
        self.data_dir = 'data'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
        
        self.file_path = os.path.join(self.data_dir, 'stats.json')
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"✅ Статистика загружена ({len(self.data)} пользователей)")
            except:
                self.data = {}
        else:
            self.data = {}
            print("📁 Файл статистики не найден, создаём новый")
    
    def save_data(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def add_message(self, user_id, user_name):
        user_id = str(user_id)
        
        if user_id not in self.data:
            self.data[user_id] = {
                'name': user_name,
                'messages': 0,
                'last_seen': datetime.now().isoformat(),
                'first_seen': datetime.now().isoformat()
            }
        
        self.data[user_id]['messages'] += 1
        self.data[user_id]['name'] = user_name
        self.data[user_id]['last_seen'] = datetime.now().isoformat()
        self.save_data()
    
    def get_top_users(self, limit=10):
        users = list(self.data.items())
        users.sort(key=lambda x: x[1]['messages'], reverse=True)
        return users[:limit]
    
    def get_user_stats(self, user_id):
        user_id = str(user_id)
        return self.data.get(user_id)

stats_db = StatsDatabase()