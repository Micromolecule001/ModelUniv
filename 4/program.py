import numpy as np
import matplotlib.pyplot as plt

def analytical_model(lambda_rate, mu, c):
    # Розрахунок середнього часу очікування
    rho = lambda_rate / (c * mu)
    W = 1 / mu + rho / (c * mu - lambda_rate)
    return W

def simulate_checkout(open_time=1440, step_time=20):
    customer_mean = [(7, 480), (4, 600), (10, 1020), (7, 1200), (1, 1380)]
    service_speed = lambda items: 1 + 0.5 * items
    results = []
    queue = 0

    for current_time in range(0, open_time, step_time):
        for mean, start in customer_mean:
            if start <= current_time < start + 120:
                num_customers = np.random.poisson(mean)
                for _ in range(num_customers):
                    items = np.random.binomial(n=10, p=0.5)
                    service_time = service_speed(items)
                    queue += 1
                    results.append(service_time)

    return results, queue

if __name__ == "__main__":
    # Параметри для аналітичної моделі
    lambda_rate = 5  # Інтенсивність надходження покупців
    mu = 1.5         # Швидкість обслуговування
    c = 5            # Кількість кас

    # Виклик аналітичної моделі
    W = analytical_model(lambda_rate, mu, c)
    print(f"Середній час очікування (аналітична модель): {W:.2f} хвилин")

    # Виклик імітаційної моделі
    results, total_customers = simulate_checkout()
    average_service_time = np.mean(results) if results else 0
    print(f"Середній час обслуговування (імітаційна модель): {average_service_time:.2f} хвилин")
    print(f"Загальна кількість обслугованих покупців: {total_customers}")

    # Візуалізація
    plt.hist(results, bins=30, alpha=0.7, color='blue')
    plt.title('Розподіл часу обслуговування')
    plt.xlabel('Час обслуговування (хвилини)')
    plt.ylabel('Кількість покупців')
    plt.show()

