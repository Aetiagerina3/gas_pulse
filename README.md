# GasPulse

Утилита для мониторинга распределения цен газа (gasPrice) в Ethereum‑мемпуле и расчёта рекомендованных значений для разных приоритетов транзакции.

## Возможности

- Сбор всех `gasPrice` из незавершённых транзакций (`txpool_content`).
- Расчёт 90‑го, 50‑го (медиана) и 25‑го процентилей.
- Вывод рекомендованных значений в Gwei для ускоренных, стандартных и экономичных транзакций.

## Установка

```bash
git clone https://github.com/ваш‑профиль/GasPulse.git
cd GasPulse
pip install -r requirements.txt
