# Using NEAT to optimise parameters for coevolution game with Braitenberg vehicles

This project explores the coevolution of "hunters" and "runners" - autonomous agents controlled by neural networks that evolve using the NeuroEvolution of Augmenting Topologies (NEAT) algorithm.
The simulation allows for the study of how competing groups of autonomous agents develop adaptive behaviors through the process of evolution.
Hunters aim to capture runners, while runners strive to escape by reaching a target zone.

The Sandbox API environment used in this project was provided by Professor Chris Johnson of the University of Sussex.

# Requirements

1. Python 3
2. numpy
3. matplotlib
4. neat-python
5. PyYAML

# Execution

Run the main file, `neat_proj.py`, using your IDE.

# How It Works

Each agent is equipped with sensors that react to light sources, along with two wheels that dictate its movement. Sensor inputs are fed into a neural network, which calculates the rotational speed of the left and right wheels.

During the simulation, the position and orientation of the agents are updated in discrete time steps.

The neat-python library is used to evolve the neural network controllers. The NEAT algorithm allows for the modification of network weights and structure through mutation and crossover; the process begins with relatively simple networks, which increase in complexity as evolution progresses.

# Coevolution

The agents are divided into two groups:
- Hunters: attempt to capture the runners.
- Runners: attempt to evade the hunters and reach the target zone.
The fitness of each group depends on its effectiveness in its interaction with the opposing group. This creates evolutionary pressure, compelling both groups to adapt to one another.

# Experimental Results

In experiments conducted without the additional task of collecting light signals, the agents developed distinct behavioral patterns.

The "hunters" evolved movement strategies that included circular trajectories and systematic "sweeping" of the space. The "runners" developed patterns characterized by chaotic, evasive, or directed movement.

The results demonstrated that there is no universal strategy equally effective against every type of opponent. For instance, some hunters successfully intercepted certain runners but encountered difficulties when those runners moved along the arena walls. This points to the existence of cyclical dominance: the strengths of a given strategy against one opponent may become vulnerabilities when facing another.

In an extended version of the environment—where runners were required to collect green light signals before they could escape—the outcomes were less successful.
This can be attributed to the small population size, an insufficient number of generations, and the increased complexity of the task, which necessitated balancing multiple objectives.

# Limitations

1. The small population size limited the diversity of the neural networks that emerged.
2. The number of generations was constrained by the duration of the simulation.
3. The additional task (collecting green signals) made achieving the primary objective more complex.
4. In the extended experiment, it was not possible to achieve consistently effective behavior.
