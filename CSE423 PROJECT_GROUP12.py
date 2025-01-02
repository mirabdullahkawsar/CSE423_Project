from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time
W_Width, W_Height = 500,500
station_width = 30
station_height = 60
speed = 0.75
solar_x = 0
solar_y = 0
pause = False
planet_angles = {
    "planet1": 0,
    "planet2": 0,  
    "planet3": 0,  
    "planet4": 0,  
    "planet5": 0,  
    "planet6": 0  
}
explosion_radius = 10  
show_nebula = False
show_black_hole = False
show_meteor_shower = False
def circ_point(x, y, a, b):      
    glVertex2f(a + x, b + y)
    glVertex2f(a + y, b + x)
    glVertex2f(a + y, b - x)
    glVertex2f(a + x, b - y)
    glVertex2f(a - x, b - y)
    glVertex2f(a - y, b - x)
    glVertex2f(a - y, b + x)
    glVertex2f(a - x, b + y)
def midCircle(radius, a, b):    
    d = 1 - radius
    x = 0
    y = radius
    glBegin(GL_POINTS)
    circ_point(x, y, a, b)
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * x - 2 * y + 5
            y -= 1
        x += 1      
        circ_point(x, y, a, b)
    glEnd()
def midCirc(radius, a, b):
    num_segments = 100
    angle = 0
    glBegin(GL_POLYGON) 
    for _ in range(num_segments):
        x = a + radius * math.cos(angle)
        y = b + radius * math.sin(angle)
        glVertex2f(x, y)
        angle += 2.0 * math.pi / num_segments
    glEnd()
