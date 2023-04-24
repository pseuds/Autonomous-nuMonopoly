f = open('names.txt', 'r+')
s = f.read()
print(s)
s_ls = s.split('\n')
print(s_ls)
sorted_namels = sorted(s_ls)

for name in sorted_namels:
    f.write(name)
    f.write('\n')