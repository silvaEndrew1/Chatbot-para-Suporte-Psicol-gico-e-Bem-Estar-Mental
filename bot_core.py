# Núcleo do bot (intents + regras)

import random
import json
from typing import Optional, Tuple
from nlp_utils import analyze_sentiment
from safety import SAFETY_BANNER, check_crisis
from markupsafe import Markup

with open("seed_corpus.json", "r", encoding="utf-8") as f:
    CORPUS = json.load(f)


INTENT_RESPONSES = {
    "saudacao": [
        "Olá! Estou aqui para te ouvir. Quer me contar um pouco de como tem se sentido?",
        "Olá! Se quiser, pode me contar como tem se sentido ultimamente.",
        "Oi! Estou aqui para te ouvir — como você tem se sentido hoje?",
        "Olá! Estou à disposição para te escutar. Quer começar me dizendo como está?",
        "Oi, tudo bem? Fique à vontade para desabafar, estou aqui com você.",
        "Olá, espero que seu dia esteja leve. Quer conversar um pouco sobre o que tem vivido?",
        "Oi, pode me contar como tem se sentido ultimamente, se quiser.",
        "Olá, tudo bem por aí? Às vezes só falar um pouco já ajuda a aliviar."
    ],
    "ansiedade": [
        """Sinto que pode haver ansiedade aí. Topa um exercício rápido de respiração? "
        • Inspire pelo nariz (4s) • Segure (4s) • Expire pela boca (6s) • Repita por 1–2 min. 
        Se quiser, posso guiar um grounding 5-4-3-2-1.""",
        "Parece que a ansiedade está presente. Podemos tentar juntos 2 minutos de respiração 4-4-6? Se preferir, faço um grounding 5-4-3-2-1 com você.",
        "Entendo — a ansiedade pode pesar. Que tal fazermos respirações profundas por 1 minuto e depois um grounding rápido?",
        "Percebo sinais de ansiedade. Vamos experimentar 4 ciclos de respiração 4-4-6 e, se quiser, seguimos com grounding 5-4-3-2-1.",
        "Parece que seu corpo está pedindo uma pausa. Respire fundo — às vezes, um momento de calma já muda tudo.",
        "A ansiedade pode ser intensa, mas ela não te define. Você está seguro aqui comigo, respira um pouco.",
        "Entendo essa sensação, ela pode vir do nada. Vamos com calma, um passo de cada vez.",
        "Pode ser difícil lidar com isso, mas reconhecer o que sente já é um começo importante."
    ],
    "tristeza": [
        """Sinto muito que esteja passando por isso. Podemos explorar 3 pontos?
         1) Como você se sente agora; 2) O que aconteceu antes; 3) O que já ajudou outras vezes.""",
        "Imagino que esteja difícil. Podemos olhar juntos para 3 coisas: 1) como está agora; 2) o que antecedeu isso; 3) o que costuma aliviar um pouco.",
        "Sinto pelo momento delicado. Te proponho 3 passos: 1) nomear o que sente; 2) reconhecer gatilhos; 3) lembrar do que já funcionou.",
        "Obrigado por confiar em mim. Vamos por partes: 1) sentir; 2) entender o contexto; 3) resgatar estratégias que já ajudaram.",
        "Parece que esse momento está pesado. Às vezes, só ter alguém pra ouvir já ajuda um pouco.",
        "Sinto muito que esteja passando por isso. Você não está sozinho, e é válido se sentir assim.",
        "Tudo bem não estar bem o tempo todo. Estou aqui pra te ouvir sem julgamentos.",
        "Quando a tristeza aparece, ela costuma pedir acolhimento. Podemos conversar com calma sobre isso."
    ],
    "estresse": [
        "Vamos montar um plano de 10 minutos: 3 min respiração, 5 min listar 3 tarefas pequenas, 2 min pausa consciente. Bora?",
        "Topa um plano rápido? 3 min de respiração + 5 min para quebrar uma tarefa grande em pequenas + 2 min de pausa consciente.",
        "Sugestão de 10 minutos: 3 min respirando, 5 min definindo 3 micro-passos, 2 min apenas observando a respiração.",
        "Que tal um reset breve: 3 min de ar consciente, 5 min de foco em 3 passos simples, 2 min de descanso intencional.",
        "O estresse pode ser um sinal de que você precisa parar um pouco. Permita-se respirar e desacelerar.",
        "Quando o corpo e a mente pedem descanso, é um lembrete pra se cuidar. Vamos tentar diminuir o ritmo por uns minutos?",
        "Estresse é comum, mas ele não precisa te dominar. Às vezes, pequenas pausas fazem toda diferença.",
        "Parece que você está sobrecarregado. Que tal dar um tempo pra si mesmo agora?"
    ],
    "sono": [
        "Higiene do sono ajuda: rotina regular, menos telas 1h antes, ambiente escuro e fresco. Descreve sua noite típica?",
        "Vamos cuidar do sono? Tente horários regulares, reduzir telas 1h antes e deixar o quarto mais escuro e silencioso. Como tem sido sua noite?",
        "Sono melhor começa de dia: luz natural pela manhã, rotina estável e menos estímulo à noite. Quer me contar como está sua rotina?",
        "Podemos ajustar hábitos noturnos: evitar cafeína à tarde, diminuir telas, banho morno e ambiente confortável. Como costuma ser seu pré-sono?",
        "O descanso é essencial. Às vezes, o corpo precisa de um ritual de desacelerar antes de dormir.",
        "Seu sono anda leve ou agitado? Às vezes pequenas mudanças já trazem melhora.",
        "Dormir bem é um autocuidado importante. Podemos conversar sobre o que anda te atrapalhando à noite?",
        "Parece que o sono tem sido um desafio. Quer compartilhar o que costuma dificultar suas noites?"
    ],
    "autocuidado": [
        "Micro-plano para hoje: 1 copo d’água agora, 5 min de alongamento, refeição simples e enviar msg para alguém de confiança.",
        "Plano curtinho: beber água agora, alongar por 5 min, fazer uma refeição simples e falar com alguém de confiança.",
        "Vamos de pequenos cuidados: hidratar-se, alongar 5 min, algo leve para comer e um contato com alguém que te faça bem.",
        "Autocuidado prático: água + alongamento rápido + alimentação simples + uma mensagem para quem te apoia.",
        "Cuidar de si mesmo também é descansar quando o corpo pede. Isso é autocuidado.",
        "Autocuidado não precisa ser complexo — basta se ouvir e atender pequenas necessidades do dia.",
        "Valorize pequenos gestos de carinho consigo mesmo, eles somam muito com o tempo.",
        "O autocuidado começa nas coisas simples: respirar fundo, se alimentar bem e respeitar o seu ritmo."
    ],
    "gratidao": [
       "Prática rápida: escreva 3 coisas boas de hoje (mesmo pequenas). Posso guardar nesta conversa.",
        "Exercício breve: liste 3 pequenas coisas que trouxeram um pouco de bem-estar hoje. Posso anotar aqui.",
        "Que tal registrar 3 acontecimentos positivos do dia, por menores que sejam? Isso ajuda a reequilibrar o olhar.",
        "Às vezes, até um pequeno momento bom pode mudar o dia. Consegue lembrar de algo assim?",
        "Praticar gratidão é perceber o que deu certo, mesmo nos dias difíceis. Quer tentar agora?",
        "Você quer compartilhar algo bom que aconteceu hoje? Às vezes reconhecer isso já acalma o coração.",
        "Gratidão é olhar com carinho pro que temos. Há algo de positivo que queira registrar?"
    ],
    "encerrar": [
        "Obrigado por conversar. Lembre: buscar um profissional é um gesto de cuidado. Se precisar, estou aqui. ❤️",
        "Agradeço nossa conversa. Se sentir necessidade, procurar um profissional pode ser um passo importante. Estarei por aqui.",
        "Foi bom conversar com você. Quando quiser, retornamos. E, se fizer sentido, considere apoio profissional.",
        "Obrigado pela confiança. Quando precisar, volto a te ouvir. Cuidar-se inclui pedir ajuda quando necessário.",
        "Fico feliz por termos conversado. Cuide-se, e lembre-se de que pedir ajuda é força, não fraqueza.",
        "Gratidão pela troca. Se algo pesar, não hesite em procurar alguém de confiança ou um profissional.",
        "Que bom ter te ouvido hoje. Continue se cuidando e respeitando o seu tempo.",
        "Encerramos por agora, mas estarei por aqui sempre que quiser conversar de novo."
    ],
    "smalltalk": [  # respostas variadas para entradas pequenas/comuns
        "Que ótimo! Fique à vontade para conversar comigo sempre que quiser. 😊",
        "Legal! Estou por aqui caso queira desabafar ou conversar um pouco. 💬",
        "Tudo bem! Posso te mostrar algumas dicas para cuidar da sua saúde mental?",
        "Fico feliz em saber! Lembre-se: cuidar de si mesmo é importante. ❤️",
        "Que bom! Se quiser, posso te ensinar uma técnica de relaxamento.",
        "Beleza 😄 Quer conversar sobre como tem se sentido ultimamente?",
        "Tranquilo! Sempre que quiser, pode mandar uma mensagem, estou por aqui.",
        "Perfeito! Às vezes só conversar já faz diferença. 🌻",
        "Tudo certo então! Se quiser, posso te sugerir algo para manter o bem-estar.",
        "Ótimo! Quer ver algumas frases motivacionais ou dicas de autocuidado?"
    ],
}

