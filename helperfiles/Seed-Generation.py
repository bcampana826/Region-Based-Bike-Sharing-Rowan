import os
import random
from datetime import datetime

def generate_seed(map_size, budget, bikes_in_circulation, max_hourly_customers):
    # Data Saving Setup
    seed_number = len(os.listdir('../RBBS-Seeds')) + 1
    data_file = open(("../RBBS-Seeds/" + str(seed_number) + ".txt"), "w")

    data_file.write(
        "2-Dimensional Region Based Bike Env Seed " + str(seed_number) + " generated at " +
        str(datetime.now()) + "\n")
    data_file.write(str(map_size) + "," + str(budget) + "," + str(bikes_in_circulation) + "," + str(
        max_hourly_customers) + "\n")

    # Generate Bike Start Locations
    bike_locations = []
    for bike in range(bikes_in_circulation):
        bike_x = random.randint(0, 10 * map_size - 1)
        bike_y = random.randint(0, 10 * map_size - 1)
        bike_locations.append("(" + str(bike_x) + ";" + str(bike_y) + ")")

    data_file.write(str(bike_locations) + "\n")

    # Generating Trips!
    for hour in range(12):
        data_file.write("Hour: " + str(hour) + ": ")

        # Generate Trips in this Hour
        number_of_trips = random.randint(int(max_hourly_customers/2), max_hourly_customers)

        for trip in range(number_of_trips):

            trip_start_x = random.randint(0, 10 * map_size-1)
            trip_start_y = random.randint(0, 10 * map_size-1)

            trip_end_x = random.randint(0, 10 * map_size-1)
            trip_end_y = random.randint(0, 10 * map_size-1)

            data_file.write("{(" + str(trip_start_x) + ";" + str(trip_start_y) +
                            "),(" + str(trip_end_x) + ";" + str(trip_end_y) + ")}")

            if trip != number_of_trips -1:
                data_file.write("-")

        data_file.write("\n")

    data_file.close()

    return seed_number

generate_seed(5, 100,50,50)