import numpy as np


class Boid:
    def __init__(self, ctrl, flock):

        self.ctrl = ctrl
        self.flock = flock

        self.position = np.random.randint(-150, 150, size=(1, 2))

        self.aligning_force = np.zeros(shape=(1, 2))
        self.cohesion_force = np.zeros(shape=(1, 2))
        self.separation_force = np.zeros(shape=(1, 2))

        self.blab = np.random.randint(-8, 8, size=(1, 2))
        self.normal_4 = np.linalg.norm(self.blab)
        if self.normal_4 != 0:
            self.normal_movement = self.blab / self.normal_4

        self.directional_force = np.random.randint(0, 25, size=(1, 2))

        self.area_boundries = 1500

    def calc_movement(self):
        self.aligning_force = np.zeros(shape=(1, 2))
        self.cohesion_force = np.zeros(shape=(1, 2))
        self.separation_force = np.zeros(shape=(1, 2))
        direction_alignment = np.zeros(shape=(1, 2))
        separation = np.zeros(shape=(1, 2))
        position_cohesion = np.zeros(shape=(1, 2))

        for idx, val in enumerate(self.flock):
            if self.flock[val] != self:
                distance_to_next_boid = np.linalg.norm(np.subtract(self.flock[val].position, self.position), 2)
                if distance_to_next_boid <= self.ctrl.distance_to_next_boid:
                    direction_alignment = np.append(direction_alignment, self.flock[val].directional_force, axis=0)

                    position_cohesion = np.append(position_cohesion, self.flock[val].position, axis=0)

                    separation = np.append(separation,
                                           np.subtract(self.position, self.flock[val].position) / distance_to_next_boid,
                                           axis=0)

                else:
                    self.cohesion_force = np.zeros(shape=(1, 2))
                    self.aligning_force = np.zeros(shape=(1, 2))
                    self.separation_force = np.zeros(shape=(1, 2))

        if self.position[0][0] <= -self.area_boundries or self.position[0][1] <= -self.area_boundries or \
                self.position[0][0] >= self.area_boundries or self.position[0][1] >= self.area_boundries:
            self.position = np.random.randint(-100, 100, size=(1, 2))
            self.cohesion_force = np.zeros(shape=(1, 2))
            self.aligning_force = np.zeros(shape=(1, 2))
            self.separation_force = np.zeros(shape=(1, 2))

        # alignment
        normal = np.linalg.norm(
            np.array([np.average(direction_alignment, axis=0)]))
        if normal != 0:
            self.aligning_force = np.array([np.average(direction_alignment, axis=0)]) / normal

        # cohesion
        avrg_position = np.array([np.average(position_cohesion, axis=0)])
        normal_2 = np.linalg.norm(np.subtract(avrg_position, self.position))
        if normal_2 != 0 and np.linalg.norm(avrg_position) != 0.0:
            self.cohesion_force = np.subtract(avrg_position, self.position) / normal_2

        # separation
        normal_3 = np.linalg.norm(
            np.array([np.average(separation, axis=0)]))
        if normal_3 != 0:
            # self.separation_force = np.array([np.average(separation, axis=0)]) / normal_3
            self.separation_force = np.array([np.average(separation, axis=0)])

        self.blab = np.random.randint(-8, 8, size=(1, 2))
        self.normal_4 = np.linalg.norm(self.blab)
        if self.normal_4 != 0:
            self.normal_movement = self.blab / self.normal_4

    def update(self):
        self.calc_movement()
        self.position = self.position + (
                self.normal_movement * self.ctrl.boids_normal_movement_factor \
                + self.separation_force * self.ctrl.boids_separation_factor \
                + self.cohesion_force * self.ctrl.boids_cohesion_factor \
                + self.aligning_force * self.ctrl.boids_alignment_factor) / self.ctrl.slow_down_factor
