from app.app import Order, DataAboutOrder, Supply

def calculate_order_fulfillment(v_zt, v_ot):
    """
    Расчёт объёма выполнения заказа (Vвз).
    """
    if v_zt <= 0:
        return 0  # Если заказанный объём некорректен

    v_vz = 1 - (v_zt - v_ot) / v_zt
    return max(0, min(1, v_vz))  # Ограничение диапазона [0, 1]

def assign_order_fulfillment_rank(v_vz):
    """
    Назначение ранга на основе Vвз.
    """
    if v_vz >= 0.8:
        return 'A', 2
    elif 0.5 <= v_vz <= 0.79:
        return 'B', 1
    else:
        return 'C', 0

def process_orders():
    """
    Основной процесс обработки заказов и выполнения расчётов.
    """
    results = []

    # Загружаем данные из базы
    orders = Order.query.all()
    data_about_orders = {data.order_id: data for data in DataAboutOrder.query.all()}
    supplies = {supply.data_about_order_id: supply for supply in Supply.query.all()}

    for order in orders:
        # Ищем данные о заказе
        data = data_about_orders.get(order.id)
        if not data:
            print(f"Данные о заказе отсутствуют для Order ID {order.id}")
            continue

        # Ищем данные о поставке
        supply = supplies.get(data.id)
        if not supply:
            print(f"Данные о поставке отсутствуют для DataAboutOrder ID {data.id}")
            continue

        # Расчёты
        v_zt = data.amount  # Планируемый объём
        v_ot = supply.amount_receiving_actual  # Реальный объём

        v_vz = calculate_order_fulfillment(v_zt, v_ot)
        rank, score = assign_order_fulfillment_rank(v_vz)

        # Сохраняем результат
        results.append({
            "order_id": order.id,
            "order_name": order.name,
            "v_zt": v_zt,
            "v_ot": v_ot,
            "v_vz": v_vz,
            "rank": rank,
            "score": score
        })

        print(f"Order ID: {order.id}, Vвз: {v_vz:.2f}, Rank: {rank}, Score: {score}")

    return results

# Запускаем процесс
if __name__ == "__main__":
    results = process_orders()

    # Можно сохранить результаты в БД или вывести в таблицу
    for result in results:
        print(result)
