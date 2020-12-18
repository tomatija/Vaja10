x = 0
rezAna1 = 0
rezAna2 = 0
sobaAna = 0
stevnikSoba = 0
while x < 1000:
    rezAna1 = (1664525*rezAna1 + 1013904223) % pow(2,32)
    sobaAna = rezAna1 % 10
    if sobaAna == 6:
        stevnikSoba += 1
    x+=1
print(stevnikSoba)