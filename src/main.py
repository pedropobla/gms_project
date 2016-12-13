"""
This file contains the main logic for training and evaluating a graphical
model that predicts New York Citi Bikes future locations.
"""

import utils
import matplotlib.pyplot as plt
import numpy as np
import pdb
import os

plt.style.use('ggplot')

out_folder = os.path.join(os.path.split(__file__)[0], "..", "out")

def process_trips(trips_df):
    print(trips_df.info())
    print(trips_df.dtypes)
    print(trips_df.dtypes)
    print(trips_df.head())
    print(trips_df.tail())
    print("min bikeid: {}".format(trips_df['bikeid'].min()))
    print("max bikeid: {}".format(trips_df['bikeid'].max()))
    print("min start station id: {}".format(trips_df['start station id'].min()))
    print("max start station id: {}".format(trips_df['start station id'].max()))
    print("min end station id: {}".format(trips_df['end station id'].min()))
    print("max end station id: {}".format(trips_df['end station id'].max()))


def plot_avg_week_for_stations(start_time_matrix,
                               station_idx,
                               time_at_idx,
                               station_ids,
                               file_name):
    print("Plotting average weeks for stations")
    # -5*48 to exclude last 5 days, to end on Sunday at 23:59
    mat = start_time_matrix[:,:-5*48].todense().A
    n_stations, total_buckets = mat.shape
    mat = mat.reshape((n_stations, -1, 48*7))
    avg = np.mean(mat, axis=1)

    plt.title("Start time")
    plt.ylabel('Number of trips exiting station')
    plt.xlabel('Time bucket')

    x_axis = [time_at_idx(i) for i in range(0, 48*7)]
    for station_id in station_ids:
        print("\r\tPlotting average week for station {}".format(station_id), end="")
        plt.plot(x_axis, avg[station_idx[station_id],:], alpha=0.7, label=station_id)
        print("\r" + " "*80 + "\r", end="")
    plt.xticks(x_axis, [x.hour if x.hour in [0,6,12,18] else "" for x in x_axis], rotation='vertical')
    plt.legend()
    plt.savefig(os.path.join(out_folder, file_name))
    plt.clf()


def plot_total_start_trips(start_time_matrix, time_idx):
    print("Plotting total trips")

    total_start_trips = np.sum(start_time_matrix, axis=0)
    plt.plot(total_start_trips.A.flatten())
    plt.title("Total trips in 30 minute intervals from 2013 - 2015")
    plt.savefig(os.path.join(out_folder, "total_trips.pdf"))
    plt.clf()


def main():
    # Ensure all data has been downloaded and processed
    #utils.download_trips_dataset()
    #for y in utils.YEARS:
    #   utils.load_trips_dataframe(y)
    #   process_trips(trips_df)

    start_time_matrix, station_idx, time_idx, time_at_idx = utils.load_start_time_matrix()
    stop_time_matrix, _, _ = utils.load_stop_time_matrix()
    start_time_matrix = start_time_matrix.astype(np.int16)
    stop_time_matrix = stop_time_matrix.astype(np.int16)
    inverse_station = { v: k for k, v in station_idx.items() }

    plot_avg_week_for_stations(start_time_matrix, station_idx, time_at_idx, [360], "avg_week_start_time.pdf")
    plot_avg_week_for_stations(stop_time_matrix, station_idx, time_at_idx, [360], "avg_week_stop_time.pdf")
    plot_avg_week_for_stations(stop_time_matrix-start_time_matrix, station_idx, time_at_idx, [360], "avg_week_flow_time.pdf")
    plot_total_start_trips(start_time_matrix, time_idx)


if __name__ == '__main__':
    main()
