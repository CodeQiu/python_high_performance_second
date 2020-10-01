from matplotlib import pyplot as plt
from matplotlib import animation
from random import uniform


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


def visualize(simulator):
    """将一个ParticleSimulator实例作为参数，并以动画的方式显示粒子的运动轨迹"""
    X = [p.x for p in simulator.particles]
    Y = [p.y for p in simulator.particles]

    fig = plt.figure()
    ax = plt.subplot(111, aspect="equal")
    line, = ax.plot(X, Y, "ro")

    # 指定坐标轴的取值范围
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    # 这个方法将在动画开始时运行
    def init():
        line.set_data([], [])
        return line,  # 这里的逗号必不可少

    def animate(i):
        # 让粒子运动0.01个时间单位
        simulator.evolve(0.01)
        X = [p.x for p in simulator.particles]
        Y = [p.y for p in simulator.particles]

        line.set_data(X, Y)
        return line,

    # 每隔10毫秒调用一次动画函数
    anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True, interval=10)
    plt.show()


# 为了测试这些代码，定义test_visualize，它以动画方式模拟一个包含3个粒子的系统，其中每个粒子的运动方向各不相同。第三个粒子环绕一周的速度是其他两个粒子的3倍
def test_visualize():
    particles = [Particle(0.3, 0.5, 1), Particle(0.0, -0.5, -1), Particle(-0.1, -0.4, 3)]
    simulator = ParticleSimulator(particles)
    visualize(simulator)


def test_evolve():
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


# 编写一个有代表性的基准测试程序：实例化1000个坐标和角速度都是随机的Particle对象，并将它们提供给ParticleSimulator类，然后让系统运行0.1个时间单位
def benchmark():
    particles = [Particle(uniform(-1.0, 1.0), uniform(-1.0, 1.0), uniform(-1.0, 1.0)) for i in range(1000)]

    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)


if __name__ == "__main__":
    test_visualize()

    # test_evolve()

    # benchmark()
