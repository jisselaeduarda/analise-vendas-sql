import sqlite3
import csv
from pathlib import Path

PASTA = Path(__file__).parent
BANCO = PASTA / "vendas.db"
CSV = PASTA / "vendas.csv"

def criar_dados():
    linhas = [
        ("2026-01-05", "Caderno", 10, 12.50),
        ("2026-01-08", "Caneta", 30, 2.00),
        ("2026-01-12", "Mochila", 3, 85.00),
        ("2026-02-02", "Caderno", 15, 12.50),
        ("2026-02-10", "Caneta", 45, 2.00),
        ("2026-02-14", "Mochila", 5, 85.00),
        ("2026-03-01", "Caderno", 8, 12.50),
        ("2026-03-04", "Caneta", 25, 2.00),
        ("2026-03-18", "Mochila", 2, 85.00),
    ]
    with sqlite3.connect(BANCO) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                produto TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL
            )
        """)
        conn.execute("DELETE FROM vendas")
        conn.executemany(
            "INSERT INTO vendas (data, produto, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
            linhas
        )

def exportar_csv():
    with sqlite3.connect(BANCO) as conn, open(CSV, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["data", "produto", "quantidade", "preco_unitario", "total"])
        for data, produto, qtd, preco in conn.execute(
            "SELECT data, produto, quantidade, preco_unitario FROM vendas ORDER BY data"
        ):
            escritor.writerow([data, produto, qtd, f"{preco:.2f}", f"{qtd * preco:.2f}"])

def mostrar_relatorios():
    with sqlite3.connect(BANCO) as conn:
        print("\n=== FATURAMENTO POR PRODUTO ===")
        for produto, quantidade, faturamento in conn.execute("""
            SELECT produto, SUM(quantidade), ROUND(SUM(quantidade * preco_unitario), 2)
            FROM vendas GROUP BY produto ORDER BY 3 DESC
        """):
            print(f"{produto}: {quantidade} unidades | R$ {faturamento:.2f}")

        print("\n=== FATURAMENTO POR MÊS ===")
        for mes, faturamento in conn.execute("""
            SELECT substr(data, 1, 7) AS mes, ROUND(SUM(quantidade * preco_unitario), 2)
            FROM vendas GROUP BY substr(data, 1, 7) ORDER BY mes
        """):
            print(f"{mes}: R$ {faturamento:.2f}")

        total = conn.execute(
            "SELECT ROUND(SUM(quantidade * preco_unitario), 2) FROM vendas"
        ).fetchone()[0]
        print(f"\nFaturamento total: R$ {total:.2f}")

if __name__ == "__main__":
    criar_dados()
    mostrar_relatorios()
    exportar_csv()
    print(f"\nArquivo CSV criado: {CSV.name}")
