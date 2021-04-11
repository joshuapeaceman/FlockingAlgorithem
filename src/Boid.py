import math
import random


class Boid:
    def __init__(self, ctrl, flock):

        self.ctrl = ctrl
        self.flock = flock

        self.x = random.randint(0, self.ctrl.frame_size)
        self.y = random.randint(0, self.ctrl.frame_size)

        self.dx = random.randint(0, self.ctrl.boids_max_speed)
        self.dy = random.randint(0, self.ctrl.boids_max_speed)

    def alignment(self, flock):
        if not flock:
            return

        avgDx = 0
        avgDy = 0
        cnt = 0

        for boid in flock:
            avgDx += boid.dx
            avgDy += boid.dy
            cnt += 1

        if cnt != 0:
            avgDx /= cnt
            avgDy /= cnt

        else:
            avgDx = self.dx
            avgDy = self.dy

        self.dx += (avgDx - self.dx) * self.ctrl.boids_alignment_factor
        self.dy += (avgDy - self.dy) * self.ctrl.boids_alignment_factor

    def cohesion(self, flock):
        if not flock:
            return
        cohesion_x = 0
        cohesion_y = 0
        cnt = 0
        for boid in flock:
            distance = self.distance_to_other_boid(boid)
            cohesion_x += (boid.x)
            cohesion_y += (boid.y)
            cnt += 1

        if cnt != 0:
            cohesion_x /= cnt
            cohesion_y /= cnt

            cohesion_x -= self.x
            cohesion_y -= self.y

        else:
            cohesion_x = 0
            cohesion_y = 0

        self.dx += cohesion_x * self.ctrl.boids_cohesion_factor
        self.dy += cohesion_y * self.ctrl.boids_cohesion_factor

    def separation(self, flock):
        if not flock:
            return
        separation_x = 0
        separation_y = 0
        cnt = 0
        for boid in flock:
            distance = self.distance_to_other_boid(boid)
            if distance != 0:
                separation_x += ((boid.x - self.x) / distance)
                separation_y += ((boid.y - self.y) / distance)
                cnt += 1

        if cnt != 0:
            separation_x /= cnt
            separation_y /= cnt

        else:
            separation_x = 0
            separation_y = 0

        self.dx -= separation_x * self.ctrl.boids_separation_factor
        self.dy -= separation_y * self.ctrl.boids_separation_factor

    def find_interesting_other_boids(self, flock):
        interesting_boids = []
        for idx, boid in enumerate(flock):
            if flock[idx] != self:
                if self.distance_to_other_boid(flock[idx]) < self.ctrl.distance_to_next_boid:
                    if self.is_other_boid_in_field_of_view(flock[idx]):
                        interesting_boids.append(flock[idx])

        return interesting_boids

    def keep_within_bounds(self):
        margin = 100
        turnFactor = 1

        if self.x < margin:
            self.dx += turnFactor
        if self.x > (self.ctrl.frame_size - margin):
            self.dx -= turnFactor

        if self.y < margin:
            self.dy += turnFactor
        if self.y > (self.ctrl.frame_size - margin):
            self.dy -= turnFactor

    def limit_speed(self):
        current_speed = math.sqrt(self.dx ** 2 + self.dy ** 2)
        max_speed = self.ctrl.boids_max_speed
        if current_speed > max_speed:
            self.dx = (self.dx / current_speed) * max_speed
            self.dy = (self.dy / current_speed) * max_speed

    def heading(self):
        if self.dy == 0:
            return 0.0
        return math.degrees(math.asin(self.dy / math.sqrt(self.dx ** 2 + self.dy ** 2)))

    def is_other_boid_in_field_of_view(self, boid):
        dx = boid.x - self.x
        dy = boid.y - self.y

        if dy == 0:
            field_of_view_offset = 0.0
        else:
            field_of_view_offset = math.degrees(math.asin(dy / math.sqrt(dx ** 2 + dy ** 2)))

        heading = self.heading()
        if field_of_view_offset <= heading + self.ctrl.boids_field_of_view_angle and field_of_view_offset >= heading - self.ctrl.boids_field_of_view_angle:
            return True
        else:
            return False

    def distance_to_other_boid(self, boid):
        return math.sqrt((boid.x - self.x) ** 2 + (boid.y - self.y) ** 2)

    def update(self):
        boids = self.find_interesting_other_boids(self.flock)

        self.cohesion(boids)
        self.separation(boids)
        self.alignment(boids)

        self.keep_within_bounds()

        self.limit_speed()
        self.x = self.x + (self.dx / self.ctrl.slow_down_factor)
        self.y = self.y + (self.dy / self.ctrl.slow_down_factor)
