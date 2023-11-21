# This script fused all the ply stored in the mensura folder. Each measurement
# was done with moving 20cm laterally along a wall.
import pandas as pd 
import numpy as np
import os 
import open3d as od
from tqdm import tqdm

# Listing all the files in mensura directory and distance from start
path = os.path.join("mensura/")
np_coordinates_list = []
for file in tqdm(os.listdir(path)): 
    distance = 2 * (int(file.split(".")[0]) -1) 
    # open .ply file and save distances to numpy array
    # TODO: add following code to loop
    input_file = os.path.join(f"mensura/{file}")
    myfile = open(input_file, 'r')
    coordinates = []
    for (num, line) in enumerate(myfile): 
        if (num > 13) and (len(line.split())<=3) and (num%2 != 0):
            x, y, z = line.split()
            coordinates.append([float(x)+distance, float(y), float(z)])
    # turning coordinates list in np array
    np_coordinates = np.array(coordinates)
    np_coordinates_list.append(np_coordinates)
    # Creating a point cloud from data
# concatenating all the coordinates together
concatenated_point_cloud = np.concatenate((np_coordinates_list))

point_cloud = od.geometry.PointCloud()
point_cloud.points = od.utility.Vector3dVector(concatenated_point_cloud)
od.io.write_point_cloud("Point.ply", point_cloud)
# TODO: On se déplace en x négatif on commence à 0 et on tend vers -infinity
