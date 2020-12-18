bobri = "54321"
globina = [4,2,3]

for x in globina:
    bobri = bobri[:- x -1:-1] + bobri[:- x]
    print(bobri)
