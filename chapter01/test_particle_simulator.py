class Particle():
    """用于存储粒子的位置(x和y)以及角速度(ang_vel)"""

    def __init__(self, x, y, ang_vel):
        self.x = x
        self.y = y
        self.ang_vel = ang_vel  # ang_vel的符合决定了旋转的方向


class ParticleSimulator():
    """封装了运动定律，负责随时间流逝修改粒子的位置"""

    def __init__(self, particles):
        """存储一个Particle实例列表"""
        self.particles = particles

    def evolve(self, dt):
        """根据指定的定律修改粒子的位置"""
        timestep = 0.00001
        nsteps = int(dt / timestep)

        for i in range(nsteps):
            for p in self.particles:
                # 1. 计算方向
                norm = (p.x ** 2 + p.y ** 2) ** 0.5
                v_x = -p.y / norm
                v_y = p.x / norm

                # 2. 计算位移
                d_x = timestep * p.ang_vel * v_x
                d_y = timestep * p.ang_vel * v_y

                p.x += d_x
                p.y += d_y
                # 3. 不断重复，直到时间过去

# def test_evolve():
#     particles = [Particle(0.3, 0.5, 1), Particle(0.0, -0.5, -1), Particle(-0.1, -0.4, 3)]
#     simulator = ParticleSimulator(particles)
#     simulator.evolve(0.1)

#     p0, p1, p2 = particles

#     def fequal(a, b, eps=1e-5):
#         return abs(a - b) < eps

#     assert fequal(p0.x, 0.210269)
#     assert fequal(p0.y, 0.543863)

#     assert fequal(p1.x, -0.099334)
#     assert fequal(p1.y, -0.490034)

#     assert fequal(p2.x, 0.191358)
#     assert fequal(p2.y, -0.365227)

def test_evolve_benchmark(benchmark):
    particles = [Particle(0.3, 0.5, 1), Particle(0.0, -0.5, -1), Particle(-0.1, -0.4, 3)]
    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)

    p0, p1, p2 = particles
    
    def fequal(a, b, eps=1e-5):
        return abs(a - b) < eps

    assert fequal(p0.x, 0.210269)
    assert fequal(p0.y, 0.543863)

    assert fequal(p1.x, -0.099334)
    assert fequal(p1.y, -0.490034)

    assert fequal(p2.x, 0.191358)
    assert fequal(p2.y, -0.365227)

    benchmark(simulator.evolve, 0.1)