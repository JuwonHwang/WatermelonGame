import pymunk
import numpy as np

class Fruit(pymunk.Body):
    def __init__(self, radius, x, y):
        super().__init__(radius**2, pymunk.moment_for_circle(radius**2, 0, radius))
        self.position = x,y
        self.radius = radius
        self.used = False
        self.circle = 0

    def check_collision(self, other):
        if self is other:
            return -1

        distance = np.linalg.norm(self.position-other.position)
        if distance - 1 < self.radius + other.radius: # collision
            if self.radius == other.radius and self.used == False and other.used == False:
                self.used = True
                other.used = True
                return 1

            # dpos = other.position - self.position
            # dx = other.position[0] - self.position[0]
            # dy = other.position[1] - self.position[1]
            # collision_angle = np.arctan2(dy, dx)
            # magnitude_1 = np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
            # magnitude_2 = np.sqrt(other.vel[0] ** 2 + other.vel[1] ** 2)
            # direction_1 = np.arctan2(self.vel[1], self.vel[0])
            # direction_2 = np.arctan2(other.vel[1], other.vel[0])

            # new_xspeed_1 = self.elasticity * magnitude_1 * np.cos(direction_1 - collision_angle)
            # new_yspeed_1 = self.elasticity * magnitude_1 * np.sin(direction_1 - collision_angle)
            # new_xspeed_2 = self.elasticity * magnitude_2 * np.cos(direction_2 - collision_angle)
            # new_yspeed_2 = self.elasticity * magnitude_2 * np.sin(direction_2 - collision_angle)

            # final_xspeed_1 = ((self.radius - other.radius) * new_xspeed_1 + (other.radius + other.radius) * new_xspeed_2) / (self.radius + other.radius)
            # final_xspeed_2 = ((self.radius + self.radius) * new_xspeed_1 + (other.radius - self.radius) * new_xspeed_2) / (self.radius + other.radius)

            # final_yspeed_1 = new_yspeed_1
            # final_yspeed_2 = new_yspeed_2

            # self.vel[0] = (np.cos(collision_angle) * final_xspeed_1 + np.cos(collision_angle + np.pi / 2) * final_yspeed_1)
            # self.vel[1] = (np.sin(collision_angle) * final_xspeed_1 + np.sin(collision_angle + np.pi / 2) * final_yspeed_1)
            # other.vel[0] = (np.cos(collision_angle) * final_xspeed_2 + np.cos(collision_angle + np.pi / 2) * final_yspeed_2)
            # other.vel[1] = (np.sin(collision_angle) * final_xspeed_2 + np.sin(collision_angle + np.pi / 2) * final_yspeed_2)
            
            # if np.linalg.norm(self.vel) < 1:
            #     self.vel = np.array([0,0])
            # if np.linalg.norm(other.vel) < 1:
            #     other.vel = np.array([0,0])


            # while np.linalg.norm(self.position-other.position) < self.radius + other.radius: # collision
            #     self.position = self.position - np.sign(dpos) 
            #     self.check_boundary_x()
            #     self.check_boundary_y()
            #     other.position = other.position + np.sign(dpos)
            #     other.check_boundary_x()
            #     other.check_boundary_y()
        return 0