import numpy as np

class Token(object):
    def __init__(self, name) -> None:
        super().__init__()

        self.name = name

        # Array of nx2 [qty,val] -> qty: purchased amount of the token | val: purchase price
        self.purchases = np.empty((0,2), float)
        self.sales = np.empty((0,2), float)
    
    def buy(self, qty, val):
        '''
        Token purchase operation
        qty: token amount
        val: token price
        '''
        self.purchases = np.append(self.purchases, np.array([[qty, val]]), axis=0)

    def sell(self, qty, val):
        '''
        Token sale operation
        qty: token amount
        val: token price
        '''
        self.sales = np.append(self.sales, np.array([[qty, val]]), axis=0)

    def trade(self,side,qty,val):
        '''
        Operation with the token
        side: could be 'buy' or 'sell' (str)
        qty: token amount
        val: token price
        '''
        if side.lower() == "buy":
            self.buy(qty,val)
        elif side.lower() == "sell":
            self.sell(qty,val)
        else:
            print("Warning: Cannot trade unknown operation: "+str(side))
    
    def get_final_qty(self):
        '''
        Returns the amount of the holded token, which was bought but not yet sold
        '''
        return self.purchases[:,0].sum() - self.sales[:,0].sum()



