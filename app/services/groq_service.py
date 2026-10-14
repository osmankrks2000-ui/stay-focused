"""Groq API bağlantısı: API anahtarı yalnızca sunucu tarafında kullanılır."""
import os
from groq import Groq
from groq import APIConnectionError, APIStatusError, APITimeoutError

SYSTEM_PROMPT = """
Sen Stay Focused markasının Türkçe konuşan dijital asistanısın.
Marka; gizli nesne ve görsel keşif kitaplarıyla dikkat, keşif ve analog
zaman deneyimini desteklemeyi amaçlar. Samimi, kısa, anlaşılır ve profesyonel
yanıt ver. Marka, fiyat, stok, teslimat veya satın alma hakkında doğrulanmamış
bilgiler uydurma; emin değilsen iletişim formuna yönlendir. Sağlık konusunda
kesin tedavi iddialarında bulunma.
""".strip()


class GroqServiceError(Exception):
    """Kullanıcıya gösterilebilecek güvenli Groq bağlantı hatası."""


def generate_reply(message: str, history=None) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise GroqServiceError(
            "Groq API anahtarı ayarlanmamış. Proje klasöründeki .env dosyasını kontrol edin."
        )

    client = Groq(api_key=api_key, timeout=30.0, max_retries=1)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Önceki mesajları sınırla ve yalnızca beklenen rollerin geçmesine izin ver.
    if isinstance(history, list):
        for item in history[-10:]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            content = item.get("content")
            if role in ("user", "assistant") and isinstance(content, str) and content.strip():
                messages.append({"role": role, "content": content.strip()[:2000]})

    messages.append({"role": "user", "content": message[:2000]})

    try:
        result = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
            messages=messages,
            temperature=0.6,
            max_tokens=700,
        )
        answer = result.choices[0].message.content
        if not answer:
            raise GroqServiceError("Asistan boş yanıt döndürdü. Lütfen tekrar deneyin.")
        return answer.strip()
    except APITimeoutError as exc:
        raise GroqServiceError("Yapay zekâ yanıtı zaman aşımına uğradı. Tekrar deneyin.") from exc
    except APIConnectionError as exc:
        raise GroqServiceError("Groq servisine bağlanılamadı. İnternet bağlantısını kontrol edin.") from exc
    except APIStatusError as exc:
        if exc.status_code in (401, 403):
            raise GroqServiceError("Groq API anahtarı geçersiz veya yetkisiz.") from exc
        if exc.status_code == 429:
            raise GroqServiceError("Groq istek sınırına ulaşıldı. Biraz sonra tekrar deneyin.") from exc
        raise GroqServiceError(f"Groq API isteği başarısız oldu (HTTP {exc.status_code}).") from exc
