# # this should not appear in the master branch until committed. 

# def sum_numbers(*args):
#     total = 0
#     for num in args:
#         total += num
#     return total

# result = sum_numbers(1, 2, 3, 4, 5)
# # print(result)  # Output: 15

# data = {'hair':'black', 'size':'large'}

# def dog(**kwargs):
#     return kwargs


# # d = dog(hair='black', size='large')
# d = dog(**data)
# print(d)

# from forex import CurrencyRates

# c = CurrencyRates()
# amount_in_usd = 100  # Enter the amount in USD you want to convert
# converted_amount = c.convert("USD", "MXN", amount_in_usd)
# print(f"{amount_in_usd} USD is equal to {converted_amount} MXN")

x = [1,2,3,4]
y = [n * 2 for n in x]
print(y)