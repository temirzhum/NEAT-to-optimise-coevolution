
import numpy as np
from numpy import random
from Brait import Braitenberg
import matplotlib.pyplot as plt
import os
import time
class MicrobialGA():
    def __init__(self):
        pass

    def ffunction1(self,cand_hunter,cand_runner,l):
        ### activates rabin fingerprint. Percentage of saved space is fitness value
        vehicle=Braitenberg(cand_hunter,cand_runner)
        time, catched_pray,win_prey=vehicle.starting(l)

        fitness_hunter=(2*(catched_pray/5)+(1-time/30))/3 #30 second is maximum time for simulation without animation for my pc
        fitness_runner=(2*(win_prey/5)+(1-time/30))/3     # 3 is maximum possible value achived from the formula
        if catched_pray==0:
            fitness_hunter=0
        if win_prey==0:
            fitness_runner=0

        return fitness_hunter,fitness_runner
 
    def tournament_selection(self,pop_genotypes, pop_fitnesses):
        max_fit=max(pop_fitnesses)
        max_index=pop_fitnesses.index(max_fit)

        min_fit=min(pop_fitnesses)
        min_index=pop_fitnesses.index(min_fit)
        return max_index, min_index


    def microbial_selection(self,pop_genotypes, pop_fitnesses,D):
        #because of strange error AttributeError: module 'numpy.random' has no attribute 'randrange' I am using range
        A=random.choice(range(D))
        B=(A+random.randint(1,D))%len(pop_genotypes)## % to wrap around
        if pop_fitnesses[A]>pop_fitnesses[B]:
            win_index=A
            los_index=B
        else:
            win_index=B
            los_index=A
        
        return win_index,los_index

    def uniform_crossover(self,cand_loser, cand_winner, prob_csross, n_genes):
        copy_loser = cand_loser.copy()

        for i in range(n_genes):
            
                prob = random.random()
                if prob < prob_csross:
                    copy_loser[i] = cand_winner[i]

        return copy_loser

    def micro_GA(self,pop_size,p_mutation,microbial_max,n_hun,n_run,D,l,hopeful_monsters_prob):
        best_fitness_hystory_hunters=[]
        best_fitness_hystory_runners=[]
        pop_genotypes_hunters=[]
        pop_genotypes_runners=[]
        pop_fitnesses_hunters=[]
        pop_fitnesses_runners=[]
        microbial_currrent_hunters=0
        
        print("Generating random genotypes")
        for i in range(pop_size-1):
            genotype_hunter=self.random_genotype(n_hun)
            genotype_runner=self.random_genotype(n_run)
            pop_genotypes_hunters.append(genotype_hunter)
            pop_genotypes_runners.append(genotype_runner)
            fit_hun,fit_run=self.ffunction1(genotype_hunter,genotype_runner,l)
            pop_fitnesses_hunters.append(fit_hun)
            pop_fitnesses_runners.append(fit_run)
        
        print(f"Finished creating genotypes\n Original genotypes for hunters \n{pop_genotypes_hunters}\n Original genotypes for runners \n{pop_genotypes_runners}\n{'*'*10}starting to mutate{'*'*10}")
        while microbial_currrent_hunters<microbial_max:
            print(f"{'*'*10} {microbial_currrent_hunters}/{microbial_max}{'*'*10}")
            overall_fit_hun=0
            overall_fit_run=0

            winner_index_hunter,loser_index_hunter=self.microbial_selection(pop_genotypes_hunters,pop_fitnesses_hunters,D)
            winner_index_runner,loser_index_runner=self.microbial_selection(pop_genotypes_runners,pop_fitnesses_runners,D)
            #crossover + mutation hunter
            loser_copy_hunter=self.uniform_crossover(pop_genotypes_hunters[loser_index_hunter],pop_genotypes_hunters[winner_index_hunter],1/8,len(pop_genotypes_hunters[loser_index_hunter]))
            pop_genotypes_hunters[loser_index_hunter]=self.mutate_genotype(loser_copy_hunter,p_mutation,hopeful_monsters_prob)
            #crossover + mutation runner
            loser_copy_runner=self.uniform_crossover(pop_genotypes_runners[loser_index_runner],pop_genotypes_runners[winner_index_runner],1/8,len(pop_genotypes_runners[loser_index_runner]))
            pop_genotypes_runners[loser_index_runner]=self.mutate_genotype(loser_copy_runner,p_mutation,hopeful_monsters_prob)
            #calculating fitness for losers
            for i in range(3): # comparing fitness 3 times vs random apponent
                current_fit_hun,_=self.ffunction1(pop_genotypes_hunters[loser_index_hunter],pop_genotypes_runners[random.randint(0,pop_size-1)],l)
                _,current_fit_run=self.ffunction1(pop_genotypes_hunters[random.randint(0,pop_size-1)],pop_genotypes_runners[loser_index_runner],l)
                overall_fit_hun+=current_fit_hun
                overall_fit_run+=current_fit_run
            pop_fitnesses_hunters[loser_index_hunter]=overall_fit_hun/3
            pop_fitnesses_runners[loser_index_runner]=overall_fit_run/3

            microbial_currrent_hunters+=1

            max_fit=max(pop_fitnesses_hunters)
            best_fitness_hystory_hunters.append(max_fit)
        
            max_fit_run=max(pop_fitnesses_runners)
            best_fitness_hystory_runners.append(max_fit_run)

        return pop_genotypes_hunters, pop_genotypes_runners,pop_fitnesses_hunters, pop_fitnesses_runners,best_fitness_hystory_hunters,best_fitness_hystory_runners
    
    def mutate_genotype(self, genotype, p_mutation,hopeful_monsters_prob):
        copy_cand = genotype.copy()
        for i in range(len(genotype)):
                if random.random() < p_mutation:
                    copy_cand[i] = copy_cand[i]-0.2
                elif random.random() < p_mutation:
                    copy_cand[i] = copy_cand[i]+0.2
                if random.random()<hopeful_monsters_prob:
                    copy_cand[i] = copy_cand[i]+1
                elif random.random()<hopeful_monsters_prob:
                    copy_cand[i] = copy_cand[i]-1
                if random.random()<hopeful_monsters_prob:
                    copy_cand[i] = copy_cand[i]*-1
        return copy_cand
        
    def random_genotype(self,n):
        genotype=[]
        for i in range(n):
            if i==1: #because turning behaviour should always be slower than other
                a=random.uniform(-0.5, 0.5)
            else:
                a=random.uniform(-2, 2)
            genotype.append(a)
        
        return genotype


