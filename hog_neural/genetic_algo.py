from neural import NeuralNet, getRandomNumber
import sys
import random
sys.path.insert(0, 'C:/Users/trest/cs61a/projects/hog') #need to change file path probably
from hog import average_win_rate
from math import log
import time
start_time = time.time()


'''primary variables, if you want to mess around with things, I'd say that these variables and the rank_population function are the places to start'''
mutation_rate=0.1
crossover_rate=0.7  #i havent implemented crossover yet so this variable is useless currently
population_size=256
elite_percent_of_pop=6.25
generations=200
hidden_layer_size =3
numof_hidden_layers=1


#helper variables
best_net=None
best_net_str=""
best_win_rate=0

def make_population(size,input_size, output_size, hidden_layer_size=3, numof_hidden_layers=1):
	population=[]
	for i in range(size):
		population.append(NeuralNet(input_size, output_size,hidden_layer_size, numof_hidden_layers))
	return population
def make_strat(net):
	'''helper function'''
	return lambda score0,score1: round(10*(net.update(score0,score1)[0]))

def rank_population(population):
	'''this is the most important function, it decides on the fitness of each member of the population
	there fitness is porportional to how likely they are to get chosen for the next generation'''
	#current set up is ranking them based on how well they do in a tournment fight and then how well they do againgst your final strat
	#initialize an empty fitness list and a winners list (contains all winner indexes)

	fitness=[0]*len(population)
	winners=[]
	losers=[]
	for i in range(len(population)):
		winners.append(i)
	'''make everyone compete in a tournment tree and make fitness=1/tournment_level where 
	tournment level is the level they got to decided by that tournement_layers=log(#competetors,2)
	tournment_level=log(len(population),2)+1	
	while tournment_level>1:
		#have last rounds winners compete
		for i in range (len(winners)//2):
			winner=average_win_rate(make_strat(population[winners[2*i]]),make_strat(population[winners[2*i+1]]))
			if winner>=0.5:
				fitness[winners[2*i+1]]=1/tournment_level
				losers.append(2*i+1)
			else:
				fitness[winners[2*i]]=1/tournment_level
				losers.append(2*i)
		#remove all losers
		for i in reversed(losers):
			del winners[i]
		losers.clear()
		tournment_level-=1

	'''
	
	#now pit them against final strat and add 2*win_rate to fitness score
	for i in range(len(population)):
		fitness[i]+=2*average_win_rate(make_strat(population[i]))

	return fitness

def crossover(net1,net2,mutation_rate):
	#helper function
	return net1.crossover(net2,mutation_rate)

def selection(population, fitness):
	'''Uses a roulette wheel to randomly select parents from the population based on their fitness
	the higher the fitness, the higher the chance of being selected'''

	#get total fitness
	sum_fitness=sum(fitness)
	sum_probability=0
	#assign each person a percent to get picked proportional to fitness
	for i in range(len(fitness)):
		fitness[i]=sum_probability + (fitness[i]/sum_fitness)
		sum_probability+=fitness[i]
	#pick 2 random numbers between 0 & 1 and find corrisponding population memebers to breed
	new_population=getElite(population,fitness,int(population_size*elite_percent_of_pop/100))
	while len(new_population)<population_size:
		numbers=[getRandomNumber(0,1),getRandomNumber(0,1)]
		parents=[]
		not_found=[True,True]
		for i in range(len(fitness)):
			if fitness[i]>numbers[0] and not_found[0]:
				#found first parent
				parents.append(population[i])
				not_found[0]=False
			if fitness[i]>numbers[1] and not_found[1]:
				#found second parent
				parents.append(population[i])
				not_found[1]=False
		#make a new child between the parents and add them to next generation
		new_population.append(crossover(parents[0], parents[1],mutation_rate))

	return new_population

def getElite(population, fitness, n):
	'''returns the top n of the population to survive to the next generation'''
	top_fitness=sorted(fitness)[population_size-n:]
	top_n=[]
	last=0
	for t in top_fitness:
		top_n.append(population[fitness.index(t)])
		last=t
	if top_n[-1]!=best_net:
		top_n.append(best_net)
	if last !=max(fitness):
		print("Something wrong")
	return top_n



#everything below is just output stuff, you can change the file name if you wanna save it somewhere special
file=open("generations_test.txt", "w")
def print_best(population, fitness):
	'''saves all time best net to text file and prints best nets preformance this generation'''
	win_rate=average_win_rate(make_strat(population[fitness.index(max(fitness))]))
	print("Winners algo against base:",win_rate)

	if win_rate>best_win_rate:
		global best_win_rate, best_net, best_net_str
		best_win_rate=win_rate
		best_net_str=str(population[fitness.index(max(fitness))].getNet())
		best_net=population[fitness.index(max(fitness))]
	file.write("Best net:"+best_net_str+"\n")

def save_generation(generation, population):
	'''saves every net to text file'''
	file.write("Generation: "+str(generation)+"\n")
	for pop in population:
		file.write(str(pop.getNet())+"\n")

def load_population(file_name,generation="LAST"):
	'''Not implemented yet, need to make the neural net be able to be initialized with string variable'''
	print("load")


sample_net={0: [[-0.9721978025244997, -0.8608603440819742, 0.3817686057645424], [-0.6878710774872121, -0.5344534314268106, -0.6882488275652301], [-0.14289802892528858, 0.9650124463941834, -0.42627366392169175]], 1: [[0.27110852944205277, -0.13608671587633925, -0.5349938172112922, -0.4424173250048222]]}


#below is basically the main
population=make_population(population_size,2,1, hidden_layer_size, numof_hidden_layers)
for i in range(generations):
	save_generation(i, population)
	print("Generation: "+str(i))
	fitness=rank_population(population)
	print_best(population,fitness)
	population=selection(population, fitness)
	print("--- %s seconds ---" % (time.time() - start_time))
	sys.stdout.flush()