import random as rn
import numpy as np
from numpy.random import choice as np_choice
from math import sqrt
import matplotlib.pyplot as plt
import csv
import timeit

class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
        Example:
            ant_colony = AntColony(distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        distance_logs=[]
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)
            shortest_path = min(all_paths, key=lambda x: x[1])
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
            distance_logs.append(all_time_shortest_path[1])                      
        return all_time_shortest_path,distance_logs

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        for path, dist in sorted_paths[:n_best]:
            for move in path:
                self.pheromone[move] += 1.0 / self.distances[move]

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start)) # going back to where we started    
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0

        row = (pheromone ** self.alpha) * ((1.0 / (dist + 1e-10)) ** self.beta)
        
        # Handling NaN or infinite values
        invalid_indices = np.isnan(row) | np.isinf(row)
        valid_indices = np.logical_not(invalid_indices)
        row[invalid_indices] = 0  # Replace NaN or infinite values with 0
        total_valid = np.sum(row[valid_indices])
        
        if total_valid > 0:
            row[valid_indices] /= total_valid
        else:
            # If all values are NaN or infinite, set equal probabilities
            row = np.ones_like(row) / len(row)

        move = np_choice(self.all_inds, 1, p=row)[0]
        return move




#Static TSP Instance
# distances = np.array([[np.inf, 2, 2, 5, 7],
#                       [2, np.inf, 4, 8, 2],
#                       [2, 4, np.inf, 1, 3],
#                       [5, 8, 1, np.inf, 2],
#                       [7, 2, 3, 2, np.inf]])


#Dinamic TSP Instance, changing the value of n_nodes will change the
#Instance size
# n_nodes=100
# dist=lambda x,y: sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))
# l=[(rn.random()*1000,rn.random()*1000) for i in range(n_nodes)]
# distances=np.array([[np.inf if i==j else dist(l[i],l[j]) for i in range(len(l))] for j in range(len(l))])


# Open the CSV file
with open('matrizDistancias/40 nodos/matrizDistancia0.csv', 'r') as file:
    reader = csv.reader(file)
    # Skip the header row
    next(reader)
    # Convert the CSV reader to a list of lists and convert each value to an integer
    graph = [[float(value) for value in row] for row in reader]
    graph = [row[1:] for row in graph]
    distancias  = np.array(graph)


start_time = timeit.default_timer()
ant_colony = AntColony(distances=distancias, n_ants=40, n_best=8, n_iterations=100, decay=0.1, alpha=1, beta=1)
shortest_path,log = ant_colony.run()
end_time = timeit.default_timer()
execution_time =  end_time - start_time

print ("Camino: {}".format(shortest_path))
print(f'Tiempo de ejecucion: {execution_time} seg')