# Stay Focused — Marka Web Projesi

Bu proje, Stay Focused pazarlama metnindeki marka yaklaşımını çalışan bir web prototipine dönüştürür.

## İçerik
- Premium marka tanıtım / landing page
- Gizli nesne ve odaklanma odaklı marka anlatımı
- Ziyaretçi iletişim formu
- SQLite müşteri adayı kaydı
- Yönetim paneli (`/panel`)
- Stay Focused dijital asistanı (`/api/chat`)
- Flask backend + REST API

## Kurulum
```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
python baslat.py
```

Tarayıcı: http://localhost:5000
Yönetim paneli: http://localhost:5000/panel

## Not
AI sohbeti bu pakette demo mantığıyla çalışır. Gerçek bir yapay zekâ API'si eklemek için `.env` ve `app/routes.py` içindeki `/api/chat` servisi genişletilebilir.
