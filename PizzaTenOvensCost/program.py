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

# Variables 
ovenList = [] 
allStats = []
queue = []
queueLimit = 10 # Define queue limit

class Order:
    __idCounter = 1
    __orderList = {}

    def __init__(self, doneTime, rejected, type, price):
        self.id = Order.__idCounter
        Order.__idCounter += 1
        self.rejected = rejected
        self.type = type
        self.price = price
        self.doneTime = doneTime 
        
    def createOrder(time, rejected, type, price, currentTime):
        newOrder = Order(time, rejected, type, price)
        print(f"Order{newOrder.id}:\n",
              f"    Start: {currentTime} \n",
              f"    End: {time} \n",
              f"    IsRejected: {rejected} \n",
              f"    PizzaType: {type} \n",
              f"    Price: {price} \n",
        )
        Order.__orderList[newOrder.id] = newOrder
        return newOrder

    def getOrderByNumber(orderNumber):
        return Order.__orderList[orderNumber] 


class Oven:
    def __init__(self, state, number):
        self.number = number
        self.state = state
        self.activeOrder = None
        self.stats = {}
         
    def printOven(self):
        print(self.number, self.state, self.stats)

    def createOven(state, number):
        newOven = Oven(state, number)
        ovenList.append(newOven)

    def deleteDone(self, currentTime):
        # Only delete if there's an active order and it's done
        if self.activeOrder:
            order = Order.getOrderByNumber(self.activeOrder)
            if currentTime >= order.doneTime:
                self.activeOrder = None  # Delete the order by setting it to None
                self.toggleState()

    def assignOrder(self, orderNumber):
        self.activeOrder = orderNumber

    def updateStats(hour):
        # Update the statistics of ecah oven.

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

            if oven.state == True:
                oven.stats[hour]['chillingTime'] += 5
                oven.stats[hour]['moneySaved'] += 1.666666667
            else: 
                oven.stats[hour]['workingTime'] += 5
                oven.stats[hour]['moneySpent'] += 1.666666667

    def getStats(self):
        # function to get dict with all data 
        statistics = []
        for hour in range(9, 18):
            if hour in self.stats:  # Убедитесь, что статистика для этого часа существует
                stat = self.stats[hour]
                statistics.append({
                    "Id": self.number,
                    "Hour": f"{hour}:00",
                    "wTime": stat["workingTime"],
                    "Orders": stat["ordersCount"],
                    "Spent": math.floor(stat["moneySpent"]),
                    "Saved": math.floor(stat["moneySaved"]),
                })
        return statistics

    def toggleState(self):
        # Toggle the state of the oven between available (True) and busy (False).
        self.state = not self.state  # Toggle state
        print(f"Oven {self.number} is now {'available' if self.state else 'busy'}.")

    def addOrderCount(self, hour):
        # Increment the order count.
        if hour not in self.stats:
            self.stats[hour] = {
            "ordersCount": 0,
            "workingTime": 0,
            "chillingTime": 0,
            "moneySaved": 0,
            "moneySpent": 0,
        }

        self.stats[hour]["ordersCount"] += 1
        print(f"Order count for oven {self.number} is now {self.stats[hour]["ordersCount"]}.")

i = 1
while i <= 10:
    Oven.createOven(True, i)
    i += 1

def main():
    daily_log = []
    currentTime = 9 * 60  # Start at 9:00 AM
    rejectedCounter = 0

    while currentTime < 18 * 60:  # Until 18:00 (6:00 PM)
        currentHour = math.floor(currentTime / 60)
        probability = getOrderProbability(currentTime)
        order = generatePizzaOrder(probability, currentTime)

        if order:
            for oven in ovenList:
                oven.deleteDone(currentTime)

            if len(queue) <= queueLimit:
                oven = assignOrderToOven(order, currentHour)  # Assign order to an available oven
                daily_log.append(order)
            else:
                rejectedCounter += 1
                daily_log.append({"rejected": True, "reason": "Queue full", "price": order["price"]})

        currentTime += 5                # Step forward in 5-minute intervals
        Oven.updateStats(currentHour)   # Update stats for each oven
    
    for oven in ovenList:
        stats = oven.getStats() # get stats from one oven 
        allStats.extend(stats)  # place stats to allStats[]

    print("Rejected orders count at the end of a day: ",rejectedCounter)
        

def getOrderProbability(currentTime):
    # Get the probability based on the time of day.

    if 9 * 60 <= currentTime <= 11 * 60:
        return 0.3
    elif 11 * 60 < currentTime <= 15 * 60:
        return 0.5
    elif 15 * 60 < currentTime <= 18 * 60:
        return 0.7
    else:
        return 0.0  # Outside working hours

def generatePizzaOrder(probability, currentTime):
    if np.random.random() < probability:
        isCustom = np.random.binomial(1, 0.5) == 1

        if isCustom:                             # if individual 
            preparationTime = 15
            price = np.random.uniform(15, 30)
        else:
            preparationTime = 10
            price = np.random.uniform(10, 15)

        time = preparationTime + currentTime

        return Order.createOrder(time, False, isCustom, price, currentTime)

    return None

def assignOrderToOven(order, hour):
    for oven in ovenList:
        if oven.state:                  # If the oven is available
            oven.toggleState()          # Toggle oven state 
            oven.addOrderCount(hour)    # Add order in current hour 
            oven.assignOrder(order.id)  # Directly assign the created order
            print(f"Order{order.id} is going to oven{oven.number}")
            return oven

    return "all ovens are busy"         # If all ovens are busy

main()

df = pd.DataFrame(allStats)
df.set_index(["Hour", "Id"], inplace=True)

pd.set_option("display.max_rows", 1000)
print(df)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

for oven_id in df.index.get_level_values('Id').unique():
    oven_data = df[df.index.get_level_values('Id') == oven_id]
    ax1.bar(oven_data.index.get_level_values('Hour'), oven_data['Spent'], label=f'Oven {oven_id}', alpha=0.4)
    ax2.bar(oven_data.index.get_level_values('Hour'), oven_data['Saved'], label=f'Oven {oven_id}', alpha=0.1)
    ax3.bar(oven_data.index.get_level_values('Hour'), oven_data['wTime'], label=f'Oven {oven_id}', alpha=0.4)
    ax4.bar(oven_data.index.get_level_values('Hour'), oven_data['Orders'], label=f'Oven {oven_id}', alpha=0.4)
    
ax1.set_xlabel("Hour")
ax1.set_ylabel("Spent Money")
ax1.set_title("Spent Money of using ovens")

ax2.set_xlabel("Hour")
ax2.set_ylabel("Saved Money")
ax2.set_title("Saved Money of not using ovens")

ax3.set_xlabel("Hour")
ax3.set_ylabel("Working Time")
ax3.set_title("Working Time per Hour for Each Oven")

ax4.set_xlabel("Hour")
ax4.set_ylabel("Orders Done")
ax4.set_title("Orders Done by each oven")

ax1.legend(title='Ovens', loc='upper left', bbox_to_anchor=(1, 1))
plt.tight_layout()
plt.show()
