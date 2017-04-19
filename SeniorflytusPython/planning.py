from grid import *
from visualizer import *
import threading
from queue import PriorityQueue
import math

def astar(grid, heuristic):
    """Perform the A* search algorithm on a defined grid

        Arguments:
        grid -- CozGrid instance to perform search on
        heuristic -- supplied heuristic function
    """
    startCell = grid.getStart()
    prev = {}
    prev[startCell] = None
    # FOR OUR PURPOSES, ALWAYS ONE GOAL STATE
    goalCell = grid.getGoals()[0]
    pri_queue = PriorityQueue()
    pri_queue.put((heuristic(startCell, goalCell), startCell, 0))
    found_goal = False
    while not pri_queue.empty():
        cur_est_coord = pri_queue.get()
        grid.addVisited(cur_est_coord[1])
        print(cur_est_coord[1])
        # goal, then break
        #print(cur_est_coord)
        if cur_est_coord[1] == goalCell:
            print("found goal")
            #prev[goalCell] = cur_est_coord[1]
            found_goal = True
            break
        # if not goal, then add all neighbors
        for neighbor_coord_weight in grid.getNeighbors(cur_est_coord[1]):
            # if neighbor_coord_weight[0] == (4,1) and prev.get(neighbor_coord_weight[0]) != None:
            #     print()
            #     print(prev[neighbor_coord_weight[0]][1])
            #     print((heuristic(neighbor_coord_weight[0], goalCell) + neighbor_coord_weight[1] + (cur_est_coord[0] - heuristic(cur_est_coord[1], goalCell))))
            #     print()
            if prev.get(neighbor_coord_weight[0]) == None and neighbor_coord_weight[0] != startCell:
                # if neighbor_coord_weight[0] == (3,1):
                #     print("3,1 is neighbor: ", cur_est_coord)
                prev[neighbor_coord_weight[0]] = cur_est_coord[1], heuristic(neighbor_coord_weight[0], goalCell) + neighbor_coord_weight[1] + cur_est_coord[2], cur_est_coord[2] + neighbor_coord_weight[1]
                #print("coord weight: ", neighbor_coord_weight[1])
                #print("heuristic: ", heuristic(neighbor_coord_weight[0], goalCell))
                #print("prev weight: ", (cur_est_coord[0] - heuristic(cur_est_coord[1], goalCell)))
                pri_queue.put((heuristic(neighbor_coord_weight[0], goalCell) + neighbor_coord_weight[1] + cur_est_coord[2], neighbor_coord_weight[0], cur_est_coord[2] + neighbor_coord_weight[1]))
            elif prev.get(neighbor_coord_weight[0]) != None and neighbor_coord_weight[0] != startCell:
                if cur_est_coord[2] + neighbor_coord_weight[1] < prev[neighbor_coord_weight[0]][2]:
                    prev[neighbor_coord_weight[0]] = cur_est_coord[1], (heuristic(neighbor_coord_weight[0], goalCell) + neighbor_coord_weight[1] + cur_est_coord[2]), cur_est_coord[2]
            #elif prev.get(neighbor_coord_weight[0]) != None and prev[neighbor_coord_weight[0]][1] == (heuristic(neighbor_coord_weight[0], goalCell) + neighbor_coord_weight[1] + (cur_est_coord[0] - heuristic(cur_est_coord[1], goalCell))) and neighbor_coord_weight[0] != startCell:
            #     print("RUNNING", neighbor_coord_weight)
            #     print("first", heuristic(cur_est_coord[1], goalCell))
            #     print("second", heuristic(prev[neighbor_coord_weight[0]][0], goalCell))
                #old_actual_dist = prev[neighbor_coord_weight[0]][1] - heuristic(prev[neighbor_coord_weight[0]][0], goalCell)
                #print(cur_est_coord)
                #print(heuristic(cur_est_coord[1], goalCell))
                #cur_actual_dist = neighbor_coord_weight[1] + (cur_est_coord[0] - heuristic(cur_est_coord[1], goalCell))
                #print("old, cur", old_actual_dist, cur_actual_dist)
                #if cur_actual_dist < old_actual_dist:
                #    prev[neighbor_coord_weight[0]] = cur_est_coord[1], (heuristic(neighbor_coord_weight[0], goalCell) + neighbor_coord_weight[1] + (cur_est_coord[0] - heuristic(cur_est_coord[1], goalCell)))
                # if heuristic(cur_est_coord[1], goalCell) > heuristic(prev[neighbor_coord_weight[0]][0], goalCell):
                #     prev[neighbor_coord_weight[0]] = cur_est_coord[1], (heuristic(neighbor_coord_weight[0], goalCell) + neighbor_coord_weight[1] + (cur_est_coord[0] - heuristic(cur_est_coord[1], goalCell)))
                #print(cur_est_coord)
    #print(prev)
    #print(prev[(4,1)])
    final_path = []
    final_path.append(goalCell)
    if found_goal:
        cur_prev = prev[goalCell]
        #print(cur_prev)
        while cur_prev != None:
            #print(cur_prev)
            final_path.append(cur_prev[0])
            cur_prev = prev[cur_prev[0]]
    grid.setPath(final_path[::-1])
	#pass # Your code here


