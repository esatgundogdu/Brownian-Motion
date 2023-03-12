import pygame
import math, random
import threading, time

class Brownian:
    def __init__(self):
        self.engine = _Engine(self.onCollision)

        self.rotateThread = threading.Thread(target=self.randomRotate)

        self.robot_v = 1.5
        self.robot_w = 1.5

    def start(self):
        self.engine.robot.v = self.robot_v
        self.engine.start()

    def onCollision(self):
        self.rotateThread.start() 
        self.rotateThread = threading.Thread(target=self.randomRotate)

    def randomRotate(self):
        self.engine.robot.v = 0.0
        time.sleep(0.1)
        self.engine.robot.w = self.robot_w

        # math.pi / w = max_time
        x = random.uniform(0, 2*math.pi/self.robot_w)
        t = time.time()
        
        while time.time() - t < x:
            pass
        self.engine.robot.w = 0.0
        self.engine.robot.v = self.robot_v


class _Engine:
    def __init__(self, collisionCall):
        self.FPS = 60
        self.PIXEL_PER_METER = 40
        self.size = self.WIDTH, self.HEIGHT = 640, 480

        pygame.display.set_caption("Brownian Motion")
        self.screen = pygame.display.set_mode(self.size)

        self.collisionCall = collisionCall

        self.robot = _Robot(self.WIDTH/2, self.HEIGHT/2)

        self.clock = pygame.time.Clock()
        self.done = False

    def start(self):
        while not self.done:
            # Limit fps
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.screen.fill("white")
            self.robot.draw(self.screen)
            self.update()

            pygame.display.flip()

    def update(self):
        # rotate
        d_angle = self.robot.w / self.FPS
        
        self.robot.yaw += d_angle
        if self.robot.yaw > math.pi:
            self.robot.yaw -= 2*math.pi
        elif self.robot.yaw < -math.pi:
            self.robot.yaw += 2*math.pi

        for i, (x,y) in enumerate(self.robot.arrowPoints):
            d_x = x - self.robot.x
            d_y = y - self.robot.y
            
            xr = d_x * math.cos(d_angle) - d_y * math.sin(d_angle)
            yr = d_x * math.sin(d_angle) + d_y * math.cos(d_angle)

            self.robot.arrowPoints[i] = (self.robot.x+xr, self.robot.y+yr)
            
        # move
        collision, motionX, motionY = self.getMotion()

        self.robot.x += motionX
        self.robot.y += motionY


        self.robot.arrowPoints = [(x+motionX, y+motionY) for (x, y) in self.robot.arrowPoints]

        if collision:
            self.onCollision()

    def getMotion(self):
        d_shift = self.robot.v / self.FPS * self.PIXEL_PER_METER
        if d_shift == 0:
            return False, 0, 0

        motionX = d_shift * math.cos(self.robot.yaw) 
        motionY = d_shift * math.sin(self.robot.yaw)

        if 0 <= self.robot.yaw <= math.pi:
            dy = self.HEIGHT - self.robot.y -self.robot.r
        else:
            dy = 0 - self.robot.y + self.robot.r

        if -math.pi/2 <= self.robot.yaw <= math.pi/2:
            dx = self.WIDTH - self.robot.x - self.robot.r
        else:
            dx = 0 - self.robot.x + self.robot.r

        if dx == 0:
            dRatio = math.tan(math.pi/2)
        else:
            dRatio = abs(dy/dx)

        if dRatio > abs(math.tan(self.robot.yaw)):
            if motionX + self.robot.x + self.robot.r > self.WIDTH:
                motionX = self.WIDTH - self.robot.x - self.robot.r
            elif motionX + self.robot.x - self.robot.r < 0:
                motionX = 0 - self.robot.x + self.robot.r
            else:
                return False, motionX, motionY

            motionY = motionX * math.tan(self.robot.yaw)
            return True, motionX, motionY

        else:
            if motionY + self.robot.y + self.robot.r > self.HEIGHT:
                motionY = self.HEIGHT - self.robot.y - self.robot.r
            elif motionY + self.robot.y - self.robot.r < 0:
                motionY = 0 - self.robot.y + self.robot.r
            else:
                return False, motionX, motionY

            motionX = motionY / math.tan(self.robot.yaw)
            return True, motionX, motionY

    def onCollision(self):
        self.collisionCall() 
    
class _Robot:
    def __init__(self, x, y):
        self.x, self.y, self.yaw = x, y, 0.0
        self.r = 20
        
        self.v = 0.0
        self.w = 0.0

        l = 4
        self.arrowPoints = [(0, l), (0, 2*l), (3*l, 2*l), (3*l, 3*l), (4*l, l*1.5), (l*3, 0), (l*3, l)] 
        self.arrowPoints = [(x+self.x, self.y+y-1.5*l) for (x,y) in self.arrowPoints]

    def draw(self, screen):
        pygame.draw.circle(screen, "blue", (self.x, self.y), self.r)
        pygame.draw.polygon(screen, (255, 0, 50), self.arrowPoints)
    
if __name__ == "__main__":
    brownian = Brownian()
    brownian.start()
