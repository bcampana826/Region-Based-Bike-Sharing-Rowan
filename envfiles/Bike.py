class Bike:

    def __init__(self, string_location):
        # Has to be in form int;int
        numbers = string_location.split(";")
        self.x_coord = int(numbers[0])
        self.y_coord = int(numbers[1])

    def set_location(self, string_location):
        numbers = string_location.split[";"]
        self.x_coord = int(numbers[0])
        self.y_coord = int(numbers[1])