
# First import the library
import pyrealsense2 as rs
import open3d as o3d
import tkinter as tk
import os 
import glob


display = True # if the user wants to display 3 model after each measurement
mensura_numerus = 1
# Creating tkinter window 
window = tk.Tk()

pittacium = tk.Label(text=f"Press to start measure {mensura_numerus}")
pittacium.pack()

def toggle_display(): 
    global display
    global display_toggle
    if display:
        display = False
    else: 
        display = True
    meus_textus = f"Display: {display}"
    display_toggle.config(text=meus_textus)

def clear_folder():
    global mensura_numerus
    print("Start clear folder")
    files = glob.glob(os.path.join("mensura/*"))
    for f in files: 
        os.remove(f)
    mensura_numerus = 1
    print("All files cleared")


def velim(): 
    global mensura_numerus 
    global pittacium 
    global display
    # Declare pointcloud object, for calculating pointclouds and texture mappings
    print("Initium")
    pc = rs.pointcloud()
    # We want the points object to be persistent so we can display the last cloud when a frame drops
    points = rs.points()

    # Declare RealSense pipeline, encapsulating the actual device and sensors
    pipe = rs.pipeline()
    config = rs.config()
    # Enable depth stream
    config.enable_stream(rs.stream.depth)

    # Start streaming with chosen configuration
    pipe.start(config)

    # We'll use the colorizer to generate texture for our PLY
    # (alternatively, texture can be obtained from color or infrared stream)
    colorizer = rs.colorizer()
    
    try:
        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()
        colorized = colorizer.process(frames)

        # Create save_to_ply object
        filename = f"{mensura_numerus}.ply"
        myfile = os.path.join("mensura",filename)
        ply = rs.save_to_ply(myfile)

        # Set options to the desired values
        # In this example we'll generate a textual PLY with normals (mesh is already created by default)
        ply.set_option(rs.save_to_ply.option_ply_binary, False)
        ply.set_option(rs.save_to_ply.option_ply_normals, False) # <- I change here

        print(f"Saving to {myfile}...")
        # Apply the processing block to the frameset which contains the depth frame and the texture
        ply.process(colorized)
        print("Done")
    finally:
        pipe.stop()
        mensura_numerus += 1
        print(mensura_numerus)
        pittacium.config(text=f"Press to start measure {mensura_numerus}")
    if display:
        # this part of the code renders the lidar 3 model using open3d
        pcd = o3d.io.read_point_cloud(myfile)
        o3d.visualization.draw_geometries([pcd])
crustulum = tk.Button(window, text="Press to start acquisition", command= velim)
crustulum.pack()
# adding purge measurement files 
vinum = tk.Button(window, text="Press to reset measures", command=clear_folder)
vinum.pack()

# toggle display button 
meus_textus = f"Display: {display}"
display_toggle= tk.Button(window, text=meus_textus, command=toggle_display)
display_toggle.pack()

window.mainloop()

