import numpy as np
import pygame
import datetime
import math
from pygame.locals import (MOUSEBUTTONDOWN, KEYDOWN, K_b, K_p, K_SPACE, K_RETURN, K_UP, K_DOWN)
from numpy import cfloat
i=1j

def f(numbers, numbers_0):
    a_0=numbers_0[0]
    b_0=numbers_0[1]
    a=numbers[0]
    b=numbers[1]
    temp_a=((a**2)-(b**2))+a_0
    temp_b=(2*a*b)+b_0
    a=temp_a
    b=temp_b
    numbers[0]=a
    numbers[1]=b
    return numbers

def save(screen):
    start=datetime.datetime.now()
    print(start)
    string=""
    for i in str(start):
        if i not in "- :.":
            string+=i
    print(string)
    filename="C:\\Users\\frase\\Documents\\mdlbrt\\"+"mdlbrt-"+string+".png"
    pygame.image.save(screen,filename)
    
def play_ding():
    pygame.init()
    pygame.mixer.init()
    ding="C:\\Users\\frase\\Documents\\microwave--small--timer--click--ding-6-sound-effect-54321290.wav"
    pygame.mixer.music.load(ding)
    pygame.mixer.music.play()

def colour(i,palette):
    rainbow=[(148,0,211),(0,0,255),(0,255,0),(255,255,0),(255,127,0),(255,0,0)]
    rgb=[(255,255,0),(255,0,255),(0,255,255)]
    trans = [(85,205,252),(247,120,184),(255,255,255),(247,120,184),(85,205,252)]
    if palette==0:
        return trans[i%5] #Rainbow
    if palette==1:
        return (((10*i)%255),((10*i)%255),((10*i)%255)) #White to Black
    if palette==2:
        return ((10*i)%255,0,0) #Red
    if palette==3:
        return (0,(10*i)%255,0) #Green
    if palette==4:
        return (0,0,(10*i)%255) #Blue
    if palette==5:
        if (i%2)==1:
            return (0,0,0)
        if (i%2)==0:
            return(255,255,255)
    if palette==6:
        i=i*0.03
        return (np.floor(255*np.sin(i)**2),np.floor(255*np.sin(i+(1/3)*np.pi)**2),np.floor(255*np.sin(i+(2/3)*np.pi)**2))
    if palette==7:
        return rgb[i%3]
        


def draw_set(width, height, colour_array, palette):
    draw_start=datetime.datetime.now()
    screen.fill((0,0,0))
    for x in range(2*width):
        for y in range(2*height):
            index=colour_array[x][y]
            screen.set_at((x,y),colour(index, palette))
            #if numbers_bool[x][y]:
                            #screen.set_at((x,y),(0,0,0))
    #play_ding()
    pygame.display.flip()

    draw_time=datetime.datetime.now()-draw_start
    print("Drawing:"+str(draw_time))
    print("")

def draw_rectangle(screen, posx, posy):
    pygame.draw.rect(screen, (255,255,255), (posx-(math.floor(width/10)),posy-(math.floor(height/10)),width/5,height/5),1)
    pygame.display.flip()

def gen_colour_array(width, height, zoom, a_offset, b_offset):
    calc_start=datetime.datetime.now()

    coords=np.mgrid[-width:width,-height:height]
    numbers_0=coords*zoom
    numbers_0[0]=numbers_0[0]+a_offset
    numbers_0[1]=numbers_0[1]+b_offset
    numbers=np.zeros(numbers_0.shape)
    numbers_bool=(numbers[0]**2+numbers[1]**2)<=4

    colour_array=np.zeros(coords[0].shape,dtype=int)
    old_bool=np.ones(numbers.shape,dtype=bool)

    runs=0
    
    while True: #and i in range(1000):
        pygame.event.get()
        if True not in numbers_bool:
            break        
        if False in numbers_bool:            
            if np.array_equal(numbers_bool, old_bool) and runs>2:
                colour_array=colour_array+numbers_bool
                break            
            colour_array=colour_array+numbers_bool
        runs+=1        
        old_bool=numbers_bool
        numbers=f(numbers, numbers_0)
        numbers_bool=(numbers[0]**2+numbers[1]**2)<=4
        
    calc_time=datetime.datetime.now()-calc_start
    print("Iterations:"+str(np.amax(colour_array)))
    print("Calculations:"+str(calc_time))
    return colour_array
################################################################################################### 
#width=500
#height=300
width=300 #HALF OF WIDTH/HEIGHT
height=300 #GRID IS 2*WIDTH+1 BY 2*HEIGHT+1
screen=pygame.display.set_mode([width*2,height*2])
a_offset=-0.75
b_offset=0
zoom=0.35/100
palette=3

colour_array=gen_colour_array(width, height, zoom, a_offset, b_offset)

draw_set(width, height, colour_array,palette)

print(str(a_offset)+" + "+str(b_offset)+" i")
print("")
print("Click on image to zoom in (x10)")

while True:
    
    coords=np.mgrid[-width:width,-height:height]
    numbers_0=coords*zoom
    numbers_0[0]=numbers_0[0]+a_offset
    numbers_0[1]=numbers_0[1]+b_offset

    event= pygame.event.wait()
    if event.type==MOUSEBUTTONDOWN :
        #screen.fill((0,0,0))
        mouse_pos=pygame.mouse.get_pos()
        posx=mouse_pos[0]
        posy=mouse_pos[1]
        draw_rectangle(screen, posx, posy)
        print("")
        print("Zooming in on point:")
        print(str(numbers_0[0][posx][posy])+" + "+str(numbers_0[1][posx][posy])+" i")
        a_offset=numbers_0[0][posx][posy]
        b_offset=numbers_0[1][posx][posy]
        zoom=zoom/10
        colour_array=gen_colour_array(width, height, zoom, a_offset, b_offset)
        draw_set(width, height, colour_array, palette)
        print("")
    if event.type==KEYDOWN:
        if event.key in (K_b, K_DOWN):
            print("Zooming out...")
            zoom=zoom*10
            colour_array=gen_colour_array(width, height, zoom, a_offset, b_offset)
            draw_set(width, height, colour_array, palette)
            print("")

        if event.key==K_UP:
            print("Zooming in...")
            zoom=zoom/10
            colour_array=gen_colour_array(width, height, zoom, a_offset, b_offset)
            draw_set(width, height, colour_array, palette)

        if event.key==K_p:
            palette=(palette+1)%8
            print("Changing palette...")
            draw_set(width, height, colour_array, palette)

        if event.key==K_SPACE:
            print("Drawing only points in the set...")
            maximum=np.amax(colour_array)
            m_set=colour_array==maximum
            screen.fill((0,0,0))
            for x in range(2*width):
                for y in range(2*height):
                    if m_set[x][y]:
                        screen.set_at((x,y),(255,255,255))
            pygame.display.flip()
            
        if event.key==K_RETURN:
            save(screen)
    




    
