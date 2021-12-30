import numpy as np

class Token(object):
    def __init__(self, name) -> None:
        super().__init__()

        self.name = name
        self.compiled = False

        # Array of nx2 [qty,val] -> qty: purchased amount of the token | val: purchase price
        self.purchases = np.empty((0,2), float)
        self.sales = np.empty((0,2), float)

        self.purchases_sold = np.empty((0,2), float)
        self.purchases_held = np.empty((0,2), float)
        
        # Parameters
        self.min_token_usd = 1.0

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
        Returns the amount of the held token, which was bought but not yet sold
        '''
        return self.purchases[:,0].sum() - self.sales[:,0].sum()

    def get_total_sales(self):
        '''
        Returns total sales value
        '''
        return (self.sales[:,0]*self.sales[:,1]).sum()

    def get_total_purchases(self):
        '''
        Returns total purchases value
        '''
        return (self.purchases[:,0]*self.purchases[:,1]).sum()

    def get_total_purchases_sold(self):
        '''
        Returns total sold purchases
        '''
        return (self.purchases_sold[:,0]*self.purchases_sold[:,1]).sum()
    
    def get_earns(self):
        '''
        Returns 
        '''
        if not(self.compiled):
            print("Compile token is needed before calculate")
            return 0
        # DEBUG
        # print("get_total_sales: "+str(self.get_total_sales()))
        # print("get_total_purchases_sold: "+str(self.get_total_purchases_sold()))
        return self.get_total_sales()-self.get_total_purchases_sold()

    def get_null_sale_price(self):
        '''
        Returns the sale price for which the gains are zero (that is, there are no losses)
        '''
        if not(self.compiled):
            print("Compile token is needed before calculate")
            return 0
            
        return 0

    def get_current_earns_status(self):
        '''
        Returns earnings if the amount of the token withheld is sold with the current market price
        '''
        if not(self.compiled):
            print("Compile token is needed before calculate")
            return 0
            
        return 0

    def get_current_token_price(self):
        '''
        Returns the current price of the token
        '''
        if not(self.compiled):
            print("Compile token is needed before calculate")
            return 0
            
        return 0
        
    # Con el de hold:
        # Buscar precio actual y ver si estas en ganancia o perdida
        # Calcular precio de venta para no tener perdidas

    def compile(self):

        if self.compiled:
            print("Token already compiled")
            return False

        self._split_purchases()

        self.compiled = True
        return True

    def _split_purchases(self):
        sorted_purchases = self.purchases[np.argsort(self.purchases[:, 1])]
        # sorted_sales = self.sales[np.argsort(self.sales[:, 1])]
        qty_sold = self.sales[:,0].sum()    # Amount sold of token 

        purchased_qty_acum = 0
        token_held_found = False

        for transaction in sorted_purchases:
            if token_held_found:
                self.purchases_held = np.append(self.purchases_held, np.array([transaction]), axis=0) # The total amount of the token in this transaction  was withheld 
            else:
                
                temp_purchased_qty_acum = purchased_qty_acum + transaction[0]
                if temp_purchased_qty_acum <= qty_sold:
                    purchased_qty_acum = temp_purchased_qty_acum
                    self.purchases_sold = np.append(self.purchases_sold, np.array([transaction]), axis=0)   # The total amount of the token in this transaction  was sold 
                else:
                    token_held_found = True

                    held_qty = temp_purchased_qty_acum - qty_sold        # Amount of token held in this transaction
                    if (held_qty*transaction[1])>self.min_token_usd:     # Avoid append very small values (less than USD(min_token_usd))
                        self.purchases_held = np.append(self.purchases_held, np.array([[held_qty,transaction[1]]]), axis=0)

                    sold_qty = transaction[0] - held_qty            # Amount of token sold in this transaction
                    if (sold_qty*transaction[1])>self.min_token_usd:     # Avoid append very small values (less than USD(min_token_usd))
                        self.purchases_sold = np.append(self.purchases_sold, np.array([[sold_qty,transaction[1]]]), axis=0)

        # DEBUG
        # print("self.sales:")
        # print(self.sales)
        # print("self.purchases:")
        # print(self.purchases)
        # print("self.purchases_held:")
        # print(self.purchases_held)
        # print("self.purchases_held:")
        # print(self.purchases_held)