FALLBACK = (
    "Desculpe, acho que não entendi muito bem o que você quis dizer. "
    "Pode tentar explicar de outro jeito? Estou aqui para te ouvir."
)

def detect_intent(text: str) -> Optional[str]:
    t = text.lower()
    # matching simples por palavras do seed_corpus
    best, score = None, 0
    for intent, kws in CORPUS.items():
        s = sum(1 for kw in kws if kw in t)
        if s > score:
            best, score = intent, s
    return best if score > 0 else None

# bot_core.py
import random

def respond(user_id: str, text: str):
    # 1) safety
    crisis = 1 if check_crisis(user_id, text) else 0
    if crisis:
        '''return (
            "Sinto muito que esteja enfrentando algo tão pesado. Sua vida é importante.\n\n" + SAFETY_BANNER,
            "crise", crisis, "unknown"
        )'''
        return (
            f"<div class='safety-msg'>"
            f"Sinto muito que esteja enfrentando algo tão pesado. Sua vida é importante.<br><br>"
            f"{SAFETY_BANNER}</div>",
            "crise", crisis, "unknown"
        )
        
    # 2) intent
    intent = detect_intent(text)

    # 3) sentimento (Transformers com fallback)
    sentiment = analyze_sentiment(text)

    # 4) resposta por intent conhecida
    if intent in INTENT_RESPONSES:
        resp = INTENT_RESPONSES[intent]
        if isinstance(resp, list):
            resp = random.choice(resp)
        return (resp, intent, crisis, sentiment)

    # 5) heurística de smalltalk (curtas/neutras), cai no smalltalk palavras curtas <=2.
    t = text.lower().strip()
    if len(t.split()) <= 2 or any(p in t for p in [
        "apenas", "só testando", "so testando", "testando", "mensagem",
        "ok", "beleza", "certo", "de boas", "de boa", "somente isso"
    ]):
        resp = INTENT_RESPONSES.get("smalltalk", FALLBACK)
        if isinstance(resp, list):
            resp = random.choice(resp)
        return (resp, "smalltalk", crisis, sentiment)

    # 6) fallback
    return (FALLBACK, "fallback", crisis, sentiment)
