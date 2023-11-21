# This script fused all the ply stored in the mensura folder. Each measurement
# was done with moving 20cm laterally along a wall.
import pandas as pd 
import numpy as np
import os 
import open3d as od

# Listing all the files in mensura directory and distance from start
path = os.path.join("mensura/")
for file in os.listdir(path): 
    distance = 20 * (int(file.split(".")[0]) -1) 
    print(f"{file} @ {distance}")

# open .ply file and save distances to numpy array
# TODO: add following code to loop
input_file = os.path.join("mensura/1.ply")
file = open(input_file, 'r')
coordinates = []
for (num, line) in enumerate(file): 
    if (num > 13) and (len(line.split())<=3) and (num%2 != 0):
        x, y, z = line.split()
        coordinates.append([x, y, z])
# turning coordinates list in np array
np_coordinates = np.array(coordinates)



# Creating a point cloud from data
'''
point_cloud = od.geometry.PointCloud()
point_cloud.points = od.utility.Vector3dVector(np_coordinates)
od.io.write_point_cloud("Point_cloud.ply", point_cloud)
'''
# TODO: On se déplace en x négatif on commence à 0 et on tend vers -infinity
