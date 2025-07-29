# w -> for forward
# s -> for backward
# a,d -> for rotating
import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1024, 512), pygame.RESIZABLE)

#movement
move = 0.1

#player position
px = 300
py = 300
angle = 0
dx,dy = move*math.cos(angle),move*math.sin(angle)

#map
mapX,mapY = 8,8
mapS = 64

map_ = [
    1, 1, 1, 1, 1, 1, 1, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 0, 0, 0, 1,
    1, 0, 1, 0, 1, 1, 0, 1,
    1, 0, 1, 1, 1, 0, 0, 1,
    1, 0, 0, 0, 0, 0, 0, 1,
    1, 0, 0, 0, 1, 0, 0, 1,
    1, 1, 1, 1, 1, 1, 1, 1
]

def draw_square(x,y,size,color):
    pygame.draw.rect(screen, color, (x, y, size,size))

def draw_map():
    for i in range(mapY):
        for j in range(mapX):
            if map_[mapY*i+j]:
                color = "white"
            else:
                color = "black"
            draw_square(j*mapS,i*mapS,mapS-1,color)

def distance(x1,x2,y1,y2,angle):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def drawRay():
    ray_angle = angle
    one_degree = 0.0174533 # in radian
    ray_angle = angle - one_degree*30
    if ray_angle < 0:
        ray_angle += 2*math.pi
    elif ray_angle > 2*math.pi:
        ray_angle -= 2*math.pi

    for rays in range(60):
        dist = 0
        # horizontal
        rx,ry = 0,0
        distH = 100000
        hx,hy = px,py
        x_offset = 0
        y_offset = 0
        dof = 0
        tanH = math.tan(ray_angle)
        itanH = 1/tanH
        if ray_angle == 0 or ray_angle == math.pi or ray_angle == 2*math.pi:
            dof = 8
            rx = px
            ry = py

        elif math.pi > ray_angle:
            #bottom
            y_offset = mapS
            x_offset = mapS*itanH
            ry = int(py/mapS)*mapS + mapS
            rx = px + (ry-py)*itanH


        elif ray_angle > math.pi:
            ry = int(py / mapS) * mapS - 0.0001
            rx = px + (ry - py) * itanH
            y_offset = -mapS
            x_offset = y_offset * itanH

        while dof < 8:
            mx = int(rx/mapS)
            my = int(ry/mapS)
            array_coor = my*mapX + mx
            if 0 <= mx < mapX and 0 <= my < mapY and map_[array_coor]:
                dof = 8
                hx = rx
                hy = ry
                distH = distance(hx,px,hy,py,ray_angle)
            else:
                rx += x_offset
                ry += y_offset
                dof += 1

        # <---vertical--->
        dof = 0
        rx = 0
        ry = 0
        distV = 100000
        vx,vy = px,py
        tanV = math.tan(ray_angle)

        if ray_angle > 3*math.pi/2 or ray_angle < math.pi/2:
            #right
            x_offset = mapS
            rx = int(px/mapS)*mapS + x_offset
            ry = (rx-px)*tanV + py
            y_offset = mapS*tanV

        elif math.pi/2 < ray_angle < 3*math.pi/2:
            #left
            k = int(px/mapS)*mapS
            rx = k - 0.0001
            ry = py - tanV*(px-k)
            x_offset = -mapS
            y_offset = -mapS*tanV

        else:
            dof = 8
            rx = px
            ry = py

        while dof < 8:
            mx = int(rx/mapS)
            my = int(ry/mapS)
            array_coor = my*mapX + mx
            if 0 <= mx < mapX and 0 <= my < mapY and map_[array_coor]:
                dof = 8
                vx = rx
                vy = ry
                distV = distance(vx, px, vy, py, ray_angle)
            else:
                rx += x_offset
                ry += y_offset
                dof += 1

        if distH < distV:
            rx = hx
            ry = hy
            dist = distH
            wall_color = 255 / (1 + dist * dist * 0.0001)
        else:
            rx = vx
            ry = vy
            dist = distV
            wall_color = 255 / (1 + dist * dist * 0.0001)

        pygame.draw.line(screen,"green",(px+4,py+4),(rx,ry),width=2)

        #3d drawing
        diff_angle = angle-ray_angle
        dist = dist*math.cos(diff_angle)

        line_height = (mapS*320)/dist
        if line_height > 320:
            line_height = 320
        line_o = 160-line_height/2
        # pygame.draw.line(screen,"white",(530 + rays*8,line_o),(530 + rays*8,line_height+line_o),width=8)
        pygame.draw.line(screen,(wall_color,wall_color,wall_color),(530 + rays*8,line_o),(530 + rays*8,line_height+line_o),width=8)


        ray_angle += one_degree
        if ray_angle < 0:
            ray_angle += 2 * math.pi
        elif ray_angle > 2 * math.pi:
            ray_angle -= 2 * math.pi



def draw_player():
    x_,y_ = (px+4,py+4)
    a = angle
    pygame.draw.rect(screen, "yellow", (px, py, 8, 8))
    pygame.draw.line(screen,"red",(x_,y_),(x_+10*math.cos(a),y_+10*math.sin(a)),width=2)

def display():
    draw_map()
    draw_player()
    drawRay()


key_pressed = None

def movement():
    global px,py,angle,dx,dy
    if key_pressed == "w":
        px += dx
        py += dy

    elif key_pressed == "s":
        px -= dx
        py -= dy
    elif key_pressed == "a":
        angle -= 0.001
        if angle < 0:
            angle += 2*math.pi
        dx = move*math.cos(angle)
        dy = move*math.sin(angle)
    elif key_pressed == "d":
        angle += 0.001
        if angle > 2*math.pi:
            angle -= 2*math.pi
        dx = move*math.cos(angle)
        dy = move*math.sin(angle)


running = True

while running:
    screen.fill((39, 43, 40))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                key_pressed = "w"
            elif event.key == pygame.K_s:
                key_pressed = "s"
            elif event.key == pygame.K_a:
                key_pressed = "a"
            elif event.key == pygame.K_d:
                key_pressed = "d"
        elif event.type == pygame.KEYUP:
            key_pressed = None

    movement()

    display()

    pygame.display.flip()

pygame.quit()