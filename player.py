import math


class Player:
    def __init__(self, pos, angle=math.pi):
        self.x = pos[0]
        self.y = pos[1]
        self.angle = 0

        self.dx = 0
        self.dy = 0

        self.rotate(angle)

    def move(self, direction):
        if direction == 'forward':
            self.x += self.dx
            self.y += self.dy
        else:
            self.x -= self.dx
            self.y -= self.dy

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def rotate(self, da):
        self.angle += da
        if self.angle < 0:
            self.angle += 2 * math.pi
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
