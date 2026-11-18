# I did some modification to sandbox for it to fulfill my task. Instances of Robot class now have 'catched' and 'win'
#attributes. Cathced detects whether object is a runner and if it has been touched by hunter. Win detects if runner achieved
#the goal. If runner is cathced it movement speed is set to 0 and light colour turned to grey and brightnes turned to 0.
#I also added global parameter to monitor number of catched pray and won pray.

# import packages
import sys
import yaml
import time

#from microbial_GA import MicrobialGA
# import Sandbox
sys.path.insert(1, '.assignment_1') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *
import global_values
# import local files
from controllers import *

#########################################################################
#                        Read parameter file                            #
#########################################################################

# read parameters from file
class Braitenberg ():
    def __init__(self, hunter_params, runner_params):
        self.hunter_params=hunter_params
        self.runner_params=runner_params
        

    def create_light(self,n,colour,x_light,y_light):
        light_list=[]
        for i in range(n):
            t=LightSource(x=x_light, y=y_light, model='linear',brightness=1,colour=colour)
            light_list.append(t)
            x_light+=10
        return light_list
    
    def starting(self,l):
        
        with open('./params.yaml', 'r') as file:
           params_dict = yaml.safe_load(file)
        duration = params_dict["duration"]
        screen_width = params_dict["screen_width"]
        animate = True if params_dict["animate"] == 1 else False
        animation_frame_delay = params_dict["animation_frame_delay"]
        plot_data = True if params_dict["plot_data"] == 1 else False

#########################################################################
#                         Set up environment                            #
#########################################################################
# set colour of second group of lights
        arena_dimantions=30
        arena = Arena([],x_left=-arena_dimantions,x_right=arena_dimantions,y_top=arena_dimantions,y_bottom=-arena_dimantions)
        
        n=5
        yellow_light_sources=self.create_light(n,'yellow',-10,-5)
        red_light_sources=self.create_light(n,'red',-10,5)
        blue_light_sources=[LightSource(x=0, y=35, model='linear',brightness=2,colour="blue")]

#########################################################################
#                           Set up agents                               #
#########################################################################

# set up hunters sensors. Hunters have nothing to do with blue light, so they don't have blue sensors. It would just 
# add unneccessary noice to GA
        x = 10
        y = 0
        FOV = 7*math.pi/8
        sensors_huters = []
        sensors_huters.append(LightSensor(light_sources=yellow_light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
        sensors_huters.append(LightSensor(light_sources=yellow_light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
        sensors_huters.append(LightSensor(light_sources=red_light_sources, x=x, y=y, FOV=FOV, colour="red"))
        sensors_huters.append(LightSensor(light_sources=red_light_sources, x=x, y=y, FOV=FOV, colour="red"))
# specify angular positions of sensors on robot's body
        sensor_angles_hunters = [2*math.pi/8, -2*math.pi/8, math.pi/4 - 0.3, -(math.pi/4 - 0.3)]

# set up runners sensors
        sensors_runners = []
        sensors_runners.append(LightSensor(light_sources=yellow_light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
        sensors_runners.append(LightSensor(light_sources=yellow_light_sources, x=x, y=y, FOV=FOV, colour="yellow"))
        sensors_runners.append(LightSensor(light_sources=red_light_sources, x=x, y=y, FOV=FOV, colour="red"))
        sensors_runners.append(LightSensor(light_sources=red_light_sources, x=x, y=y, FOV=FOV, colour="red"))
        sensors_runners.append(LightSensor(light_sources=blue_light_sources, x=x, y=y, FOV=FOV, colour="blue"))
        sensors_runners.append(LightSensor(light_sources=blue_light_sources, x=x, y=y, FOV=FOV, colour="blue"))
# specify angular positions of sensors on robot's body
        sensor_angles_runners = [2*math.pi/8, -2*math.pi/8, math.pi/4 - 0.3, -(math.pi/4 - 0.3),math.pi/2-1.3,-(math.pi/2-1.3)]

# construct Robot

        #runner_params=[1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        controller_runner = Controller(step_fun=controller_runner_1, inputs_n=6, commands_n=2, params=self.runner_params)
        controller_hunter = Controller(step_fun=controller_hunter_1, inputs_n=4, commands_n=2, params=self.hunter_params)

        agents=[]
        x_light=0
        y_light=0
        for light_yellow in yellow_light_sources:
            rob=Robot(x=x_light, y=y_light, theta=0, controller=controller_runner, sensors=sensors_runners, sensor_angles=sensor_angles_runners, light=light_yellow, type='runner')
            agents.append(rob)
            x_light+=10
        x_light=0
        y_light=50
        for light_red in red_light_sources:
            rob=Robot(x=x_light, y=y_light, theta=0, controller=controller_hunter, sensors=sensors_huters, sensor_angles=sensor_angles_hunters, light=light_red,type='hunter')
            agents.append(rob)
            x_light+=10

# put robot into list of agents for Simulator


#########################################################################
#                    Set up experimental conditions                     #
#########################################################################

# nothing to set up this time, but we will still need a list of disturbances, even if it is empty
        disturbances = []

#########################################################################
#                      Set up and run simulation                        #
#########################################################################

        arena.agents = agents
        bumper = AgentCollisionManager(agents)
        # get Simulator object - note that agents, environmental systems, and disturbances are all passed to its constructor
        sim = Simulator(agents=agents, envs=blue_light_sources+yellow_light_sources+red_light_sources+[arena, bumper], duration=duration, dt=0.1, disturbances=disturbances)
        # get SimulationRunner object
        sim_runner = SimulationRunner(sim, animate=l, pause_ani=True, animation_delay=animation_frame_delay, screen_width=screen_width)
        # use SimulationRunner to run Simulation n number of times
        start = time.perf_counter()

        global_values.catched_pray=0 #setting global parameters to zero for each generations
        global_values.win_pray=0 
      

        sim_data = sim_runner.run_sims(n=1)
        end = time.perf_counter()
        elapsed=end - start

        self.plotting(sim_data,agents)
        return elapsed,global_values.catched_pray,global_values.win_pray

#########################################################################
#                     Plotting and analysis section                     #
#########################################################################
        


# plot agents' trajectories
    def plotting(self,sim_data,agents):
        ax = plot_all_sims_trajectories(sim_data, show_cbar=False, cbar_fig=False)


        for rob in agents:
            rob.draw(ax)
        plt.show()
"""
runner_params = [2, 1, 0, 1]
hunter_params = [2, 1, 0]
l=True
f=Braitenberg(hunter_params,runner_params)
f.starting(l)"""