import pandas as pd
from config import CSV_OUTPUT

def generate_csv(devices):
    """
    Экспортирует список устройств в CSV-файл.
    """
    try:
        df = pd.DataFrame(devices)
        df.to_csv(CSV_OUTPUT, index=False, sep=';')
        print(f"[CSV] CSV-отчёт сохранён: {CSV_OUTPUT}")
    except Exception as e:
        print(f"[CSV] Ошибка сохранения CSV: {e}")