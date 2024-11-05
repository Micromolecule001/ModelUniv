"""
    В піцерії є 10 печей для виготовлення піци. Черга до них одна. В черзі
    може знаходитися не більше 10 замовлень, інакше замовлення не
    приймається. Утримання 1 печі ввімкненою коштує закладу 20 умовних
    одиниць за годину. Власника піцерії цікавить, скільки печей потрібно
    вмикати в різні періоди часу, щоб отримати максимальний виторг.
    Швидкість виготовлення однією піччю стандартної піци з меню – 10 хвилин,
    індивідуальне замовлення – 15 хвилин. Вартість стандартної піци від 10 до 15 умовних
    одиниць, вартість індивідуального замовлення від 15 до 30 умовних одиниць, рівномірний
    закон розподілу. Крок зміни модельного часу – 5 хвилин. Тривалість моделювання –
    1 доба. Ймовірність того, що протягом 5 хвилин надійде замовлення залежить від часу
    дня: з 09:00 до 11:00 – 0,3; з 10:00 до 15:00 – 0,5; з 15:00 до 20:00 – 0,9; з 20:00 до 22:00 –
    0,7. «Індивідуальність» замовлення – випадкова величина з розподілом Бернуллі
    (дивитися біноміальний розподіл для однократного випробовування).
"""

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Oven:
    def __init__(self, state, number):
        self.number = number
        self.state = state
        self.activeOrder = {}
        self.stats = {
            9: {
                "ordersCount": 0,
                "workingTime": 0,
                "chillingTime": 0,
                "moneySaved": 0,
                "moneySpent": 0,
            }
        }
         
    def createOven(state, number):
        newOven = Oven(state, number)
        ovenList.append(newOven)

    def printOven(self):
        print(self.number, self.state, self.stats)

    def updateStats(hour):
        """Update the statistics of ecah oven."""

        for oven in ovenList:
            if hour not in oven.stats:
                # Initialize the stats for the new hour
                oven.stats[hour] = {
                    "ordersCount": 0,
                    "workingTime": 0,
                    "chillingTime": 0,
                    "moneySaved": 0,
                    "moneySpent": 0,
                }

            if oven.state == False:
                oven.stats[hour]['chillingTime'] += 5
                oven.stats[hour]['moneySaved'] += 1.666666667
            else: 
                oven.stats[hour]['workingTime'] += 5
                oven.stats[hour]['moneySpent'] += 1.666666667

    def getStats(self):
        """Return and reset the hourly stats for the oven."""
        statistic = self.stats
        start = 9
        end = 18

        while start < end:
            hour = statistic[start]
            print(f"Statistic of {self.number} in {start}:00",
                  f"\nWorking Time: {hour['workingTime']}", 
                  f"\nMoney Spent: {hour['moneySpent']}",
                  f"\nOrders Count: {hour['ordersCount']}",
                  f"\nMoney Saved: {math.floor(hour['moneySaved'])}",
            )
            start += 1

        print("\n")

    def toggleState(self):
        """Toggle the state of the oven between available (True) and busy (False)."""
        self.state = not self.state  # Toggle state
        print(f"Oven {self.number} is now {'available' if self.state else 'busy'}.")

    def addOrderCount(self):
        """Increment the order count."""
        self.stats["ordersCount"] += 1
        print(f"Order count for oven {self.number} is now {self.stats['orderCount']}.")
        

ovenList = [] 
all_statistics = []
queue = []
queueLimit = 10  # Define queue limit

# generate 10 ovens
i = 1
while i <= 10:
    Oven.createOven(True, i)
    i += 1

def simulateOneDay():
    daily_log = []
    current_time = 9 * 60  # Start at 9:00 AM

    while current_time < 18 * 60:  # Until 18:00 (6:00 PM)
        current_time += 5  # Step forward in 5-minute intervals
        current_hour = math.floor(current_time / 60)
        
        probability = getOrderProbability(current_time)
        order = generatePizzaOrder(probability)

        if order:
            checkQueue(current_time)
            if len(queue) <= queueLimit:
                queue.append({"time": current_time, **order})
                oven = assignOrderToOven(order, current_hour)  # Assign order to an available oven
                daily_log.append(order)
            else:
                daily_log.append({"rejected": True, "reason": "Queue full", "price": order["price"]})

        Oven.updateStats(current_hour)

    for oven in ovenList:
        # oven.getStats()
        pass


    # Store daily statistics
    all_statistics.append(daily_log)
    return daily_log

def getOrderProbability(current_time):
    # Get the probability based on the time of day.

    if 9 * 60 <= current_time <= 11 * 60:
        return 0.3
    elif 11 * 60 < current_time <= 15 * 60:
        return 0.5
    elif 15 * 60 < current_time <= 18 * 60:
        return 0.7
    else:
        return 0.0  # Outside working hours

def checkQueue(current_time):
    global queue
    completed_orders = []

    # Check each order in the queue if it's complete
    for order in queue:
        end_time = order["time"] + order["preparation_time"]
        if current_time >= end_time:
            completed_orders.append(order)

    for order in completed_orders:
        queue.remove(order)

def generatePizzaOrder(probability):
    if np.random.random() < probability:
        is_custom = np.random.binomial(1, 0.5) == 1

        if is_custom:
            preparation_time = 15
            price = np.random.uniform(15, 30)
        else:
            preparation_time = 10
            price = np.random.uniform(10, 15)
        
        return {
            "rejected": False,
            "is_custom": is_custom,
            "preparation_time": preparation_time,
            "price": price
        }

    return None

def assignOrderToOven(order, hour):
    # Assign an order to an oven (choose the first available one).
    for oven in ovenList:
        if oven.state:  # If the oven is available
            oven.toggleState()
            oven.addOrderCount()
            return oven

    return "all ovens are busy"  # If all ovens are busy

# Main simulation loop
def main():
    for day in range(1):
        print(f"Simulating Day {day+1}")
        simulateOneDay()

main()