def draw_station(radius, x, y):  
    def draw_point(x, y):
        glVertex2f(x, y)   
    def draw_midpoint_line(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        d = 2 * dy - dx
        C = 2 * dy
        C = 2 * (dy - dx)
        x, y = x1, y1
        draw_point(x, y)
        while x < x2:
            if d <= 0:
                d += C
            else:
                d += C
                y += 1
            x += 1
            draw_point(x, y)
    glColor3f(0.5, 0.5, 0.5) 
    glBegin(GL_POINTS)
    for i in range(int(x), int(x + station_width + 1)):
        for j in range(int(y), int(y + station_height + 1)):
            draw_point(i, j)
    glEnd()
    glColor3f(0.8, 0.8, 0.8) 
    midCirc(8, x + station_width / 2, y + station_height / 2)
def draw_solar():  
    glColor3f(1.0, 1.0,1.0)
    glPointSize(3.0)
    midCircle(100, 200+ solar_x, 200 + solar_y)
    midCircle(200, 200+ solar_x, 200 + solar_y)
    midCircle(300, 200+ solar_x, 200 + solar_y)
    midCircle(400, 200+ solar_x, 200 + solar_y)
    midCircle(500, 200+ solar_x, 200 + solar_y)
    midCircle(600, 200+ solar_x, 200 + solar_y)
def draw_sun():
    glColor3f(1.0, 1.0, 0.0)  
    midCirc(50, 200 + solar_x, 200 + solar_y)

    glColor3f(1.0, 1.0, 0.5)  
    midCirc(60, 200 + solar_x, 200 + solar_y)

    glColor3f(1.0, 1.0, 1.0) 
    midCirc(70, 200 + solar_x, 200 + solar_y)
def draw_sun_corona():
    glColor3f(1.0, 0.8, 0.0) 
    glLineWidth(3)
    num_segments = 100
    angle = 0
    glBegin(GL_LINE_LOOP)

    for _ in range(num_segments):
        x = 200 + solar_x + 80 * math.cos(angle)
        y = 200 + solar_y + 80 * math.sin(angle)
        glVertex2f(x, y)
        angle += 2.0 * math.pi / num_segments
    glEnd()
    glLineWidth(1)

def update_solar_center():              
    global solar_x , solar_y
    solar_x -= speed
    solar_y += speed
    if solar_x < -W_Width / 2:
        solar_x = W_Width / 2 + solar_x
    if solar_y >W_Width / 2:
        solar_y = -W_Width / 2 + solar_y
def draw_sunspots():
    glColor3f(0.3, 0.3, 0.3) 
    num_spots = random.randint(3, 6)  
    for _ in range(num_spots):
        spot_x = random.uniform(200 + solar_x - 50, 200 + solar_x + 50)
        spot_y = random.uniform(200 + solar_y - 50, 200 + solar_y + 50)
        spot_size = random.uniform(5, 10)
        midCirc(spot_size, spot_x, spot_y)
sun_size_factor = 1.0 
def pulse_sun():
    global sun_size_factor
    sun_size_factor += 0.005 * math.sin(glutGet(GLUT_ELAPSED_TIME) / 1000.0) 
    if sun_size_factor < 0.8: sun_size_factor = 0.8 
    if sun_size_factor > 1.2: sun_size_factor = 1.2 
def draw_pulsing_sun():
    global sun_size_factor
    glColor3f(1.0, 1.0, 0.0) 
    midCirc(50 * sun_size_factor, 200 + solar_x, 200 + solar_y)
def draw_sun_halo():
    glColor3f(1.0, 0.9, 0.0) 
    glLineWidth(1)
    num_segments = 100
    angle = 0
    glBegin(GL_LINE_LOOP)
    for _ in range(num_segments):
        x = 200 + solar_x + 100 * math.cos(angle)
        y = 200 + solar_y + 100 * math.sin(angle)
        glVertex2f(x, y)
        angle += 2.0 * math.pi / num_segments
    glEnd()
def draw_twinkling_stars(num_stars):
    for _ in range(num_stars):
        x = random.uniform(-W_Width / 2, W_Width / 2)
        y = random.uniform(-W_Height / 2, W_Height / 2)
        size = random.uniform(1, 3)
        brightness = random.uniform(0.5, 1.0)
        glColor3f(brightness, brightness, brightness) 
        draw_star(x, y, size, [brightness, brightness, brightness])
def draw_star(x, y, size, color):
    glColor3f(color[0], color[1], color[2])  
    glPointSize(size)  
    glBegin(GL_POINTS)
    glVertex2f(x, y)  
    glEnd()
def draw_sun():  
    glColor3f(1.0, 1.0, 0.0)  
    midCirc(50, 200 + solar_x, 200 + solar_y)
def draw_asteroid_belt():
    num_asteroids = 100
    orbit_radius = 350  
    for _ in range(num_asteroids):
        angle = random.uniform(0, 360)
        angle_rad = math.radians(angle)
        x = 200 + orbit_radius * math.cos(angle_rad)
        y = 200 + orbit_radius * math.sin(angle_rad)
        glColor3f(0.8, 0.7, 0.8) 
        midCirc(3, x, y)  
comet_angle = 0  
comet_distance = 700  
def draw_comet():
    global comet_angle
    angle_rad = math.radians(comet_angle)
    x = 200 + comet_distance * math.cos(angle_rad)
    y = 200 + comet_distance * math.sin(angle_rad)
    glColor3f(1.0, 0.8, 0.0) 
    midCirc(10, x, y)
    glBegin(GL_LINES)
    for i in range(5): 
        glColor3f(1.0, 0.5, 0.0) 
        glVertex2f(x - i * 15 * math.cos(angle_rad), y - i * 15 * math.sin(angle_rad))
        glVertex2f(x - (i + 1) * 15 * math.cos(angle_rad), y - (i + 1) * 15 * math.sin(angle_rad))
    glEnd()
def update_comet():
    global comet_angle
    comet_angle += 0.2  
    if comet_angle >= 360:
        comet_angle -= 360
def update_planet_rotation():
    global planet_angles
    planet_angles["planet1"] += 1  
    planet_angles["planet2"] += 0.5  
    planet_angles["planet3"] += 0.3 
    planet_angles["planet4"] += 0.2  
    planet_angles["planet5"] += 0.1  
    planet_angles["planet6"] += 0.05  
    for key in planet_angles:
        if planet_angles[key] >= 360:
            planet_angles[key] -= 360
def draw_planet():
    planets = [
        {"radius": 20, "distance": 100, "color": (0.5, 0.5, 0.5), "angle_key": "planet1"},
        {"radius": 30, "distance": 200, "color": (1.0, 0.0, 1.0), "angle_key": "planet2"},
        {"radius": 50, "distance": 300, "color": (0.0, 1.0, 0.0), "angle_key": "planet3"},
        {"radius": 40, "distance": 400, "color": (0.0, 0.0, 1.0), "angle_key": "planet4"},
        {"radius": 60, "distance": 500, "color": (1.0, 0.0, 0.0), "angle_key": "planet5"},
        {"radius": 30, "distance": 600, "color": (0.0, 1.0, 1.0), "angle_key": "planet6"},
    ]
    for planet in planets:
        angle_rad = math.radians(planet_angles[planet["angle_key"]])
        x = 200 + solar_x + planet["distance"] * math.cos(angle_rad)
        y = 200 + solar_y + planet["distance"] * math.sin(angle_rad)
        glColor3f(*planet["color"])
        midCirc(planet["radius"], x, y)
def draw_stars(num_stars):
    global zoom_factor
    star_area_factor = 20 
    glPointSize(2)  
    glBegin(GL_POINTS)
    for _ in range(num_stars):
        x = random.uniform(-W_Width * star_area_factor, W_Width * star_area_factor)
        y = random.uniform(-W_Height * star_area_factor, W_Height * star_area_factor)
        color_intensity = random.uniform(0.5, 1.0) 
        glColor3f(color_intensity, color_intensity, color_intensity)  
        glVertex2f(x, y)
    glEnd()
def draw_meteor_shower(num_meteors):
    glColor3f(0.8, 0.8, 0.8) 
    glBegin(GL_POINTS)
    for _ in range(num_meteors):
        x = random.uniform(-W_Width, W_Width)
        y = random.uniform(W_Height / 2, W_Height)  
        glVertex2f(x, y)
    glEnd()
def draw_nebula(center_x, center_y, size, density):
    glColor4f(0.5, 0.3, 0.7, 0.7) 
    glBegin(GL_POINTS)
    for _ in range(density):
        x = random.uniform(center_x - size, center_x + size)
        y = random.uniform(center_y - size, center_y + size)
        glVertex2f(x, y)
    glEnd()
def draw_spiral_galaxy(center_x, center_y, arms, num_points):
    glColor3f(0.7, 0.7, 1.0) 
    glBegin(GL_POINTS)
    for _ in range(num_points):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, 200)
        arm_offset = (2 * math.pi / arms) * (radius / 200)
        x = center_x + (radius * math.cos(angle + arm_offset))
        y = center_y + (radius * math.sin(angle + arm_offset))
        glVertex2f(x, y)
    glEnd()
