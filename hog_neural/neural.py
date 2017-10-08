
from math import exp
import random

class Neuron(object):
	"""This represents a single Neuron in the Neural Net. 
	It takes inputs compares it to its weights, and then fires to tbe next neuron"""
	def __init__(self, weights):
		super (Neuron, self).__init__()
		self.weights = weights
	def calculate(self, inputs):
		sum=0
		for i in range(len(inputs)):
			sum+=inputs[i]*self.weights[i]
		sum+=self.weights[-1]
		return sigmoid(sum)
	def getWeights(self):
		return self.weights
	def crossover(self, other, mutation_rate):
		"""This function takes takes two neurons and returns a neuron
		 that is a combination of the two """
		new_weights=[]
		for i in range(len(self.weights)):
			if getRandomNumber(0,1)<mutation_rate:
				new_weights.append(getRandomNumber())
			elif i%2==0:
				new_weights.append(self.weights[i])
			else:
				new_weights.append(other.weights[i])
		return new_weights
def sigmoid(n):
	return 1/(1+exp(-n))

class NeuralNet(object):
	"""This object takes inputs and puts them through its neuralnet"""
	def __init__(self, input_size, output_size, hidden_layer_size =3, numof_hidden_layers=1, net=None,strNet=None):
		super(NeuralNet, self).__init__()
		self.input_size=input_size
		self.output_size=output_size
		self.hidden_layer_size=hidden_layer_size
		self.numof_hidden_layers=numof_hidden_layers
		if net==None:
			self.net={}
			for i in range(numof_hidden_layers+1):
				if i==0:
					self.net[i]=makeLayer(hidden_layer_size,input_size+1)
				else:
					self.net[i]=makeLayer(hidden_layer_size, hidden_layer_size+1)
			self.net[numof_hidden_layers]=makeLayer(output_size,hidden_layer_size+1)
		elif strNet:
			self.net={}
			for i in strNet:
				temp_layer=[]
				for j in range(len(strNet[i])):
					temp_layer.append(Neuron(strNet[i][j]))
				self.net[i]=temp_layer
		else:
			self.net=net

	def update (self,*args):
		"""This function takes input_size inputs, puts them through the neuralnet,
		 then returns resulting output. Outputs are floats between 0 & 1 """
		arguments=[]
		#for i in args:
		#	arguments.append(i)
		output=[]
		for i in range(self.numof_hidden_layers+1):
			temp_output=[]
			for node in self.net[i]:
				if i==0:
					temp_output.append(node.calculate(args))
				else:
					temp_output.append(node.calculate(output))
			output=temp_output
		return output

	def crossover(self, other,mutation_rate=0.007):
		"""This function takes takes two nerualnets and returns a neuralnet 
		that is a combination of the two """
		new_net={}
		for i in range(self.numof_hidden_layers+1):
			new_layer=[]
			for j in range(len(self.net[i])):
				#self.net[i][j] is the jth neuron in layer i
				new_weights=self.net[i][j].crossover(other.net[i][j], mutation_rate)
				new_layer.append(Neuron(new_weights))
			new_net[i]=new_layer

		return NeuralNet(self.input_size, self.output_size, self.hidden_layer_size, self.numof_hidden_layers,new_net)

	def getNet(self):
		temp_net={}
		for i in range(self.numof_hidden_layers+1):
			temp_layer=[]
			for j in range(len(self.net[i])):
				temp_weights=self.net[i][j].getWeights()
				temp_layer.append(temp_weights)
			temp_net[i]=temp_layer
		return temp_net


def makeLayer(layer_size, weights_size):
	layer=[]
	weights=[]
	for i in range(layer_size):
		layer.append(Neuron(getRandomLayer(weights_size)))
	return layer


def getRandomLayer(weights_size):
	random_list=[]
	for i in range(weights_size):
		random_list.append(getRandomNumber())
	return random_list
def getRandomNumber(start=-1, end=1):
	return random.uniform(start,end)

sample_net={0: [[-0.9721978025244997, -0.8608603440819742, 0.3817686057645424], [-0.6878710774872121, -0.5344534314268106, -0.6882488275652301], [-0.14289802892528858, 0.9650124463941834, -0.42627366392169175]], 1: [[0.27110852944205277, -0.13608671587633925, -0.5349938172112922, -0.4424173250048222]]}

def printW():
	for i in sample_net:
		for j in range(len(sample_net[i])):
			print(sample_net[i][j])
			
