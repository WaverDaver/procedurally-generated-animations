import pygame as pg 
import math

pg.init()

screen_width = 800
screen_height = 600

screen = pg.display.set_mode((screen_width,screen_height))

#distance is calculated from one center to the other
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
    second_point_position[0] = distance_constraint_point_coordinate[0]
    second_point_position[1] = distance_constraint_point_coordinate[1]
    print(distance_constraint_point_coordinate)

def calculating_angles(pointone,pointtwo):
    global angle_in_radians
    angle_in_radians = math.atan2(pointtwo[1]-pointone[1],pointtwo[0]-pointone[0])
    print("Angle is: " + str(angle_in_radians))
    
    
    


color = (255,200,0)

#poisition and outer radius of the point that is moved
main_point_position = [400,300]
main_point_outer_radius = 100

second_point_position = [300,200]

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
    pg.draw.circle(screen,color,main_point_position, all_points_radius, 1)
    
    #main point "radius" visualization
    pg.draw.circle(screen, color, main_point_position, main_point_outer_radius, 1)
    
    # second point
    pg.draw.circle(screen, color, second_point_position, all_points_radius, 1 )
    
    #vector connecting the first and second point
    pg.draw.line(screen, color, main_point_position,second_point_position)
    
    #visualizing the constraint point
    pg.draw.circle(screen, (0,255,0), (distance_constraint_point_coordinate[0], distance_constraint_point_coordinate[1]),5)
    
    calculating_distance(main_point_position,second_point_position)
    calculating_angles(main_point_position,second_point_position)
    calculating_distance_constraint_point(main_point_position)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        keys = pg.key.get_pressed()
        
        #movement of the main point to check the constraint point
        if keys[pg.K_LEFT]:
            main_point_position[0] = main_point_position[0] - 20
        
        if keys[pg.K_RIGHT]:
            main_point_position[0] = main_point_position[0] + 20
        
        if keys[pg.K_UP]:
            main_point_position[1] = main_point_position[1] - 20
        
        if keys[pg.K_DOWN]:
            main_point_position[1] = main_point_position[1] + 20
            
    
    pg.display.update()



pg.quit()