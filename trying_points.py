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
    #print(distance)


def calculating_distance_constraint_point(known_point):
    global distance_constraint_point_coordinate
    distance_constraint_point_x = known_point[0] + main_point_outer_radius * math.cos(angle_in_radians)
    distance_constraint_point_y = known_point[1] + main_point_outer_radius * math.sin(angle_in_radians)
    distance_constraint_point_coordinate[0] = distance_constraint_point_x
    distance_constraint_point_coordinate[1] = distance_constraint_point_y
    #print(distance_constraint_point_coordinate)

def calculating_angles(pointone,pointtwo):
    global angle_in_radians
    angle_in_radians = math.atan2(pointtwo[1]-pointone[1],pointtwo[0]-pointone[0])
    #print("Angle is: " + str(angle_in_radians))


def parametric_equation(point, radius):
    global first_parametric_x, first_parametric_y, second_parametric_x, second_parametric_y
    global left_parametric_eyes_x, left_parametric_eyes_y, right_parametric_eyes_x, right_parametric_eyes_y
    first_parametric_x = point[0] + radius * math.cos(angle_in_radians - 1.5708)
    first_parametric_y = point[1] + radius * math.sin(angle_in_radians - 1.5708)
    
    second_parametric_x = point[0] + radius * math.cos(angle_in_radians + 1.5708)
    second_parametric_y = point[1] + radius * math.sin(angle_in_radians  + 1.5708)
    
    eye_radius = radius - 10
    #for only the eyes
    left_parametric_eyes_x = point[0] + eye_radius * math.cos(angle_in_radians - 1.5708)
    left_parametric_eyes_y = point[1] + eye_radius * math.sin(angle_in_radians - 1.5708)
    
    right_parametric_eyes_x = point[0] + eye_radius * math.cos(angle_in_radians + 1.5708)
    right_parametric_eyes_y = point[1] + eye_radius * math.sin(angle_in_radians  + 1.5708)
    
    all_first_parametric_points.append([first_parametric_x, first_parametric_y])
    all_second_parametric_points.append([second_parametric_x,second_parametric_y]) 
    #print(all_first_parametric_points)   
    
    
#VARIABLES

#points at the sides of each body part, this can be used to render the body
first_parametric_x = 0
first_parametric_y = 0
second_parametric_x = 0
second_parametric_y = 0

left_parametric_eyes_x = 0
left_parametric_eyes_y = 0
right_parametric_eyes_x = 0
right_parametric_eyes_y = 0

all_first_parametric_points = []
all_second_parametric_points = []

color = (255,200,0)
fps = 60

#this controls how far each body "part"/segment is from each other
main_point_outer_radius = 15

#NOTE TO SELF, CREATE A LOT MORE POINTS TO MAKE THE SNAKE SMOOTHER

#body segment positions and body widths
points = [[500,200],[400,200],[300,200],[200,200],[100,200], [0,200], [0,0], [0,1], [0,2], [0,5],[0,6]]
radius_list = [35,37,37,33,33,32,31,30,29,28,27]
#the second and third radiuses are bigger to make the head more outlined

num_of_points = len(points)

#angle between the first and second point
angle_in_radians = 0

distance_constraint_point_x = 0
distance_constraint_point_y = 0
distance_constraint_point_coordinate = [0,0]

#movement

xspeed = 2
yspeed = 2

run = True

#button to make the snake longer

button = pg.Rect(600,0,200,80)
button_color = (0,0,155)



while run:
    #makes sure the player isn't duplicating all over the screen
    screen.fill((42, 44, 53))
    pg.time.Clock().tick(fps)
    
    #main point "radius" visualization
    pg.draw.circle(screen, color, points[0], main_point_outer_radius, 1)
    
    #vector connecting the first and second point
    pg.draw.line(screen, color, points[0],points[1])
    
    #DRAWING ALL THE POINTS
    #for i in range(num_of_points-1):
        #pg.draw.circle(screen, color, points[i], radius_list[i], 1)
    
    #makes sure the list is empty so that it doesn't pile up and try to draw the sides of the body on old positions
    all_second_parametric_points.clear()
    all_first_parametric_points.clear()
    
    
    #MAKES THE ENTIRE CHAIN CONNECTED AND FOLLOW THE MAIN POINT
    #loops through the points list, and makes sure each point is connected to the point behind it
    for i in range(num_of_points - 1):
        num_of_points = len(points)
        calculating_angles(points[i],points[i+1])
        calculating_distance(points[i],points[i+1])
        calculating_distance_constraint_point(points[i])
        points[i+1][0] = distance_constraint_point_coordinate[0]
        points[i+1][1] = distance_constraint_point_coordinate[1]
        
        #this is what draws the lines connecting the parametric points to form an actual body
        parametric_equation(points[i],radius_list[i])
        
        #these two circles show the parametric points that are used to draw the polygon
        #pg.draw.circle(screen, (255,0,0), [first_parametric_x,first_parametric_y], 5, 1)
        #pg.draw.circle(screen, (255,0,0),[second_parametric_x,second_parametric_y], 5, 1)
        
        #drawing the eyes by using the very first parametric points calculated
        if i == 0:
            pg.draw.circle(screen, (58,124,165), points[0], radius_list[0], 100)
            pg.draw.circle(screen, (255,255,255), [left_parametric_eyes_x,left_parametric_eyes_y], 5, 100)
            pg.draw.circle(screen, (255,255,255),[right_parametric_eyes_x,right_parametric_eyes_y], 5, 100)
           
        
        #these two lines show the lines connecting in between the parametric points for each side of the body
        #pg.draw.line(screen,(255,0,0), (int(all_first_parametric_points[i - 1][0]), int(all_first_parametric_points[i - 1][1])), 
         #            (int(all_first_parametric_points[i][0]), int(all_first_parametric_points[i][1])), width=1   )
        #pg.draw.line(screen,(255,0,0), (int(all_second_parametric_points[i - 1][0]), int(all_second_parametric_points[i - 1][1])), 
            #         (int(all_second_parametric_points[i][0]), int(all_second_parametric_points[i][1])), width=1   )
        pg.draw.polygon(screen, (58,124,165), [(all_first_parametric_points[i-1][0], all_first_parametric_points[i-1][1]),
                            (all_second_parametric_points[i-1][0], all_second_parametric_points[i-1][1]),
                            (all_second_parametric_points[i][0], all_second_parametric_points[i][1]),
                            (all_first_parametric_points[i][0], all_first_parametric_points[i][1])])
        pg.draw.rect(screen, button_color, button)
    
    
    #button text
    font = pg.font.Font(None, 36)
    button_text = font.render("LONGER SNAKE", True, (255,255,255))
    button_rect = button_text.get_rect(center=button.center)
    screen.blit(button_text, button_rect)
    
    
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
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                points.append([0,1])
                latest_in_radius_list = radius_list[-1]
                last_minus_one = latest_in_radius_list - 1
                if last_minus_one < 5:
                    last_minus_one = 5
                radius_list.append(last_minus_one)
                button_color = (255,0,0)
                print(points)
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