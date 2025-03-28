import itertools

# Danh sách ban đầu
lst = [1, 2, 3]

# Lấy tất cả hoán vị của danh sách
hoan_vi = list(itertools.permutations(lst))

# In ra tất cả hoán vị
print("Các hoán vị của danh sách [1, 2, 3] là:")
for hv in hoan_vi:
    print(hv)