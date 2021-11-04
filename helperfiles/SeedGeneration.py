import os
import random
from datetime import datetime

from scipy.stats import binom


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

# uh oh - POPULARTIY?
def generate_seed_bin(map_size, budget, bikes_in_circulation, max_hourly_customers):
    # Data Saving Setup
    seed_number = len(os.listdir('../RBBS-Seeds')) + 1
    data_file = open(("../RBBS-Seeds/" + str(seed_number) + ".txt"), "w")

    data_file.write(
        "2-Dimensional Region Based Bike Env Seed (BINOMIAL DISTRIBUTION) " + str(seed_number) + " generated at " +
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

    # setting the values
    # of n and p
    n = map_size**2
    p = 0.5
    # defining the list of r values
    reg_list = list(range(map_size ** 2))

    # obtaining the mean and variance
    mean, var = binom.stats(n, p)
    # list of pmf values
    dist = [binom.pmf(r, n, p) for r in reg_list]
    dist[1] += dist[0]
    dist[0] = 0.0
    random.shuffle(dist)

    # Generating Trips!
    for hour in range(12):
        data_file.write("Hour: " + str(hour) + ": ")

        # Generate Trips in this Hour
        number_of_trips = random.randint(int(max_hourly_customers / 2), max_hourly_customers)

        for trip in range(number_of_trips):

            trip_chance = random.random()
            adding = 0.0
            loops = 0
            going = True
            while (loops < len(dist) and going):
                adding += dist[loops]
                if (trip_chance <= adding):
                    going = False
                else:
                    loops += 1

            x = (loops%map_size) * 10
            y = int(loops/map_size) * 10

            trip_start_x = random.randint(x, x + 9)
            trip_start_y = random.randint(y, y + 9)

            trip_end_x = random.randint(0, 10 * map_size - 1)
            trip_end_y = random.randint(0, 10 * map_size - 1)

            data_file.write("{(" + str(trip_start_x) + ";" + str(trip_start_y) +
                            "),(" + str(trip_end_x) + ";" + str(trip_end_y) + ")}")

            if trip != number_of_trips - 1:
                data_file.write("-")

        data_file.write("\n")

    data_file.close()

# working mans a sucker
def generate_seed_working(map_size, budget, bikes_in_circulation, max_hourly_customers):
    '''
    This seed generations going to create to groups - home sector, and a work sector, and a middle section

    over the 12 hour period, different patterns will occur
    assuming our 12 hour period starts at say 7 am, and goes to 7 pm

    0 - 1 - 2 will be working transport hours, where 40HW/40HR/20RR will be in effect with 50%-100% customers

    3 - 4 will be lower customer hours, with 100% random but only 10 - 30% customers

    5 will be to the mini surge in the middle section, like a lunch time rush, with 40WM/20HM/20RM/20RR 50 - 75 % customers

    6 will be a mini surge back, with 40MW/20MH/20MR/20RR 50 - 75 % customers

    7 - 8 will be lower customer hours, will 100% random but only 10 - 30% customers

    9 - 10 - 11 will be home transport hours, where 40WH/40WR/20RR will be in effect with 50%-100% customers
    '''

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

    # creating trip groups
    '''
    so like
    [ ][ ][ ][ ][ ][ ][ ]
    [ ][M][ ][W][W][W][ ]
    [ ][ ][M][ ][W][W][ ]
    [ ][H][ ][M][ ][W][ ]
    [ ][H][H][ ][M][ ][ ]
    [ ][H][H][H][ ][M][ ]
    [ ][ ][ ][ ][ ][ ][ ]
    
    [ ][ ][ ][ ][ ][ ][ ][ ]
    [ ][M][ ][W][W][W][W][ ]
    [ ][ ][M][ ][W][W][W][ ]
    [ ][H][ ][M][ ][W][W][ ]
    [ ][H][H][ ][M][ ][W][ ]
    [ ][H][H][H][ ][M][ ][ ]
    [ ][H][H][H][H][ ][M][ ]
    [ ][ ][ ][ ][ ][ ][ ][ ]
    '''
    home = []
    work = []
    mid = []

    for i in range(int(map_size/2)):
        for j in range(int(map_size/2)-i):
            home.append([i+1,map_size-2-j])
            work.append([map_size-2-j,i+1])

    for i in range(map_size - 2):
        mid.append([i+1,i+1])




    # Generating Trips!
    for hour in range(12):
        data_file.write("Hour: " + str(hour) + ": ")

        if hour == 0 or hour == 1 or hour == 2:
            # 0 - 1 - 2 will be working transport hours, where 40HW/40HR/20RR will be in effect with 50%-100% customers
            number_of_trips = random.randint(int(max_hourly_customers *.5), max_hourly_customers)

            for trip in range(number_of_trips):

                choice = random.randint(0, 99)

                if choice < 39:
                    # H W
                    start_reg = random.choice(home)
                    end_reg = random.choice(work)

                    trip_start_x = random.randint(start_reg[0]*10, (start_reg[0]+1)*10 - 1)
                    trip_start_y = random.randint(start_reg[1]*10, (start_reg[1]+1)*10 - 1)

                    trip_end_x = random.randint(end_reg[0]*10, (end_reg[0]+1)*10 - 1)
                    trip_end_y = random.randint(end_reg[1]*10, (end_reg[1]+1)*10 - 1)

                elif choice < 79:
                    # H R
                    start_reg = random.choice(home)

                    trip_start_x = random.randint(start_reg[0] * 10, (start_reg[0] + 1) * 10 - 1)
                    trip_start_y = random.randint(start_reg[1] * 10, (start_reg[1] + 1) * 10 - 1)

                    trip_end_x = random.randint(0, 10 * map_size - 1)
                    trip_end_y = random.randint(0, 10 * map_size - 1)

                else:

                    trip_start_x = random.randint(0, 10 * map_size - 1)
                    trip_start_y = random.randint(0, 10 * map_size - 1)

                    trip_end_x = random.randint(0, 10 * map_size - 1)
                    trip_end_y = random.randint(0, 10 * map_size - 1)

                data_file.write("{(" + str(trip_start_x) + ";" + str(trip_start_y) +
                                "),(" + str(trip_end_x) + ";" + str(trip_end_y) + ")}")

                if trip != number_of_trips - 1:
                    data_file.write("-")

        elif 2 < hour >= 8:
            # 3 - 4, 7 - 8 will be lower customer hours, with 100% random but only 10 - 30% customers
            number_of_trips = random.randint(int(max_hourly_customers * .1), int(max_hourly_customers * .3))

            for trip in range(number_of_trips):

                trip_start_x = random.randint(0, 10 * map_size - 1)
                trip_start_y = random.randint(0, 10 * map_size - 1)

                trip_end_x = random.randint(0, 10 * map_size - 1)
                trip_end_y = random.randint(0, 10 * map_size - 1)

                data_file.write("{(" + str(trip_start_x) + ";" + str(trip_start_y) +
                                "),(" + str(trip_end_x) + ";" + str(trip_end_y) + ")}")

                if trip != number_of_trips - 1:
                    data_file.write("-")
        else:
            #9 - 10 - 11 will be home transport hours, where 40WH/40WR/20RR will be in effect with 50%-100% customers
            number_of_trips = random.randint(int(max_hourly_customers *.5), max_hourly_customers)

            for trip in range(number_of_trips):

                choice = random.randint(0, 99)

                if choice < 39:
                    # W H
                    start_reg = random.choice(work)
                    end_reg = random.choice(home)

                    trip_start_x = random.randint(start_reg[0]*10, (start_reg[0]+1)*10 - 1)
                    trip_start_y = random.randint(start_reg[1]*10, (start_reg[1]+1)*10 - 1)

                    trip_end_x = random.randint(end_reg[0]*10, (end_reg[0]+1)*10 - 1)
                    trip_end_y = random.randint(end_reg[1]*10, (end_reg[1]+1)*10 - 1)

                elif choice < 79:
                    # W R
                    start_reg = random.choice(work)

                    trip_start_x = random.randint(start_reg[0] * 10, (start_reg[0] + 1) * 10 - 1)
                    trip_start_y = random.randint(start_reg[1] * 10, (start_reg[1] + 1) * 10 - 1)

                    trip_end_x = random.randint(0, 10 * map_size - 1)
                    trip_end_y = random.randint(0, 10 * map_size - 1)

                else:

                    trip_start_x = random.randint(0, 10 * map_size - 1)
                    trip_start_y = random.randint(0, 10 * map_size - 1)

                    trip_end_x = random.randint(0, 10 * map_size - 1)
                    trip_end_y = random.randint(0, 10 * map_size - 1)

                data_file.write("{(" + str(trip_start_x) + ";" + str(trip_start_y) +
                                "),(" + str(trip_end_x) + ";" + str(trip_end_y) + ")}")

                if trip != number_of_trips - 1:
                    data_file.write("-")

        data_file.write("\n")

    data_file.close()

    return seed_number

generate_seed_working(7,600,300,245)

''' elif hour == 5:
            #5 will be to the mini surge in the middle section, like a lunch time rush, with 40WM/20HM/20RM/20RR 50 - 75 % customers


            number_of_trips = random.randint(int(max_hourly_customers * .5), int(max_hourly_customers * .75))

            for trip in range(number_of_trips):

                choice = random.randint(0, 99)

                if choice < 39:
                    # W M
                    start_reg = random.choice(work)
                    end_reg = random.choice(mid)

                    trip_start_x = random.randint(start_reg[0]*10, (start_reg[0]+1)*10 - 1)
                    trip_start_y = random.randint(start_reg[1]*10, (start_reg[1]+1)*10 - 1)

                    trip_end_x = random.randint(end_reg[0]*10, (end_reg[0]+1)*10 - 1)
                    trip_end_y = random.randint(end_reg[1]*10, (end_reg[1]+1)*10 - 1)

                elif choice < 59:
                    # H M
                    start_reg = random.choice(home)
                    end_reg = random.choice(mid)

                    trip_start_x = random.randint(start_reg[0]*10, (start_reg[0]+1)*10 - 1)
                    trip_start_y = random.randint(start_reg[1]*10, (start_reg[1]+1)*10 - 1)

                    trip_end_x = random.randint(end_reg[0]*10, (end_reg[0]+1)*10 - 1)
                    trip_end_y = random.randint(end_reg[1]*10, (end_reg[1]+1)*10 - 1)

                elif choice < 79:
                    # R M
                    end_reg = random.choice(mid)

                    trip_start_x = random.randint(0, 10 * map_size - 1)
                    trip_start_y = random.randint(0, 10 * map_size - 1)

                    trip_end_x = random.randint(end_reg[0] * 10, (end_reg[0] + 1) * 10 - 1)
                    trip_end_y = random.randint(end_reg[1] * 10, (end_reg[1] + 1) * 10 - 1)

                else:

                    trip_start_x = random.randint(0, 10 * map_size - 1)
                    trip_start_y = random.randint(0, 10 * map_size - 1)

                    trip_end_x = random.randint(0, 10 * map_size - 1)
                    trip_end_y = random.randint(0, 10 * map_size - 1)

                data_file.write("{(" + str(trip_start_x) + ";" + str(trip_start_y) +
                                "),(" + str(trip_end_x) + ";" + str(trip_end_y) + ")}")

                if trip != number_of_trips - 1:
                    data_file.write("-")

        elif hour == 6:
            #6 will be a mini surge back, with 40MW/20MH/20MR/20RR 50 - 75 % customers

            number_of_trips = random.randint(int(max_hourly_customers * .5), int(max_hourly_customers * .75))

            for trip in range(number_of_trips):

                choice = random.randint(0, 99)

                if choice < 39:
                    # M W
                    start_reg = random.choice(mid)
                    end_reg = random.choice(work)

                    trip_start_x = random.randint(start_reg[0] * 10, (start_reg[0] + 1) * 10 - 1)
                    trip_start_y = random.randint(start_reg[1] * 10, (start_reg[1] + 1) * 10 - 1)

                    trip_end_x = random.randint(end_reg[0] * 10, (end_reg[0] + 1) * 10 - 1)
                    trip_end_y = random.randint(end_reg[1] * 10, (end_reg[1] + 1) * 10 - 1)

                elif choice < 59:
                    # H M
                    start_reg = random.choice(mid)
                    end_reg = random.choice(home)

                    trip_start_x = random.randint(start_reg[0] * 10, (start_reg[0] + 1) * 10 - 1)
                    trip_start_y = random.randint(start_reg[1] * 10, (start_reg[1] + 1) * 10 - 1)

                    trip_end_x = random.randint(end_reg[0] * 10, (end_reg[0] + 1) * 10 - 1)
                    trip_end_y = random.randint(end_reg[1] * 10, (end_reg[1] + 1) * 10 - 1)

                elif choice < 79:
                    # M R
                    start_reg = random.choice(mid)

                    trip_start_x = random.randint(start_reg[0] * 10, (start_reg[0] + 1) * 10 - 1)
                    trip_start_y = random.randint(start_reg[1] * 10, (start_reg[1] + 1) * 10 - 1)

                    trip_end_x = random.randint(0, 10 * map_size - 1)
                    trip_end_y = random.randint(0, 10 * map_size - 1)

                else:

                    trip_start_x = random.randint(0, 10 * map_size - 1)
                    trip_start_y = random.randint(0, 10 * map_size - 1)

                    trip_end_x = random.randint(0, 10 * map_size - 1)
                    trip_end_y = random.randint(0, 10 * map_size - 1)

                data_file.write("{(" + str(trip_start_x) + ";" + str(trip_start_y) +
                                "),(" + str(trip_end_x) + ";" + str(trip_end_y) + ")}")

                if trip != number_of_trips - 1:
                    data_file.write("-")'''