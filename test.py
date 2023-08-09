# # this should not appear in the master branch until committed. 

# def sum_numbers(*args):
#     total = 0
#     for num in args:
#         total += num
#     return total

# result = sum_numbers(1, 2, 3, 4, 5)
# print(result)  # Output: 15

data = {'hair':'black', 'size':'large'}

def dog(**kwargs):
    return kwargs


# d = dog(hair='black', size='large')
d = dog(**data)
print(d)