def heuristic(current, goal):
    """Heuristic function for A* algorithm

        Arguments:
        current -- current cell
        goal -- desired goal cell
    """
    #print(math.sqrt((current[0] - goal[0]) ** 2 + (current[1] - goal[1]) ** 2))
    x = abs(current[0]-goal[0])
    y = abs(current[1]-goal[1])
    return max(x, y) + (math.sqrt(2)-1)*min(x,y)
    #return math.sqrt((current[0] - goal[0]) ** 2 + (current[1] - goal[1]) ** 2)
    #return 1 # Your code here

def setup(start, goal):
    """Cozmo search behavior. See assignment document for details

        Has global access to grid, a CozGrid instance created by the main thread, and
        stopevent, a threading.Event instance used to signal when the main thread has stopped.
        You can use stopevent.is_set() to check its status or stopevent.wait() to wait for the
        main thread to finish.

        Arguments:
        robot -- cozmo.robot.Robot instance, supplied by cozmo.run_program
    """

    print('RUNNING')

    #setup
    global grid, stopevent
    stopevent = threading.Event()
    grid = CozGrid("vl3rdfloor.json")
    #visualizer = Visualizer(grid)
    #updater = UpdateThread(visualizer)
    #updater.start()
    # robot = RobotThread()
    # robot.start()
    #stopevent.set()
        
    #global grid, stopevent
    #Grid is 26x18 of 25mm squares - vals are in mm
    
   
    ####################
    #SETUP GRID
    ####################
    
    grid.setStart(start)
    
    #grid.addGoal((29,1))
    grid.addGoal(goal)

    while True:#not stopevent.is_set():
        

        ####################
        #CALCULATE PATH
        ####################    
        
        astar(grid, heuristic)
        
        ####################
        #FOLLOW PATH
        ####################
        
        #Step will be used to iterate through the path
        step = 1
        
        heading = 6
        #heading will be the number of 45 degree rotations it is from the positive x direction (starting direction)
        #pointing up (+y) is 2 because it is 90 degrees (2 x 45 deg)
        #    6
        #  7 | 5
        #0---|---4 
        #  1 | 3
        #    2
        
        #Get the list of cells to navigate through
        path_cells = grid.getPath()
        added = False
        
        
        headings = []
        while step < len(path_cells):
            headings.append(calculateHeading(path_cells[step-1][0], path_cells[step-1][1], path_cells[step][0], path_cells[step][1]))
            step += 1
        print("Headings: " + str(headings))

        visualizer = Visualizer(grid)
        visualizer.start()
        #visualizer.update()
        #updater = UpdateThread(visualizer)
        #updater.start()
        
        #step = 0
        # while step < len(headings):
        #     #Calculate the direction to turn to
        #     #new_heading = calculateHeading(path_cells[step-1][0], path_cells[step-1][1], path_cells[step][0], path_cells[step][1])
        #     counter = 1
            
        #     new_heading = headings[step]
            
        #     #while (step + counter < len(headings) and headings[step + counter] == new_heading):
        #     #    counter += 1
            
        #     #Turn to the new heading
        #     heading = turnToHeading(heading, new_heading)
            
        #     #Move to next Square
        #     moveForward(counter)
            
        #     #Increment step and go again
        #     step += counter
        
        return headings          
        
        
def mmToGrid(length):
    return int((length / 25)) 
    #int will round down
    #25mm x 25mm grid cells
    #the offset of 1 allows for starting from (1,1)
    
