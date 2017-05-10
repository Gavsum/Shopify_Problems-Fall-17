# Shopify Coding Problems Fall 2017
### Problem 1: Back End Dev 
* Problem Brief:
    * Shopify store makes treats and sells local
    * Cant keep up with orders coming in, Needs solution
    * Limited Num of Cookies remaining
    * Current existing orders are logged
    * Merchant wants to know which orders will & wont be filled according to the requirements below..
    
    * Requirements:
        * Read all orders from paginated JSON (url provided)
        * Any order **without** cookies can be fulfilled
        * prioritize fulfilling orders with the highest amount of cookies
        * If orders have the same amount of cookies, prioritize the order with the lowest ID
        * If an order has an amount of cookies larger than the remaining cookies, skip the order.
        
* Todo:
    * Change output from print statement to outfile
    * Change functions to operate under more general inputs
        * resource could be food item other than Cookie, can be specified with cmd line arg
        * Specify fill or sort rules from cmd line arg

Solution in cookies.py

### Problem 2: Data Analysis
* Problem Brief:
    * 100 Sneaker shops selling shoes online
    * Want to calc an Average order value (AOV).
    * Tried to calc directly but result was misleading
    * How can data be evaluated more accurately with a similar metric?
    
Solution in jupyter notebook
    
### Problem 3: Data Engineering
* To be added