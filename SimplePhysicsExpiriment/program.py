import numpy as np
import matplotlib.pyplot as plt

# Константи
g = 9.81  # прискорення вільного падіння, м/с^2
rho_s = 11.3 * 10**3  # щільність свинцю, кг/м^3
r = 0.01  # радіус кульки, м
V = (4/3) * np.pi * r**3  # об'єм кульки, м^3
m = rho_s * V  # маса кульки, кг

# Функція для обчислення прискорення
def model(v, rho_m, mu_m):
    k = 6 * np.pi * mu_m * r  # коефіцієнт опору (формула Стокса)
    F_g = m * g  # сила тяжіння
    F_a = rho_m * V * g  # Архімедова сила
    F_op = -k * v  # сила опору
    F = F_g - F_a + F_op  # сумарна сила
    a = F / m  # прискорення
    return a

# Початкові параметри для моделювання
v0_values = [0, 1, 5]  # початкові швидкості, м/с
rho_m_values = [0.8 * 10**3, 0.92 * 10**3, 1.1 * 10**3]  # різні щільності рідини
mu_m_values = [0.5, 0.95, 1.5]  # різні значення в'язкості рідини

# Часова шкала
t = np.linspace(0, 10, 1000)  # час, сек

# Підготовка для побудови 9 графіків
fig, axs = plt.subplots(3, 3, figsize=(15, 10))
fig.suptitle('Вплив початкової швидкості, щільності та в’язкості на рух кульки', fontsize=16)

# Моделюємо та будуємо графіки
for i, v0 in enumerate(v0_values):
    for j, (rho_m, mu_m) in enumerate(zip(rho_m_values, mu_m_values)):
        v = np.zeros_like(t)
        v[0] = v0  # задаємо початкову швидкість
        
        # Розрахунок швидкості на кожному кроці часу
        for k in range(1, len(t)):
            dt = t[k] - t[k-1]
            v[k] = v[k-1] + model(v[k-1], rho_m, mu_m) * dt

        # Відображення графіка
        axs[i, j].plot(t, v)
        axs[i, j].set_title(f'v0={v0} м/с, ρ={rho_m/1000:.2f} г/см³, μ={mu_m}')
        axs[i, j].set_xlabel('Час (с)')
        axs[i, j].set_ylabel('Швидкість (м/с)')
        axs[i, j].grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

