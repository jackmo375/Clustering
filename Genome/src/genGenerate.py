import numpy as np
import random as rd

NUCL_VEC = ['A','C','G','T']

def genGenome(n_g):
	return np.array([rd.randint(0,3) for i in range(n_g)],
		dtype=np.int32)

def genPanGenome(n_g, n_p):
	'''
	Generate totally random pan genome with no structure
	'''
	panGenome = np.empty([n_p,n_g], dtype=np.int32)
	for i in range(n_p):
		panGenome[i,:] = genGenome(n_g)
	return panGenome

def genGenomeCluster(n_nucleotides, n_genomes, max_dist):

	g = genGenome(n_nucleotides)

	cluster = np.empty([n_genomes,n_nucleotides], dtype=np.int32)
	for i in range(n_genomes):
		n_mutations = rd.randint(0,max_dist-1)
		mutation_loci = [rd.randint(0,n_nucleotides-1) for i in range(n_mutations)]
		cluster[i,:] = mutateGenome(g, mutation_loci)

	return cluster

def mutateGenome(genome, loci):

	mutated = np.copy(genome)
	for i in loci:
		mutated[i] = rd.randint(0,3)

	return mutated
