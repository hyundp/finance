f = open("name.txt", "rt")
text = f.read()
for i in text:
    print(i, end='')
f.close()
