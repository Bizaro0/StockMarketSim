from tkinter import Menu
from finances import Finances
import yfinance as yf
from datetime import datetime
import streamlit as st
import json
import time

finance = Finances()


isPicked =True
isValue = False

def buyStock():
    while True:
        inp = input("Enter Ticker Symbol: ").upper()
        ticker = yf.Ticker(inp)
        try:
            data = ticker.history(period="1d", interval="1m")
            if data.empty:
                raise ValueError("Empty data")
        except:
            print("Invalid ticker symbol or network error. Please try again.\n")
            continue
       
        info = ticker.fast_info
        day_high = round(data["High"].max(), 2)
        day_low = round(data["Low"].min(), 2)
        current_price = round(info['lastPrice'], 2)
        currentDate = datetime.now()
        timeStamp = currentDate.strftime("%Y-%m-%d %H:%M:%S") 
      
        print("Day's highest:", day_high)
        print("Day's lowest:", day_low)
        print("Current:", current_price)
        print("Current Deposit:", finance.getCash())
       
      
        inp2 = input("Do you wish to proceed? (Y/N): ").upper()
        if inp2 == "Y":
            try:
                amt = int(input("Amount you wish to buy: "))
                company_name = ticker.info.get('longName', "Unknown Company")
                total_cost = current_price * amt
                cash = finance.getCash()

                if total_cost > cash:
                    print("Insufficient funds.")
                    continue

                finance.setCash(cash - total_cost)

                print("After Purchase:", finance.getCash())
                print(f"Order Confirmation:\n{company_name}\nAmount: {amt}\nDate: {timeStamp}")
                
                finance.addToPortfolio(inp, company_name, amt, current_price, timeStamp)
                
                again = input("Would you like to buy another stock? (Y/N): ").upper()
                if again != 'Y':
                    print("You are now leaving the market!")
                    isPicked = True
                    menu()
                    break
                
            except ValueError:
                isPicked = True
                global isValue
                isValue = True
                time.sleep(5)
                menu()

def sellStock():
    prtfo = finance.getPortfolio()
    print(f"Portfolio {prtfo}")
    while True:
        ticker_sell = input("Enter the ticker of the stock you want to sell: ").upper()

        if ticker_sell in prtfo:
            owned_stock = prtfo[ticker_sell]  
            try:
                amount = int(input("Amount to sell : "))
                if amount > owned_stock['amount']:
                    print("You do not own that amount of shares.")
                    continue
                else:
                    ticker = yf.Ticker(ticker_sell)
                    current_price = round(ticker.fast_info['lastPrice'], 2)
                    total_val = current_price * amount
                    new_amt = owned_stock['amount'] - amount
                    owned_stock['amount'] = new_amt

                    new_csh = finance.getCash() + total_val
                    finance.setCash(new_csh)

                    print(f"Sold {amount} shares of {owned_stock['company_name']}")
                    print(f"New Cash Balance : {finance.getCash()}")

                    if owned_stock['amount'] == 0:
                        del prtfo[ticker_sell]
                    
                    break 

            except ValueError:
                print("Please enter a valid number of shares.")
        else: 
            print(f"You do not own shares of {ticker_sell}. Try again.")


        

                    


def showTransactions():
    try:
        with open("portfolio.json", "r") as file:
            try:
                trans = json.load(file)
                for i, entry in enumerate(trans, 1):
                    if not entry:  # Skip empty entries
                        print(f"Skipping empty entry at transaction {i}")
                        continue
                    
                    if isinstance(entry, dict):
                      
                        if 'ticker' in entry: 
                            data = entry
                            ticker = data['ticker']
                        elif len(entry) == 1:
                            ticker, data = list(entry.items())[0]
                        else:
                            print(f"Skipping invalid data for transaction {i}")
                            continue
                    else:
                        print(f"Skipping invalid data for transaction {i}")
                        continue
                    
               
                    if isinstance(data, dict) and 'ticker' in data:
                        print(f"\nTransaction {i}:")
                        print(f"  Ticker        : {ticker}")
                        print(f"  Company Name  : {data['company_name']}")
                        print(f"  Amount        : {data['amount']}")
                        print(f"  Price per Share: ${data['price']}")
                        print(f"  Date & Time   : {data['date']}")
                    else:
                        print(f"Skipping invalid data for transaction {i}")
                        
            except json.JSONDecodeError: 
                print("Error: The file is empty or has invalid JSON content.")
                trans = []  
    except FileNotFoundError:
        print("Error: portfolio.json not found.")
        trans = []

            

def menu():
    global isPicked
    global isValue
    while isPicked:
        if(isValue):
            num = input("Please select a number \n1. See Portfolio \n2. Buy Stock \n3. Sell Stock \n4. View Transaction History: \n ")
        else:
            num = input("Enter your choice: ")
        isValue = False
        match num:
            case "1":
                finance.getPortfolio()
                isPicked = False
            case "2":
                buyStock()
                isPicked = False
            case "3":
                sellStock()
                isPicked = False
            case "4":
                showTransactions()
                isPicked = False
            case _:
                print("Invalid Choice\n")


st.title("📈 Stock Market Simulator")

print("Welcome to the Stock Market Sim!")
print("1. View Portfolio ")
print("2. Buy Stock ")
print("3. Sell Stock ")
print("4. View Transaction History")
menu()
