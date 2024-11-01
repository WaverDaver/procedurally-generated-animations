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
    #points[1][0] = distance_constraint_point_coordinate[0]
    #points[1][1] = distance_constraint_point_coordinate[1]
    print(distance_constraint_point_coordinate)

def calculating_angles(pointone,pointtwo):
    global angle_in_radians
    angle_in_radians = math.atan2(pointtwo[1]-pointone[1],pointtwo[0]-pointone[0])
    print("Angle is: " + str(angle_in_radians))
    
    
    
#VARIABLES

color = (255,200,0)

#poisition and outer radius of the point that is moved
main_point_outer_radius = 100
points = [[500,200],[400,200],[300,200],[200,200],[100,200]]
num_of_points = len(points)

all_points_radius = 20

#angle between the first and second point
angle_in_radians = 0

distance_constraint_point_x = 0
distance_constraint_point_y = 0
distance_constraint_point_coordinate = [0,0]

run = True

while run:
    #makes sure the player isn't duplicating all over the screen
    screen.fill((0,0,0))
    
    # main point
    pg.draw.circle(screen,color,points[0], all_points_radius, 1)
    
    #main point "radius" visualization
    pg.draw.circle(screen, color, points[0], main_point_outer_radius, 1)
    
    # second point
    pg.draw.circle(screen, color, points[0], all_points_radius, 1 )
    
    #vector connecting the first and second point
    pg.draw.line(screen, color, points[0],points[1])
    
    #visualizing the constraint point
    pg.draw.circle(screen, (0,255,0), (distance_constraint_point_coordinate[0], distance_constraint_point_coordinate[1]),5)
    
    #third,fourth,fifth points
    pg.draw.circle(screen,color, points[1], all_points_radius, 1 )
    pg.draw.circle(screen,color, points[2], all_points_radius, 1)
    pg.draw.circle(screen,color, points[3], all_points_radius, 1)
    
    for i in range(num_of_points - 1):
        calculating_angles(points[i],points[i+1])
        calculating_distance(points[i],points[i+1])
        calculating_distance_constraint_point(points[i])
        points[i+1][0] = distance_constraint_point_coordinate[0]
        points[i+1][1] = distance_constraint_point_coordinate[1]
        
    
    
    #calculating_distance(points[0],points[1])
    #calculating_angles(points[0],points[1])
    #calculating_distance_constraint_point(points[0])
    
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