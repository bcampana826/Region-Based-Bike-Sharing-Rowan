class Trip():

    def __init__(self, string_trip):
        self.x_start = 0
        self.y_start = 0
        self.x_end = 0
        self.y_end = 0

        areas = string_trip.strip().strip("{").strip("}").split(",")

        numbers = areas[0].strip("(").strip(")").split(";")

        self.x_start = int(numbers[0])
        self.y_start = int(numbers[1])

        numbers = areas[1].strip("{").strip("}").strip("(").strip(")").split(";")
        self.x_end = int(numbers[0])
        self.y_end = int(numbers[1])