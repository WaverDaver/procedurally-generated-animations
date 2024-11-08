import pygame as pg 
import math

pg.init()

screen_width = 800
screen_height = 600

screen = pg.display.set_mode((screen_width,screen_height))

#distance is calculated from one center to the other, THIS ISN'T NEEDED, JUST CALCULATING FOR CURIOSITY
distance = 0
def calculating_distance(pointone, pointtwo):
    global distance
    distance = math.sqrt((pointtwo[0]-pointone[0])**2 + (pointtwo[1]-pointone[1])**2)
    print(distance)


def calculating_distance_constraint_point(known_point):
    global distance_constraint_point_coordinate
    distance_constraint_point_x = known_point[0] + main_point_outer_radius * math.cos(angle_in_radians)
    distance_constraint_point_y = known_point[1] + main_point_outer_radius * math.sin(angle_in_radians)
    distance_constraint_point_coordinate[0] = distance_constraint_point_x
    distance_constraint_point_coordinate[1] = distance_constraint_point_y
    print(distance_constraint_point_coordinate)

def calculating_angles(pointone,pointtwo):
    global angle_in_radians
    angle_in_radians = math.atan2(pointtwo[1]-pointone[1],pointtwo[0]-pointone[0])
    print("Angle is: " + str(angle_in_radians))


def parametric_equation(point):
    global first_parametric_x, first_parametric_y, second_parametric_x, second_parametric_y
    first_parametric_x = point[0] + all_points_radius * math.cos(angle_in_radians - 1.5708)
    first_parametric_y = point[1] + all_points_radius * math.sin(angle_in_radians - 1.5708)
    
    second_parametric_x = point[0] + all_points_radius * math.cos(angle_in_radians + 1.5708)
    second_parametric_y = point[1] + all_points_radius * math.sin(angle_in_radians  + 1.5708)
    
    all_first_parametric_points.append([first_parametric_x, first_parametric_y])
    all_second_parametric_points.append([second_parametric_x,second_parametric_y]) 
    print(all_first_parametric_points)   
    
    
#VARIABLES

#points at the sides of each body part, this can be used to render the body
first_parametric_x = 0
first_parametric_y = 0
second_parametric_x = 0
second_parametric_y = 0

all_first_parametric_points = []
all_second_parametric_points = []

color = (255,200,0)
fps = 60

#poisition and outer radius of the point that is moved
main_point_outer_radius = 100
points = [[500,200],[400,200],[300,200],[200,200],[100,200], [0,200]]
num_of_points = len(points)

all_points_radius = 20

#angle between the first and second point
angle_in_radians = 0

distance_constraint_point_x = 0
distance_constraint_point_y = 0
distance_constraint_point_coordinate = [0,0]

#movement

xspeed = 2
yspeed = 2

run = True


while run:
    #makes sure the player isn't duplicating all over the screen
    screen.fill((42, 44, 53))
    pg.time.Clock().tick(fps)
    
    # main point
    pg.draw.circle(screen,color,points[0], all_points_radius, 1)
    
    #main point "radius" visualization
    pg.draw.circle(screen, color, points[0], main_point_outer_radius, 1)
    
    # second point
    pg.draw.circle(screen, color, points[1], all_points_radius, 1 )
    
    #vector connecting the first and second point
    pg.draw.line(screen, color, points[0],points[1])
    
    #visualizing the constraint point
    pg.draw.circle(screen, (0,255,0), (distance_constraint_point_coordinate[0], distance_constraint_point_coordinate[1]),5)
    
    #third,fourth,fifth, sixth points
    pg.draw.circle(screen,color, points[2], all_points_radius, 1)
    pg.draw.circle(screen,color, points[3], all_points_radius, 1)
    pg.draw.circle(screen,color, points[4], all_points_radius, 1)
    #pg.draw.circle(screen,color, points[5], all_points_radius, 1)
    
    #makes sure the list is empty so that it doesn't pile up and try to draw the sides of the body on old positions
    all_second_parametric_points.clear()
    all_first_parametric_points.clear()
    
    
    #MAKES THE ENTIRE CHAIN CONNECTED AND FOLLOW THE MAIN POINT
    #loops through the points list, and makes sure each point is connected to the point behind it
    for i in range(num_of_points - 1):
        
        calculating_angles(points[i],points[i+1])
        calculating_distance(points[i],points[i+1])
        calculating_distance_constraint_point(points[i])
        points[i+1][0] = distance_constraint_point_coordinate[0]
        points[i+1][1] = distance_constraint_point_coordinate[1]
        
        #this is what draws the lines connecting the parametric points to form an actual body
        parametric_equation(points[i])
        pg.draw.circle(screen, (255,0,0), [first_parametric_x,first_parametric_y], 5, 1)
        pg.draw.circle(screen, (255,0,0),[second_parametric_x,second_parametric_y], 5, 1)
        pg.draw.line(screen,(255,0,0), (int(all_first_parametric_points[i - 1][0]), int(all_first_parametric_points[i - 1][1])), 
                     (int(all_first_parametric_points[i][0]), int(all_first_parametric_points[i][1])), width=1   )
        pg.draw.line(screen,(255,0,0), (int(all_second_parametric_points[i - 1][0]), int(all_second_parametric_points[i - 1][1])), 
                     (int(all_second_parametric_points[i][0]), int(all_second_parametric_points[i][1])), width=1   )
        if i > 0:
            pg.draw.polygon(screen, (0,255,0), [(all_first_parametric_points[i][0], all_first_parametric_points[i][1]),
                            (all_second_parametric_points[i][0], all_second_parametric_points[i][1]),
                            (all_second_parametric_points[i-1][0], all_second_parametric_points[i-1][1]),
                            (all_first_parametric_points[i-1][0], all_first_parametric_points[i-1][1])])
    
    points[0][0] += xspeed
    points[0][1] += yspeed
    
    if points[0][0] == 800:
        xspeed = -2
    
    if points[0][1] == 600:
        yspeed = -2
        
    if points[0][0] == 0:
        xspeed = 2
    
    if points[0][1] == 0:
        yspeed = 2
        
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        keys = pg.key.get_pressed()
        
        #movement of the main point to check the constraint point
        if keys[pg.K_LEFT]:
            points[0][0] = points[0][0] - 20
        
        if keys[pg.K_RIGHT]:
            points[0][0] = points[0][0] + 20
        
        if keys[pg.K_UP]:
            points[0][1] = points[0][1] - 20
        
        if keys[pg.K_DOWN]:
            points[0][1] = points[0][1] + 20
            
    
    pg.display.update()



pg.quit()