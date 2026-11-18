# import packages
import sys

# import Sandbox
sys.path.insert(1, '../../') # relative path to folder which contains the Sandbox module
from Sandbox_V1_4 import *


def controller_runner_1(dt, inputs, params, state):
    yl = inputs[4]   # yellow left
    yr = inputs[5]   # yellow right
    rl = inputs[6]   # red left
    rr = inputs[7]   # red right
    bl = inputs[8]/2   # blue left, devivding because I set up blue light to have brightness of 2 for runners to know where to run 
    br = inputs[9]/2   # blue right
    
    if bl!=0 and br!=0:
        turn_l=0
        turn_r=0
    else:
        turn_l=params[1] # to turn when no light
        turn_r=params[1]
    
    agressor_left= br*params[0] #run toward blue light
    agressor_right=bl*params[0]

    consider_left=yl*params[2] # consider other runners
    consider_right=yr*params[2]

    coward_left=rl*params[3] # avoid hunters
    coward_right=rr*params[3]

    left_speed_command = agressor_left + turn_l + coward_left + consider_left 
    right_speed_command = agressor_right + turn_r + coward_right + consider_right

    if left_speed_command>5:
        left_speed_command=5
    if right_speed_command>5:
        right_speed_command=5

    return [left_speed_command, right_speed_command], None


def controller_hunter_1(dt, inputs, params, state):
    
    yl = inputs[4]   # yellow left
    yr = inputs[5]   # yellow right
    rl = inputs[6]   # red left 
    rr = inputs[7]   # red right 
    agressor_left=yr*params[0] #chase runners
    agressor_right=yl*params[0]
    if yl!=0 and yr!=0:
        turn_l=0
        turn_r=0
    else:
        turn_l=params[1]
        turn_r=params[1]
    consider_left=rl*params[2] #consider other 
    consider_right=rr*params[2]

    left_speed_command = agressor_left+ turn_r + consider_left
    right_speed_command = agressor_right+turn_l +consider_right

    if left_speed_command>5:
        left_speed_command=5
    if right_speed_command>5:
        right_speed_command=5

    return [left_speed_command, right_speed_command], None

