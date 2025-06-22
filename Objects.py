import pyglet as pg
from Box2D import b2
from Tools import LoadAsset, LoadAudio
from math import degrees,sqrt

class PhysCircle(pg.shapes.Circle):
    def __init__(self,PPM, world, x,y,radius,color = (0,0,0,255), batch = None):
        super().__init__(x * PPM,y * PPM,radius * PPM,color = color, batch = batch)
        self.PPM = PPM
        
        body_def = bodyDef()
        body_def.type = dynamicBody
        body_def.position = (x,y)

        body = world.CreateBody(body_def)
        

        fixture = fixtureDef()
        fixture.shape = circleShape(radius=radius)
        fixture.density = 1
        fixture.friction = 0
        fixture.restitution = 1

        body.CreateFixture(fixture)

        self.body = body
        

    def update(self):
        self.x = self.body.position.x * self.PPM
        self.y = self.body.position.y * self.PPM

class PhysRect(pg.shapes.Rectangle):
    def __init__(self,PPM,world, x, y, w, h, color=(255, 255, 255),batch = None):
        super().__init__(x * PPM, y * PPM, w * PPM, h * PPM, color=color, batch=batch)
        self.anchor_position = (w * (PPM)/2, h * (PPM)/2)
        self.size_x = w
        self.size_y = h
        self.body = world.CreateStaticBody(position=(x, y), shapes=b2.polygonShape(box=(w / 2, h / 2)))

    def set_angle(self, deg: float, add=False):
        self.rotation = deg if not add else self.rotation + deg
        self.body.angle = -radians(self.rotation)



class Cap(pg.sprite.Sprite):
    def __init__(self, PPM, world, radius, x=0, y=0, batch=None):
        # Load and center texture
        texture = LoadAsset('assets/Cap.png')
        texture.anchor_x = texture.width // 2
        texture.anchor_y = texture.height // 2

        # Init sprite at center of physics body (scaled)
        super().__init__(texture, x=x * PPM, y=y * PPM, batch=batch)
        self.PPM = PPM

        # Scale sprite to match physics body diameter
        diameter_pixels = 2 * radius * PPM
        self.scale = diameter_pixels / texture.width

        # Create Box2D body
        body_def = b2.bodyDef()
        body_def.type = b2.dynamicBody
        body_def.position = (x, y)
        self.body = world.CreateBody(body_def)

        # Create circle fixture
        circle = b2.circleShape(radius=radius, pos=(0, 0))
        fixture = b2.fixtureDef(
            shape=circle,
            density=1.0,
            friction=1,
            restitution=0.5
        )
        self.body.CreateFixture(fixture)
        self.body.userData = 'Cap'


        self.hit_sfx = LoadAudio('assets/hit.ogg')

        self.slide_sfx = [LoadAudio(f'assets/slide{i}.ogg') for i in range(1,4)]

    def update(self):
        self.rotation = -degrees(self.body.angle)
        self.x = self.body.position.x * self.PPM
        self.y = self.body.position.y * self.PPM

    def get_velocity_len(self):
        return sqrt(self.body.linearVelocity.x**2 + self.body.linearVelocity.y**2)


class Hand(pg.sprite.Sprite):
    def __init__(self, PPM, world, x=0, y=0, batch=None):
        # Load frame images and set anchors
        self.frames = []
        for path in ['assets/Hand0.png', 'assets/Hand1.png']:
            texture = LoadAsset(path)
            texture.anchor_x = texture.width - 120
            texture.anchor_y = texture.height // 2 + 100
            self.frames.append(texture)

        # Start with the first frame (not animated yet)
        super().__init__(self.frames[0], x=x * PPM, y=y * PPM, batch=batch)

        self.PPM = PPM
        self.world = world
        self.scale = 0.2
        self.rotation = -90
        self.current_frame = 0


        sensor_shape = b2.circleShape(radius=0.5)  # size (half-width, half-height)

        fixture_def = b2.fixtureDef(
            shape=sensor_shape,
            isSensor=True
        )

        self.sensor = world.CreateStaticBody(
            position=(0,0),
            fixtures=fixture_def
        )
        

        
        

    def set_frame(self, index):
        if 0 <= index < len(self.frames):
            self.image = self.frames[index]
            self.current_frame = index

    HandFrameChangedTime = 0
    
    def update(self,delta):
        self.sensor.position.x = self.x / self.PPM*2
        self.sensor.position.y = self.y / self.PPM*2
        
        if self.HandFrameChangedTime > 0:
            self.HandFrameChangedTime -= delta

        else:
            self.set_frame(0)

        
        

def are_fixtures_overlapping(fixA, fixB):
    shapeA = fixA.shape
    shapeB = fixB.shape
    xfA = fixA.body.transform
    xfB = fixB.body.transform

    return b2.testOverlap(shapeA, 0, shapeB, 0, xfA, xfB)

        


class CapContactListener(b2.contactListener):
    def __init__(self):
        super().__init__()
        self.cap_is_hit = False

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        if bodyA.userData == "Cap" or bodyB.userData == "Cap":
            self.cap_is_hit = True

    def EndContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body

        if bodyA.userData == "Cap" or bodyB.userData == "Cap":
            self.cap_is_hit = False
        






