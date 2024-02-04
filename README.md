# Pathfinder

A robot who explores a mazes and navigates with in it to a chosen point

## Overview
[![Video of the robot exploring](presentation/Movie/explorer/start_explorer.png)](presentation/explorer.mp4)
Set in a 4x4 maze, the robots explores the maze by its own and their by creating a map, thats written to disk. (-> [Video of Explorer stage](presentation/explorer.mp4))


[![Video of the robot navigating through a maze](presentation/Movie/finder/start_finder.png)](presentation/finder.mp4)
Given a map and current position the robot finds the shortes path to a given goal and moves to it
(-> [Video of Navigation stage](presentation/finder.mp4))

## System
There are two components in this system: The Client (a Laptop or Tower Computer) and the EV3 robot it self. 

The EV3 robot is controlled via protocol based on tcp. (This is specified [here](./ProtocolSpec.md)). The Script that runs on the EV3 can be found in the [robot](./src/robot) folder. The Robot is a lego Mindstorms EV3 running [EV3Dev](https://www.ev3dev.org/) and is connected via WIFI to the client.

The pathfinding and controlle on the other side is done on the client due to the hardware constrains on the EV3. The code for it can be found [here](./src/client/). Dijkstras algorithm is used to determain the shortes path.


