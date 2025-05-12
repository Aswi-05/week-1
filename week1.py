import time
import threading
import sqlite3
import logging
from datetime import datetime

# === SETUP LOGGING ===
logging.basicConfig(filename='operation_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# === TIMER FUNCTION ===
def countdown_timer(duration):
    print(f"\nTimer started for {duration} seconds.")
    while duration:
        mins, secs = divmod(duration, 60)
        print(f'Time left: {mins:02d}:{secs:02d}', end='\r')
        time.sleep(1)
        duration -= 1
    print("\n⏰ Timer finished!")
    logging.info("Timer completed.")

# === CALCULATOR FUNCTION ===
def perform_operation():
    try:
        num1 = float(input("\nEnter first number: "))
        op = input("Enter operation (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            result = num1 / num2
        else:
            raise ValueError("Invalid operation.")

        print(f"Result: {result}")
        logging.info(f"Calculated: {num1} {op} {num2} = {result}")

        return (num1, op, num2, result)
    except Exception as e:
        print(f"❌ Error: {e}")
        logging.error(f"Calculation error: {e}")

# === OPTIONAL: HISTORY WITH SQLITE ===
def save_to_db(entry):
    conn = sqlite3.connect('calculator_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num1 REAL,
            operation TEXT,
            num2 REAL,
            result REAL,
            timestamp TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO history (num1, operation, num2, result, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (entry[0], entry[1], entry[2], entry[3], datetime.now().isoformat()))
    conn.commit()
    conn.close()

# === MAIN MENU ===
def main():
    print("==== Countdown Timer & Calculator App ====")

    while True:
        print("\nChoose an option:")
        print("1. Start Countdown Timer")
        print("2. Use Calculator")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            try:
                unit = input("Enter unit (s for seconds / m for minutes): ").lower()
                duration = int(input("Enter duration: "))
                seconds = duration * 60 if unit == 'm' else duration
                t = threading.Thread(target=countdown_timer, args=(seconds,))
                t.start()
                t.join()
            except ValueError:
                print("❌ Invalid input. Please enter a valid number.")
        elif choice == '2':
            entry = perform_operation()
            if entry:
                save_option = input("Save to history? (y/n): ").lower()
                if save_option == 'y':
                    save_to_db(entry)
        elif choice == '3':
            print("Exiting application. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# === RUN APP ===
main()
