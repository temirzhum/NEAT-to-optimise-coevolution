import sys
# relative path to folder which contains the Sandbox module
sys.path.insert(1, '../../')
from Sandbox_V1_4 import *

# from BraitenbergController import *
from disturbances import *
from controllers import *

# set pygame window size automatically
import tkinter
root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

# prepare environment
radius = 15
arena = CircularArena([], x=0, y=0, radius=radius)

# add lights around edge of arena
light_sources = []
n = 24
for i in range(n):
    angle = i * 2 * math.pi / n
    light_sources.append(LightSource(radius*math.cos(angle), radius*math.sin(angle), 1))

# set up circular obstacles
obstacles = []
for _ in range(5):
    spread = 9
    obstacles.append(CircularArena([], x=random_in_interval(-spread, spread), y=random_in_interval(-spread, spread), radius=random_in_interval(1.3, 3), keep_out=True))

# "attach" lights to centres of circular obstacles, setting brightness according to obstacle radius
for obstacle in obstacles:
    light_sources.append(LightSource(obstacle.x, obstacle.y, obstacle.radius))

# set up rectangular obstacles, with lights at their centres
for _ in range(3):
    x_left = random_in_interval(-7, 7)
    y_bottom = random_in_interval(-7, 7)
    x_right = x_left + random_in_interval(1, 4)
    y_top = y_bottom + random_in_interval(1, 4)
    obstacles.append(Arena([], x_left=x_left, x_right=x_right, y_top=y_top, y_bottom=y_bottom, keep_out=True))
    light_sources.append(LightSource(x_left+(x_right-x_left)/2, y_bottom+(y_top-y_bottom)/2, 8))

# noisemakers for ant controller
noisemaker = BrownNoiseSource(max_step_size=0.01)
noisemaker2 = BrownNoiseSource(max_step_size=0.01)

# set up controller for ant
controller = AntController(inputs_n=2, step_fun=ant_correlated_random_walk, params=[1], noisemakers=[noisemaker, noisemaker2], noisemakers_inds=[1, 0])

# this object manages the ant's pheromones, and how quickly they evaporate
phermanager = PheromoneManager(decay_rate=0.01)

# construct ant agent
ant = Ant(x=4, y=9, theta=0, controller=controller, sensors=[], sensor_angles=[], turn_motor_inertia=10, pheromone_manager=phermanager, drop_interval=1)

# set up robot controller
generalised_controller = RobotController(inputs_n=6, step_fun=generalised_braitenberg, noisemakers=[], noisemakers_inds=[], params=[3.6, 0, 0.05, 0, 3, 0])

# set parameters for robot sensor morphology (roughly speaking, morphology means the structure and properties of the body)
field_of_view = 0.9 * math.pi
left_sensor_angle = np.pi/6
right_sensor_angle = -np.pi/6

# construct robot, using the controller and parameters specified above
robot = new_light_seeking_Robot(x=-5, y=0, theta=0, light_sources=light_sources, controller=generalised_controller, FOV=field_of_view, left_sensor_angle=left_sensor_angle, right_sensor_angle=right_sensor_angle, left_motor_inertia=1, right_motor_inertia=1)

# put agents in list
agents = [ant, robot]

# this object handles agents colliding with each other - without it, they can just pass over each other
bumper = AgentCollisionManager(agents)

# make arena and obstacles interact with agents
arena.agents = agents
for obstacle in obstacles:
    obstacle.agents = agents

disturbances = []

# simulation run parameters
screen_width = int(0.9*height) # 700
print(screen_width)
duration = 600
animate = True

sim = Simulator(agents=agents, envs=[arena, bumper] + light_sources + obstacles + [phermanager], duration=duration, dt=0.1, disturbances=disturbances)
sim_runner = SimulationRunner(sim, animate=True, pause_ani=True, screen_width=screen_width)
sim_data = sim_runner.run_sims(n=1)

ax = plot_all_sims_trajectories(sim_data, show_cbar=False, cbar_fig=False)
arena.draw(ax)
for obstacle in obstacles:
    obstacle.draw(ax)

plot_all_agents_basic_data(sim_data, show_motors=False, show_controllers=False, show_sensors=True)

plt.figure()
plt.plot(ant.move_motor.speeds)
plt.title("move motor speed")

plt.figure()
plt.plot(ant.turn_motor.speeds)
plt.title("turn motor speed")

plt.figure()
plt.plot(ant.controller.commands_hist)
plt.title("controller outputs")

plt.show()
