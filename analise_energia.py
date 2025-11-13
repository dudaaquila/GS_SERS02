import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# gerar dados simulados
def gerar_dados(dias=30):
    np.random.seed(42)
    inicio = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(days=dias)
    dados = []
    for i in range(dias * 24):
        hora = (inicio + timedelta(hours=i)).hour
        ocupacao = 1 if 8 <= hora < 18 else 0
        base = 200 if ocupacao else 100
        variacao = np.random.normal(0, 20)
        carga = max(50, base + variacao + (np.random.uniform(100, 400) if np.random.rand() < 0.05 else 0))
        dados.append([inicio + timedelta(hours=i), round(carga, 1), ocupacao])
    return pd.DataFrame(dados, columns=["timestamp", "carga_W", "ocupacao"])

# detectar desperdícios
def detectar_desperdicio(df):
    df["hora"] = df["timestamp"].dt.hour
    noite = df[(df["hora"] >= 0) & (df["hora"] < 6) & (df["ocupacao"] == 0)]
    desperdicio = noite[noite["carga_W"] > 150]
    return desperdicio

# estimar economia
def estimar_economia(df):
    media_total = df["carga_W"].mean()
    economia = media_total * 0.15  # 15% de economia estimada
    return economia

# plot de gráfico
def gerar_grafico(df):
    df["dia"] = df["timestamp"].dt.date
    consumo_diario = df.groupby("dia")["carga_W"].mean()
    plt.figure(figsize=(10, 4))
    plt.plot(consumo_diario, marker="o")
    plt.title("Consumo Médio Diário (W)")
    plt.xlabel("Dia")
    plt.ylabel("Consumo (W)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("consumo_diario.png")
    print("Gráfico salvo em consumo_diario.png")

# execução
if __name__ == "__main__":
    df = gerar_dados()
    desperdicio = detectar_desperdicio(df)
    economia = estimar_economia(df)

    print(f"Horas com consumo indevido (noite): {len(desperdicio)}")
    print(f"Economia potencial estimada: {economia:.2f} W em média")
    gerar_grafico(df)
