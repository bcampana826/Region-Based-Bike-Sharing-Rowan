class Region:

    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.bikes = []
        self.surrounding_regions = []

    def take_bike(self, bike):

        self.bikes.remove(bike)
        self.bikes = list(filter(None, self.bikes))
        return bike

    # Initializes the surrounding_regions field
    def set_surrounding_regions(self, size):
        #   Given a region, will save a list of [region, boolean] where region is the region and boolean is true
        #   if directly next to
        x = self.x_coord
        y = self.y_coord

        for i in range(-1, 1):
            for j in range(-1, 1):
                if 0 <= x + i < size and 0 <= y + j < size:
                    if (i != 0 or j != 0) and (i==0 or j==0):
                        self.surrounding_regions.append([i+x,j+y])