def main():
    microbialGA=MicrobialGA()
    p_mutation1 = 1/5
    a=input("Do you want animation to play? Enter 1 for YES and 0 for NO\n>>")
    if a=="1":
        l=True
    elif a=="0":
        l=False
    
    # genotype=[int(rand_deg_pol),int(polynomial),int(rand_window_degree),int(mask),min, max]

    """cand_best1, fitness_best1,fitness_history,positive_mutations = microbialGA.generalised_hill_climber(
        fitness_target=100,
        iteration_max=number_of_generations,
        p_mutation=p_mutation1,
        cand=cand,
    )"""
    start = time.perf_counter()
    
    pop_genotypes_hunters, pop_genotypes_runners,pop_fitnesses_hunters, pop_fitnesses_runners,best_fitness_hystory_hunters,best_fitness_hystory_runners=microbialGA.micro_GA(
        pop_size=7,
        p_mutation=p_mutation1,
        microbial_max=10,
        n_hun=3,
        n_run=4,
        D=3,
        l=l,
        hopeful_monsters_prob=0.01
    )
    end = time.perf_counter()
    elapsed=end - start
    print(f"Overall time for algorithm {elapsed} sec")
    winner_index,loser_index=microbialGA.microbial_selection(pop_genotypes_hunters,pop_fitnesses_hunters,D=5)
    print("\nPopulation of hunters is\n")
    for i in range(len(pop_genotypes_hunters)):
        print(f"{pop_genotypes_hunters[i]} it's fitness is {pop_fitnesses_hunters[i]}")

    print("\nPopulation of runners is\n")
    for i in range(len(pop_genotypes_runners)):
        print(f"{pop_genotypes_runners[i]} it's fitness is {pop_fitnesses_runners[i]}")
 

    try:
        max_fit_hun=max(pop_fitnesses_hunters)
        max_index_hunters=pop_fitnesses_hunters.index(max_fit_hun)
        print(f"\nThe best cand of hunters is {pop_genotypes_hunters[max_index_hunters]}, it's fitness is {max_fit_hun}, index {max_index_hunters}")
        plt.figure(figsize=(8,5))
        plt.plot(range(1, len(best_fitness_hystory_hunters)+1), best_fitness_hystory_hunters, marker='o')
        plt.xlabel("Iterations")
        plt.ylabel("Fitness")
        plt.title("Hunter Fitness over iterations")
        plt.grid(True)
        plt.show()
    except:
        print("something went wrong when printing graph for hunter")


    try:
        max_fit_run=max(pop_fitnesses_runners)
        max_index_runners=pop_fitnesses_runners.index(max_fit_run)
        print(f"\nThe best cand of runners is {pop_genotypes_runners[max_index_runners]}, it's fitness is {max_fit_run}, index {max_index_runners}")
        plt.figure(figsize=(8,5))
        plt.plot(range(1, len(best_fitness_hystory_runners)+1), best_fitness_hystory_runners, marker='o')
        plt.xlabel("Iterations")
        plt.ylabel("Fitness")
        plt.title("Runner Fitness over iterations")
        plt.grid(True)
        plt.show()
    except:
        print("something went wrong when printing graph for runners")

def test_1():
    runner_params = [-1.0935290586175563, -2.262602117843621, -1.0369459524601699, 0.5584253106781603]
    hunter_params =[-1.0625809985807089, -0.19010542474140596, -1.7965813491903622]
    l=True
    f=Braitenberg(hunter_params,runner_params)
    f.starting(l)

if __name__ == "__main__":
    test_1()  #To run just hunter/runner game
    #main()   #To run coevolution


