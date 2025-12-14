"""
reset_db.py
-------------------------------------
Script para limpar todas as tabelas do banco de dados chatbot.db
sem apagar a estrutura das tabelas.

Este script:
 - Remove todos os registros de conversations e safety_logs
 - Reseta os IDs automáticos (autoincremento)
 - Fecha a conexão com segurança

Uso:
    python reset_db.py
"""

import sqlite3

def reset_database(db_name="chatbot.db"):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Apaga registros de todas as tabelas principais
        cur.execute("DELETE FROM conversations;")
        cur.execute("DELETE FROM safety_logs;")

        # Reseta o contador de IDs automáticos
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('conversations', 'safety_logs');")

        conn.commit()
        conn.close()

        print("✅ Banco de dados limpo com sucesso!")
        print("Todas as conversas e logs foram removidos, e os IDs foram resetados.")
    except Exception as e:
        print(f"❌ Erro ao limpar o banco de dados: {e}")

if __name__ == "__main__":
    reset_database()
