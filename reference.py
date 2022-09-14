# will use flask_social_media_backend as reference to create my flask backend..
# copy content and paste it, once I am confident enough, try to do some routes/models on my own..
# created two separate blueprints, one for authentication/user db, the other for the user's ability to create a portfolio....



# LEAVE PORTFOLIO FOLDER FOR LATER, FINISH THE AUTH FIRST

# example
# user creates an acct
    # post create user
# user has no funds and no stock ownership
# user searches for stocks
# user buys a selected amount of stocks, depending on their portfolio cash funds
# user can buy other stocks they search for, as long as the value is not greater than their portfolio cash funds
# user has multiple ownership of different stocks
# user decides to sell some stocks completely, removing his ownership of those stocks, receiving their value in cash
# user decides to sell some stock ownership for a certain company, but not all of it, retaining some shares but reducing their stake

# if this is all user can do, it would be:
# 1. add funds to                       portfolio cash funds +
# 2. remove funds from                  portfolio cash funds -
# 3. remove portfolio cash funds    ==  add stock funds into a set amount of shares of a set stock ticker
# 4. add portfolio cash funds       ==  remove stock funds from a set amount of shares of a set stock ticker
# THIS IS WHAT THE USER CAN DO ^^^

# besides what the user can do, in order to add the right funds to/from stock portfolio:
# need to get the stock's current price when the user buys a set amount of shares
# need to get the stock's current price when the user sells a set amount of shares
# need to get the user's amount of shares to calculate the investment/divestment of portfolio stock funds
# need ticker, current price, amount of shares, date for every transaction

# so when a user sells shares of a stock, they will receive the num of shares * current price at the moment they sell those shares back into their portfolio cash funds