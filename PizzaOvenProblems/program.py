import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

queue = []  # Use a list to manage the queue of orders
queueLimit = 5

def SimulateOneDay():
    dayLog = []  # Initialize a new log for each day
    currentTime = 9 * 60  # Start at 9:00 AM

    while currentTime < 18 * 60:  # Until 18:00 (6:00 PM)
        currentTime += 5  # Step forward in 5-minute intervals
        
        # Determine the probability for order generation based on time of day
        if currentTime >= 9 * 60 and currentTime <= 11 * 60:
            probability = 0.3
        elif currentTime > 11 * 60 and currentTime <= 15 * 60:
            probability = 0.5
        elif currentTime > 15 * 60 and currentTime <= 18 * 60:
            probability = 0.7
        else:
            print('not working hours ')

        order = generatePizzaOrder(probability)
        
        # Check if an order was generated and the queue is not full
        if order:
            # Update the queue and check if it's full
            checkQueue(currentTime)
            if len(queue) < queueLimit:
                queue.append({"time": currentTime, **order})  # Add the order with its time
                dayLog.append(order)  # Log the order
            else:
                # Log that order is rejected due to full queue
                dayLog.append({"rejected": True, "reason": "Queue full", "price": order["price"]})

    return dayLog

def generatePizzaOrder(probability):
    if np.random.random() < probability:
        is_custom = np.random.binomial(1, 0.5) == 1

        if is_custom:
            preparation_time = 15
            price = np.random.uniform(15, 20)
        else:
            preparation_time = 10
            price = np.random.uniform(10, 15)
        
        return {
            "rejected": False,
            "is_custom": is_custom,
            "preparation_time": preparation_time,
            "price": price
        }

def checkQueue(currentTime):
    global queue  # Access the global queue
    completed_orders = []

    if currentTime >= 1075: 
        queue = []

    # Iterate over the queue to check if each order is ready
    for order in queue:
        end_time = order["time"] + order["preparation_time"]  # Calculate the end time of the order
        if currentTime >= end_time:
            completed_orders.append(order)  # Mark order as complete

    # Remove completed orders from the queue
    for order in completed_orders:

#       print('\n\n Start order time: ', order["time"],
#             '\n\n Preparation time: ', order["preparation_time"], 
#             '\n\n Current day time: ', currentTime,
#             '\n\n Queue before: \n', queue)
        queue.remove(order)
#       print('\n Queue after: ', queue)

def sumAmount(logs):
    priceSum = 0
    orderCount = 0
    rejectedCount = 0
    rejectedMoney = 0

    for log in logs:
        if not log["rejected"]:
            priceSum += log["price"]
            orderCount += 1
        else:
            rejectedCount += 1
            rejectedMoney += log["price"] 

    return  {
        "sum": priceSum,
        "orderCount": orderCount,
        "rejectedCount": rejectedCount,
        "rejectedSum": rejectedMoney,
    }

def main():
    averageMoney = {}
    averageOrders = {}
    averageRejected = {}
    averageRejectedMoney = {}

    for i in range(31):  # Simulate for 5 days
        dayLog = SimulateOneDay()
        dayStats = sumAmount(dayLog)
#       print(f'\n\n DayLog {i}:  {dayLog}')
#       print('Stats: ', dayStats)

        averageMoney[i] = dayStats['sum']
        averageOrders[i] = dayStats['orderCount']
        averageRejected[i] = dayStats['rejectedCount']
        averageRejectedMoney[i] = dayStats['rejectedSum']

#       print('\n\n Money: ', averageMoney,
#             '\n\n Orders: ', averageOrders, 
#             '\n\n Rejects: ', averageRejected,
#             '\n\n RejectsSum: ', averageRejectedMoney,
#       )

        data = {
            "Money": averageMoney,
            "Orders": averageOrders,
            "Rejects": averageRejected,
            "RejectsSum": averageRejectedMoney
        }

    df = pd.DataFrame(data)
    print(df.to_string())

    # Plotting
    plt.figure(figsize=(14, 8))

    # Plot each column
    plt.subplot(2, 2, 1)
    plt.plot(df["Money"], marker='o', color='blue', label='Money')
    plt.title("Total Money per Day")
    plt.xlabel("Day")
    plt.ylabel("Money ($)")
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(df["Orders"], marker='o', color='green', label='Orders')
    plt.title("Total Orders per Day")
    plt.xlabel("Day")
    plt.ylabel("Orders")
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(df["Rejects"], marker='o', color='red', label='Rejected Orders')
    plt.title("Rejected Orders per Day")
    plt.xlabel("Day")
    plt.ylabel("Rejected Orders")
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(df["RejectsSum"], marker='o', color='purple', label='Rejected Money')
    plt.title("Money Lost from Rejections per Day")
    plt.xlabel("Day")
    plt.ylabel("Rejected Money ($)")
    plt.legend()

    plt.tight_layout()
    plt.show()

main()

