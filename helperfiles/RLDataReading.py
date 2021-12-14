import os

# 16679 for long
# 50 for greed

data_file = open(("../RBBS-Data/LongStatReadings.txt"), "w")

long_stats_dirc = "../RBBS-Data/Static-stats"
long_greedy_dirc = "../RBBS-Data/long-stats-greedy"

for filename in os.listdir(long_stats_dirc):
    long_file = open((long_stats_dirc + "/" + filename), "r")
    long_file_data = [float(n) for n in long_file]
    long_start = long_file_data[5]
    long_end = long_file_data[16679]
    long_learn = long_end - long_start

    #greedy_file = open((long_greedy_dirc + "/" + filename.strip(".txt") + "-greedy.txt"), "r")
    #greedy_file_data = [float(n) for n in greedy_file]
    #greedy = greedy_file_data[50]
                                                                                        #" " + str(greedy)+
    data_file.write(filename + " " + str(long_start) + " " + str(long_end) + " " + str(long_learn) + "\n")


