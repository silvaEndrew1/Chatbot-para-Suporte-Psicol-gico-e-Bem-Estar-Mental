# Regras de segurança (filtros)

import re
from db import log_safety

SAFETY_BANNER = (
    "⚠️ AVISO IMPORTANTE!!!\n"
    "Sou um assistente virtual de apoio emocional inicial — não substituo psicoterapia ou atendimento médico.\n"
    "Se estiver em perigo imediato ou pensando em se ferir, procure ajuda agora:\n"
    "• Brasil: 188 (CVV – 24h) | 190 (emergência) | SAMU 192.\n"
    "• Fale com alguém de confiança ou procure um serviço de saúde próximo.\n"
)

CRISIS_PATTERNS = [
    r"\b(quero|vou|penso em|tenho vontade de)\s+(me\s+)?(matar|morrer|sumir)\b",
    r"\b(não aguento mais|sem saída|vida sem sentido)\b",
    r"\b(suic[ií]dio|tirar minha vida)\b",
    r"\b(autoles(ão|ao)|me cortar|me ferir)\b",
]

def check_crisis(user_id: str, text: str):
    t = text.lower()
    for pat in CRISIS_PATTERNS:
        if re.search(pat, t):
            log_safety(user_id, text, pat)
            return True
    return False

