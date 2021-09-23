from envfiles import Region

class Region:

    def __init__(self):
        pass

test = [[Region()]*3]*3
test[0][1] = Region()

print(test)