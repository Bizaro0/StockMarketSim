import json
class Finances:

    def __init__(self):
        self.cash = 100000
        self.portfolio = {}
        self.transaction_history = []
      

    def getCash(self):
            return self.cash
    
    def getPortfolio(self):
        try:
            with open("portfolio.json", "r") as f:
                self.portfolio = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.portfolio = []
        return self.portfolio
        
    def setCash(self, new_Value):
          self.cash = new_Value

    def addToPortfolio(self, inp, company_name, amt, current_price, timeStamp):
        portfolio_entry = {
       
            "ticker": inp,
            "company_name": company_name,
            "amount": amt,
            "price": current_price,
            "date": timeStamp
            
    
    }


        
        try:
              with open("portfolio.json","r") as f:
                    portfolio = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
              portfolio = []
        
        portfolio.append(portfolio_entry)
    
        with open("portfolio.json", "w") as f:
                json.dump(portfolio, f, indent=4)

        

        
    
    
    

        