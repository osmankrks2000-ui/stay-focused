from flask import Blueprint, render_template, request, jsonify
from .database import add_lead, all_leads
from .services.groq_service import generate_reply, GroqServiceError

pages = Blueprint('pages', __name__)
api = Blueprint('api', __name__)

@pages.get('/')
def home():
    return render_template('index.html')

@pages.get('/panel')
def panel():
    return render_template('dashboard.html')

@api.post('/leads')
def leads():
    data = request.get_json(silent=True) or request.form
    name = str(data.get('name','')).strip()
    if not name:
        return jsonify(success=False, error='Ad Soyad zorunludur.'), 400
    add_lead(name, str(data.get('email','')).strip(), str(data.get('phone','')).strip(), str(data.get('message','')).strip())
    return jsonify(success=True, message='Bilgileriniz başarıyla alındı.')

@api.get('/leads')
def lead_list():
    rows = all_leads()
    return jsonify(success=True, total=len(rows), leads=rows)

@api.post('/chat')
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get('message', '')).strip()
    if not message:
        return jsonify(success=False, error='Mesaj boş olamaz.'), 400
    if len(message) > 2000:
        return jsonify(success=False, error='Mesaj en fazla 2000 karakter olabilir.'), 400

    history = data.get('history', [])
    try:
        answer = generate_reply(message, history)
        return jsonify(success=True, answer=answer)
    except GroqServiceError as exc:
        return jsonify(success=False, error=str(exc)), 503
    except Exception:
        # Ayrıntıları kullanıcıya veya tarayıcıya sızdırma.
        return jsonify(success=False, error='Beklenmeyen bir hata oluştu. Sunucu kayıtlarını kontrol edin.'), 500