def calculateHeading(cur_x, cur_y, new_x, new_y):
    #print(str(cur_x) + " " + str(cur_y) + " " + str(new_x) + " " + str(new_y))
    if (cur_y == new_y and cur_x < new_x):
        heading = 4
    elif (cur_y < new_y and cur_x < new_x):
        heading = 5
    elif (cur_y < new_y and cur_x == new_x):
        heading = 6
    elif (cur_y < new_y and cur_x > new_x):
        heading = 7
    elif (cur_y == new_y and cur_x > new_x):
        heading = 0
    elif (cur_y > new_y and cur_x > new_x):
        heading = 1
    elif (cur_y > new_y and cur_x == new_x):
        heading = 2
    elif (cur_y > new_y and cur_x < new_x):
        heading = 3
    #print(heading)
    return heading
    
# def turnToHeading(current_heading, new_heading):
#     #    6
#     #  7 | 5
#     #0---|---4 
#     #  1 | 3
#     #    2
    
#     #TODO doesnt properly deal with the 0-7 gap pointing left
#     turnDirection = 1
#     if (new_heading < current_heading):
#         turnDirection = -1
#     turns = abs(new_heading - current_heading)
#     #print(str(current_heading) + " | " + str(new_heading) + " | " + str(turns))
#     #TODO TURN  drone.
#     return new_heading
    
# def moveForward(cells=1):
#     #TODO MOVE FORWARD
#     pass
    
def addBlock(x, y, xOffset, yOffset, gpX=0, gpY=0):
    grid_x = mmToGrid(x) + xOffset
    grid_y = mmToGrid(y) + yOffset        
    
    print(gpX)
    print(gpY)
    if (not gpX == 0 or not gpY == 0):
        grid.addGoal((grid_x + 3 * gpX, grid_y + 3 * gpY))
    
    for i in [-2, 1, 0, -1, 2]:
        for j in [-2, 1, 0, -1, 2]:
            #if (gpX == 0 and gpY == 0):
            #    grid.addObstacle((grid_x + i, grid_y + j))
            #elif (i == gpX and j == gpY):
            #    grid.addGoal((grid_x + i + gpX, grid_y + j + gpY))
            #else:
            #if (not (i == 2 * gpX and j == 2 * gpY)):
            grid.addObstacle((grid_x + i, grid_y + j))

    
def calculatePath(startCoords):
    grid.clearPath()
    grid.clearStart()
    grid.setStart(startCoords)
    astar(grid, heuristic)
    print("Path calculated. Here we go.")

def calculateGoalRotation(zangle):
    #    6
    #  7 | 5
    #0---|---4 
    #  1 | 3
    #    2   - rotated 45 degrees
    
    if (zangle < 0):
        zangle = 360 + zangle
        
    print("Degrees: " + str(zangle))
    
    global finalHeading
    
    goalSquare = (-1, 0)
    finalHeading = 4
    if (zangle < 22.5):
        goalSquare = (-1, 0)
        finalHeading = 4
    elif (zangle < 67.5):
        goalSquare = (-1, -1)
        finalHeading = 5
    elif (zangle < 112.5):
        goalSquare = (0, -1)
        finalHeading = 6
    elif (zangle < 157.5):
        goalSquare = (1, -1)
        finalHeading = 7
    elif (zangle < 202.5):
        goalSquare = (1, 0)
        finalHeading = 0
    elif (zangle < 247.5):
        goalSquare = (1, 1)
        finalHeading = 1
    elif (zangle < 292.5):
        goalSquare = (0, 1)
        finalHeading = 2
    elif (zangle < 337.5):
        goalSquare = (-1, 1)
        finalHeading = 3
    print("Goal Square" + str(goalSquare))
    return goalSquare
    
   
######################## DO NOT MODIFY CODE BELOW THIS LINE ####################################


# class RobotThread(threading.Thread):
#     """Thread to run cozmo code separate from main thread
#     """
        
#     def __init__(self):
#         threading.Thread.__init__(self, daemon=True)

#     def run(self):
#         setup()


# # If run as executable, start RobotThread and launch visualizer with empty grid file
# if __name__ == "__main__":
#     global grid, stopevent
#     stopevent = threading.Event()
#     grid = CozGrid("emptygrid.json")
#     visualizer = Visualizer(grid)
#     updater = UpdateThread(visualizer)
#     updater.start()
#     robot = RobotThread()
#     robot.start()
#     visualizer.start()
#     stopevent.set()

