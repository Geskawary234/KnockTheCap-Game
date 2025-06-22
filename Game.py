from Box2D.b2 import *
import pyglet as pg
from pyglet import math
from Tools import LoadAsset
from Objects import *
from random import uniform,randint

PPM = 50

window = pg.window.Window(640, 480, 'Game', vsync=True)
window.set_mouse_visible(False)

audio_player = pg.media.Player()
sliding_player = pg.media.Player()

world = world(gravity=(0, 0))
world.contactListener = CapContactListener()

batch = pg.graphics.Batch()




        
#s1 = PhysCircle(PPM,world,0.5,0.5,1,color = (255,0,0,255),batch = batch)
wall1 = PhysRect(PPM,world,5,10,25,0.5,batch = batch)
wall2 = PhysRect(PPM,world,5,-0.5,20,0.5,batch = batch)
wall3 = PhysRect(PPM,world,-0.5,5,1,10,batch = batch)
wall4 = PhysRect(PPM,world,13.5,5,1,10,batch = batch)



cap = Cap(PPM,world,0.5,x = (window.width//2)/PPM,y = (window.height//2)/PPM,batch = batch)

def play_sfx(sfx,pitch = 1, volume = 1):
    if audio_player.playing:
        audio_player.pause()
        audio_player.seek(0)
    audio_player.queue(sfx)
    audio_player.pitch = pitch
    audio_player.volume = volume
    audio_player.play()

def play_sliding_sfx(volume):
    if not sliding_player.playing:
        sliding_player.queue(cap.slide_sfx[randint(0,len(cap.slide_sfx)-1)])
        sliding_player.volume = volume
        sliding_player.play()
        


hand = Hand(PPM=100, world=world, x=5, y=5, batch = batch)

strength = 25

@window.event
def on_draw():
    window.clear()
    #pg.shapes.Circle(hand.sensor.position.x * PPM,hand.sensor.position.y * PPM,radius = 1*PPM).draw()
    batch.draw()

    

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pg.window.mouse.LEFT and hand.HandFrameChangedTime<=0 :
        hand.set_frame(1)
        hand.HandFrameChangedTime = 0.25
        
        hand_fix = hand.sensor.fixtures[0]
        cap_fix = cap.body.fixtures[0]
        pos = (x/PPM,y/PPM)
        
        if are_fixtures_overlapping(hand_fix,cap_fix):
            direction = cap.body.position - hand.sensor.position
            direction.Normalize()
            
    
            impulse = strength * direction
            cap.body.ApplyLinearImpulse(impulse, pos, wake=True)

            play_sfx(cap.hit_sfx, pitch = uniform(0.75,1.25))
            

@window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_pos = x, y
    hand.x = x 
    hand.y = y

next_time_play = 0

def process(delta):
    world.Step(delta,10,10)
    cap.update()
    hand.update(delta)
    global next_time_play
    if next_time_play>0:
        next_time_play -= delta
    else:
    
        if world.contactListener.cap_is_hit and cap.get_velocity_len()>1:
            play_sfx(cap.hit_sfx,pitch = uniform(0.75,1.25))
            next_time_play = 0.2

        if cap.get_velocity_len()>1:
            volume = cap.get_velocity_len()/40
            play_sliding_sfx(volume)
            #play_sfx(,volume = volume)

        


def ready(delta):
    pass
    

pg.clock.schedule(process)
pg.clock.schedule_once(ready,0)


if __name__ == '__main__':
    pg.app.run()
