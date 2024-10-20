import numpy as np
import matplotlib.pyplot as plt

def simulate_checkout(open_time=1440, step_time=20):
    # Налаштування параметрів
    customer_mean = [
        (7, 480),   # 08:00 - 10:00
        (4, 600),   # 10:00 - 17:00
        (10, 1020), # 17:00 - 20:00
        (7, 1200),  # 20:00 - 23:00
        (1, 1380)   # 23:00 - 08:00
    ]
    service_speed = lambda items: 1 + 0.5 * items  # Лінійна залежність швидкості обслуговування
    results = []  # Для збереження загального часу обслуговування на кожному кроці
    queue = 0
    total_service_time = 0

    for current_time in range(0, open_time, step_time):
        # Визначення середнього значення покупців на поточний час
        for mean, start in customer_mean:
            if current_time >= start and current_time < start + 120:  # 120 хвилин для кожного періоду
                num_customers = np.random.poisson(mean)  # Кількість покупців
                for _ in range(num_customers):
                    items = np.random.binomial(n=10, p=0.5)  # Кількість товару
                    service_time = service_speed(items)  # Час обслуговування
                    queue += 1
                    total_service_time += service_time
                    results.append(total_service_time)  # Додаємо загальний час обслуговування

    return results, queue, total_service_time

def plot_results(results, queue, total_service_time):
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(results)), results, label='Загальний час обслуговування (хвилини)')
    plt.title('Час обслуговування клієнтів у магазині')
    plt.xlabel('Час (кроки)')
    plt.ylabel('Час обслуговування (хвилини)')
    plt.axhline(y=total_service_time, color='r', linestyle='--', label='Сумарний час обслуговування')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    results, queue, total_service_time = simulate_checkout()
    print("Results: ", results, queue, total_service_time)
    plot_results(results, queue, total_service_time)

