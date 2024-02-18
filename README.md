# OVERVIEW

This application is a Flask backend API based on a frontend stock buying and selling web app that allows users to buy and sell stocks among other things. It is designed as an API that allows for CRUD capabilities for users, as well as CRUD abilities for any user's stock portfolio transactions. 

There are 2 main blueprints for this API, the auth and portfolio blueprints. The auth blueprint contains an http authorization module, a models module, and a routes module. The http authorization file contains the general user authentication capabilities as well as token generation. The models module contains the User model. The routes module contains multiple routes to perform CRUD for a given user. 

The portfolio blueprint contains a models module and a routes module. The models module contains both the Stock and the Transaction models. The Transaction model accounts for any user transactions involving some cash in or cash out movement. The Stock model accounts for a given stock's information based on the user's transaction movements. So, a transaction could involve buying more shares of a stock the user already owns, which would create a new transaction and update the Stock model to reflect the new updates made to that specific user stock. 



# SAMPLE USER FUNCTIONALITY

- user creates an acct
    - post create user
- user has no funds and no stock ownership
- user searches for stocks
- user buys a selected amount of stocks, depending on their portfolio cash funds
- user can buy other stocks they search for, as long as the value is not greater than their - portfolio cash funds
- user has multiple ownership of different stocks
- user decides to sell some stocks completely, removing his ownership of those stocks, receiving - their value in cash
- user decides to sell some stock ownership for a certain company, but not all of it, retaining - some shares but reducing their stake

if this is all user can do, it would be:
1. add funds to                       portfolio cash funds +
2. remove funds from                  portfolio cash funds -
3. remove portfolio cash funds    ==  add stock funds into a set amount of shares of a set stock ticker
4. add portfolio cash funds       ==  remove stock funds from a set amount of shares of a set stock ticker

besides what the user can do, in order to add the right funds to/from stock portfolio:
need to get the stock's current price when the user buys a set amount of shares
need to get the stock's current price when the user sells a set amount of shares
need to get the user's amount of shares to calculate the investment/divestment of portfolio stock funds
need ticker, current price, amount of shares, date for every transaction

so when a user sells shares of a stock, they will receive the num of shares * current price at the moment they sell those shares back into their portfolio cash funds