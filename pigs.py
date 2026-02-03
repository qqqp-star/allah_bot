import json
import os
from datetime import datetime, timedelta

class PigSystem:
    def __init__(self):
        self.data_dir = 'data'
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
        
        self.file_path = os.path.join(self.data_dir, 'pigs.json')
        self.load_data()
        self.cooldown_hours = 4
        self.admin_id = "898569707433656370"  # Твой Discord ID
    
    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"✅ Данные свиней загружены ({len(self.data)} записей)")
            except:
                self.data = {}
        else:
            self.data = {}
            print("📁 Файл свиней не найден, создаём новый")
    
    def save_data(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def get_or_create_pig(self, user_id, user_name):
        user_id = str(user_id)
        
        if user_id not in self.data:
            self.data[user_id] = {
                'name': user_name,
                'weight': 1.0,
                'feed_count': 0,
                'created': datetime.now().isoformat(),
                'last_feed': None,
                'level': 1,
                'next_feed': None
            }
            self.save_data()
        
        return self.data[user_id]
    
    def can_feed(self, user_id):
        pig = self.get_or_create_pig(user_id, "Unknown")
        
        # Админ всегда может кормить
        if str(user_id) == self.admin_id:
            return True, None
        
        if not pig['last_feed']:
            return True, None
        
        try:
            last_feed_time = datetime.fromisoformat(pig['last_feed'])
            cooldown_end = last_feed_time + timedelta(hours=self.cooldown_hours)
            now = datetime.now()
            
            if now >= cooldown_end:
                return True, None
            else:
                remaining = cooldown_end - now
                return False, remaining
        except:
            return True, None
    
    def feed_pig(self, user_id, user_name):
        pig = self.get_or_create_pig(user_id, user_name)
        
        now = datetime.now()
        next_feed = now + timedelta(hours=self.cooldown_hours)
        
        pig['weight'] = round(pig['weight'] + 5, 2)
        pig['feed_count'] += 1
        pig['last_feed'] = now.isoformat()
        pig['next_feed'] = next_feed.isoformat()
        
        old_level = pig['level']
        new_level = min(pig['weight'] // 50 + 1, 10)
        pig['level'] = int(new_level)
        
        self.save_data()
        
        level_up = new_level > old_level
        
        if str(user_id) == self.admin_id:
            pig['next_feed'] = None
            self.save_data()
        
        return pig, level_up
    
    def get_pig(self, user_id):
        user_id = str(user_id)
        return self.data.get(user_id)
    
    def get_top_pigs(self, limit=10):
        pigs = list(self.data.items())
        pigs.sort(key=lambda x: x[1]['weight'], reverse=True)
        return pigs[:limit]
    
    def get_user_rank(self, user_id):
        user_id = str(user_id)
        top = self.get_top_pigs(limit=100)
        
        for i, (uid, _) in enumerate(top):
            if uid == user_id:
                return i + 1
        
        return None

pig_system = PigSystem()