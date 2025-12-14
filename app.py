# Flask (API + UI simples)

from flask import Flask, render_template, request, redirect, url_for
from db import save_turn, last_messages
from safety import SAFETY_BANNER
from bot_core import respond
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# Configurações de fuso horário
TZ_SP = ZoneInfo("America/Sao_Paulo")
TZ_UTC = ZoneInfo("UTC")

app = Flask(__name__)

USER_ID = "demo"

# Função utilitária para converter UTC → SP
def to_sp(ts: str) -> str:
    """Converte timestamp ISO para formato legível em São Paulo"""
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            # assume fuso SP se não houver info de timezone
            dt = dt.replace(tzinfo=TZ_SP)
        dt_sp = dt.astimezone(TZ_SP)
        # Exibe no formato '08/10 às 21h36'
        return dt_sp.strftime("%d/%m às %Hh%M")
    except Exception:
        return ""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        msg = request.form.get("msg", "").strip()
        if msg:
            bot_msg, intent, crisis, sentiment = respond(USER_ID, msg)
            save_turn(USER_ID, msg, bot_msg, sentiment, intent, crisis)
        return redirect(url_for("index"))

    # Carrega últimas mensagens
    rows = last_messages(50)
    history = [(u, b, to_sp(ts)) for (u, b, ts) in rows]
    return render_template("index.html", history=history, safety_banner=SAFETY_BANNER)

if __name__ == "__main__":
    app.run(debug=True)
