#!/usr/bin/env python
import pandas as pd
import numpy as np


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def euclidean_speed(euclidean_distance, travel_time):
    return euclidean_distance / travel_time


def unit_vector(startx, starty, endx, endy):
    start = np.array([startx, starty])
    end = np.array([endx, endy])
    vec = end - start
    return vec / np.linalg.norm(vec)


def parametric_line(startx, starty, endx, endy, depart_time, travel_time, unit_vec, speed):
    def x(t):
        arrival_time = depart_time + travel_time
        if depart_time <= t <= arrival_time:
            t = t - depart_time
            return startx + unit_vec[0] * speed * t
        elif t < depart_time:
            return startx;
        else:
            return endx;

    def y(t):
        arrival_time = depart_time + travel_time
        if depart_time <= t <= arrival_time:
            t = t - depart_time
            return starty + unit_vec[1] * speed * t
        elif t < depart_time:
            return starty;
        else:
            return endy;

    return x, y


def euclidean_path_to_list(df, time_step, start_time=0, max_time=86400, include_time=True):
    paths = []
    for index, row in df.iterrows():
        speed = euclidean_speed(row['euclidean_distance'], row['trav_time'])
        startx = row['start_x']
        starty = row['start_y']
        endx = row['end_x']
        endy = row['end_y']
        unit = unit_vector(startx, starty, endx, endy)
        depart_time = row['dep_time']
        travel_time = row['trav_time']
        x, y = parametric_line(startx, starty, endx, endy, depart_time, travel_time, unit, speed)
        path = []
        if include_time:
            for t in range(start_time, max_time, time_step):
                path.append((t, x(t), y(t)))
        else:
            for t in range(start_time, max_time, time_step):
                path.append((x(t), y(t)))
        paths.append(path)
    return paths


def convertTime(df, write=False, outname="0.trips-1.csv"):
    df['dep_time'] = df['dep_time'].map(lambda x: get_sec(x))
    df['trav_time'] = df['trav_time'].map(lambda x: get_sec(x))
    df['wait_time'] = df['wait_time'].map(lambda x: get_sec(x))
    if write:
        df.to_csv(outname)
    return df


def paths_to_file(paths, limit=False, set_limit=0, name="0.trips-iter.csv.gz"):
    paths_list = []
    if not limit:
        set_limit = len(paths)
    else:
        if set_limit == 0:
            print("You need to set limit for paths to file")
            return None
        if set_limit > len(paths):
            print("Set limit has to be less than length of paths")
            return None
    for i, path in enumerate(paths):
        if i == set_limit:
            break
        for coord in path:
            a = [i]
            for z in coord:
                a.append(z)
            paths_list.append(a)
    df = pd.DataFrame(paths_list, columns=['PersonId', 'Time', 'X', 'Y'])
    df.to_csv(name, index=False)
    return df


if __name__ == "__main__":
    with open("0.trips.csv", "r") as file:
        df = pd.read_csv(file, sep=";")
    df = convertTime(df)
    euclidean_paths = euclidean_path_to_list(df, 1, start_time=25000, max_time=32700)
    paths_to_file(euclidean_paths, limit=True, set_limit=6000, name="0.trips-iter.csv")
