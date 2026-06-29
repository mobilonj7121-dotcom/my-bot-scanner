import requests
from bs4 import BeautifulSoup

def fetch_data(url):
    # Додаємо заголовки, щоб сайт думав, що ми звичайний браузер, а не бот
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Робимо запит на сайт
        response = requests.get(url, headers=headers)
        
        # Перевіряємо, чи успішний запит (статус 200 означає "Все ОК")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Шукаємо головний заголовок сайту
            title = soup.title.string if soup.title else "Заголовок не знайдено"
            return f"✅ Успіх! Заголовок сайту: {title}"
        else:
            return f"❌ Помилка доступу до сайту. Статус: {response.status_code}"
            
    except Exception as e:
        return f"❌ Сталася помилка: {e}"
      