def draw_space_dust(num_particles):
    glColor3f(0.6, 0.6, 0.6)  
    glBegin(GL_POINTS)
    for _ in range(num_particles):
        x = random.uniform(-W_Width * 2, W_Width * 2) 
        y = random.uniform(-W_Height * 2, W_Height * 2)
        glVertex2f(x, y)
    glEnd()
def draw_pulsar(center_x, center_y, base_radius, pulse_amplitude):
    elapsed_time = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    radius = base_radius + pulse_amplitude * math.sin(elapsed_time * 2 * math.pi)
    glColor3f(1.0, 1.0, 0.0)  
    glBegin(GL_POINTS)
    for _ in range(500):
        angle = random.uniform(0, 2 * math.pi)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()
def draw_black_hole(center_x, center_y, core_radius, event_horizon_radius, density):
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_POINTS)
    for _ in range(density):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(core_radius, event_horizon_radius)
        x = center_x + distance * math.cos(angle)
        y = center_y + distance * math.sin(angle)
        glVertex2f(x, y)
    glEnd()
cluster_x, cluster_y = 0, 0 
def update_cluster_position():
    global cluster_x, cluster_y
    cluster_x += random.uniform(-1, 1)
    cluster_y += random.uniform(-1, 1)
def draw_moving_star_cluster(num_stars, cluster_x, cluster_y):
    glColor3f(1.0, 1.0, 1.0) 
    glBegin(GL_POINTS)
    for _ in range(num_stars):
        x = cluster_x + random.uniform(-50, 50)
        y = cluster_y + random.uniform(-50, 50)
        glVertex2f(x, y)
    glEnd()
def draw_supernova(center_x, center_y, num_particles, explosion_radius):
    glColor3f(1.0, 0.5, 0.0)
    glBegin(GL_POINTS)
    for _ in range(num_particles):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, explosion_radius)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()
def keyboardListener(key, x, y):
    global pause
    if key == b' ':
        pause = not pause 
    glutPostRedisplay()
zoom_factor = 1.0  
def mouseListener(button, state, x, y):  
    global speed, zoom_factor
    if button == GLUT_LEFT_BUTTON: 
        if state == GLUT_DOWN:
            speed -= 2 
    elif button == GLUT_RIGHT_BUTTON: 
        if state == GLUT_DOWN:
            speed += 2  
    if button == 3: 
        zoom_factor *= 1.1  
    elif button == 4: 
        zoom_factor /= 1.1  
    if zoom_factor < 0.1:
        zoom_factor = 0.1
    elif zoom_factor > 5.0:
        zoom_factor = 5.0
    glutPostRedisplay()
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200 / zoom_factor, 0, 0, 0, 0, 1, 0) 
    draw_solar()
    draw_sun()
    draw_stars(5000)  
    draw_planet()
    draw_asteroid_belt()
    draw_comet()
    draw_sun_corona()
    draw_sunspots()
    draw_pulsing_sun()
    draw_sun_halo()
    draw_twinkling_stars(10)
    draw_meteor_shower(150) 
    draw_nebula(0, 0, 100, 200) 
    draw_spiral_galaxy(0, 0, 4, 1000) 
    draw_space_dust(100)  
    draw_pulsar(-150, 150, 20, 10) 
    draw_black_hole(250, -250, 10, 50, 200) 
    draw_moving_star_cluster(100, cluster_x, cluster_y)  
    draw_supernova(-300, 300, 300, explosion_radius)  
    draw_station(15, 20 + solar_x, 40 + solar_y)  
    glutSwapBuffers()
def animate():
    global speed, explosion_radius,pause
    if not pause:
        update_solar_center()
        update_planet_rotation()
        pulse_sun()        
        explosion_radius += 0.5
        if explosion_radius > 200: 
            explosion_radius = 10
    update_comet()
    glutPostRedisplay()   
def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(104,	1,	1,	1000.0)
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 
wind = glutCreateWindow(b"Solar System")
init()
glutDisplayFunc(display)	
glutIdleFunc(animate)	
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()