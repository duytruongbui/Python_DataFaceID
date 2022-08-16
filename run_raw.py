import json

with open("test_raw.txt", 'r') as cc:
    data = cc.read()
    # print(data)

# if data.find("AIPictureData") == -1:
#     print("NO")
# else:
#     print("cc")
# file = open("js.txt", "a")
# file.write(value)
y = len(data)
# print(y)
# print(data.find("AIPictureData"))
i = data.index("AIPictureData")
print(i)
ii = i + 4
# print(ii)
# print(data[ii::])
# file = open("js.txt", "a")
# file.write(data[ii:])
