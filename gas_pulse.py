#!/usr/bin/env python3
"""
GasPulse — мониторинг распределения цены газа в mempool и расчет рекомендованных gasPrice.
"""

import os
import time
from datetime import datetime
from web3 import Web3

RPC_URL       = os.getenv("ETH_RPC_URL")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "15"))  # сек

if not RPC_URL:
    print("Ошибка: задайте переменную ETH_RPC_URL с адресом вашего RPC‑узла.")
    exit(1)

w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    print("Ошибка: не удалось подключиться к RPC‑узлу.")
    exit(1)

def fetch_pending_gas_prices():
    """Возвращает список gasPrice из всех незакрытых транзакций."""
    try:
        content = w3.manager.request_blocking("txpool_content", [])
    except Exception as e:
        print(f"[{datetime.now()}] Не удалось получить txpool: {e}")
        return []
    prices = []
    for acc in content.get("pending", {}).values():
        for txobj in (v if isinstance(v, list) else [v] for v in acc.values()):
            for tx in txobj:
                gp = tx.get("gasPrice")
                if gp:
                    prices.append(int(gp))
    return prices

def percentile(sorted_list, pct):
    """Возвращает значение на уровне pct‑го процентиля (0–100)."""
    if not sorted_list:
        return None
    k = (len(sorted_list) - 1) * pct / 100
    f = int(k)
    c = min(f + 1, len(sorted_list) - 1)
    if f == c:
        return sorted_list[int(k)]
    d0 = sorted_list[f] * (c - k)
    d1 = sorted_list[c] * (k - f)
    return int(d0 + d1)

def to_gwei(wei):
    return wei / 10**9

def main():
    print(f"[{datetime.now()}] GasPulse запущен. Интервал опроса {POLL_INTERVAL}s.")
    while True:
        gas_prices = fetch_pending_gas_prices()
        if not gas_prices:
            print(f"[{datetime.now()}] Нет данных mempool.")
        else:
            gas_prices.sort()
            fast   = percentile(gas_prices, 90)  # верхний 10%
            standard = percentile(gas_prices, 50)  # медиана
            slow   = percentile(gas_prices, 25)  # нижний 25%
            print(f"[{datetime.now()}] Рекомендации gasPrice (Gwei):")
            print(f"  • ускоренно (90%):  {to_gwei(fast):.1f}")
            print(f"  • стандартно (50%): {to_gwei(standard):.1f}")
            print(f"  • экономично (25%): {to_gwei(slow):.1f}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
