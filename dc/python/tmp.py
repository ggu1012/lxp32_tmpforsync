x = 'a'
y=['b']
z= [x]

tmp = dict()

tmp[x] = y

tmp[x].append('c')

print(tmp['a'])
print(z)

tmp['d'] = 'e'
print(tmp)

for tmp1 in tmp:
    print(tmp1)