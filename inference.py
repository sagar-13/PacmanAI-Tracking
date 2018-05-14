# # inference.py
# # ------------
# # Licensing Information:  You are free to use or extend these projects for
# # educational purposes provided that (1) you do not distribute or publish
# # solutions, (2) you retain this notice, and (3) you provide clear
# # attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# # 
# # Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# # The core projects and autograders were primarily created by John DeNero
# # (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# # Student side autograding was added by Brad Miller, Nick Hay, and
# # Pieter Abbeel (pabbeel@cs.berkeley.edu).


# import itertools
# import util
# import random
# import busters
# import game

# class InferenceModule:
#     """
#     An inference module tracks a belief distribution over a ghost's location.
#     This is an abstract class, which you should not modify.
#     """

#     ############################################
#     # Useful methods for all inference modules #
#     ############################################

#     def __init__(self, ghostAgent):
#         "Sets the ghost agent for later access"
#         self.ghostAgent = ghostAgent
#         self.index = ghostAgent.index
#         self.obs = [] # most recent observation position

#     def getJailPosition(self):
#         return (2 * self.ghostAgent.index - 1, 1)

#     def getPositionDistribution(self, gameState):
#         """
#         Returns a distribution over successor positions of the ghost from the
#         given gameState.

#         You must first place the ghost in the gameState, using setGhostPosition
#         below.
#         """
#         ghostPosition = gameState.getGhostPosition(self.index) # The position you set
#         actionDist = self.ghostAgent.getDistribution(gameState)
#         dist = util.Counter()
#         for action, prob in actionDist.items():
#             successorPosition = game.Actions.getSuccessor(ghostPosition, action)
#             dist[successorPosition] = prob
#         return dist

#     def setGhostPosition(self, gameState, ghostPosition):
#         """
#         Sets the position of the ghost for this inference module to the
#         specified position in the supplied gameState.

#         Note that calling setGhostPosition does not change the position of the
#         ghost in the GameState object used for tracking the true progression of
#         the game.  The code in inference.py only ever receives a deep copy of
#         the GameState object which is responsible for maintaining game state,
#         not a reference to the original object.  Note also that the ghost
#         distance observations are stored at the time the GameState object is
#         created, so changing the position of the ghost will not affect the
#         functioning of observeState.
#         """
#         conf = game.Configuration(ghostPosition, game.Directions.STOP)
#         gameState.data.agentStates[self.index] = game.AgentState(conf, False)
#         return gameState

#     def observeState(self, gameState):
#         "Collects the relevant noisy distance observation and pass it along."
#         distances = gameState.getNoisyGhostDistances()
#         if len(distances) >= self.index: # Check for missing observations
#             obs = distances[self.index - 1]
#             self.obs = obs
#             self.observe(obs, gameState)

#     def initialize(self, gameState):
#         "Initializes beliefs to a uniform distribution over all positions."
#         # The legal positions do not include the ghost prison cells in the bottom left.
#         self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
#         self.initializeUniformly(gameState)

#     ######################################
#     # Methods that need to be overridden #
#     ######################################

#     def initializeUniformly(self, gameState):
#         "Sets the belief state to a uniform prior belief over all positions."
#         pass

#     def observe(self, observation, gameState):
#         "Updates beliefs based on the given distance observation and gameState."
#         pass

#     def elapseTime(self, gameState):
#         "Updates beliefs for a time step elapsing from a gameState."
#         pass

#     def getBeliefDistribution(self):
#         """
#         Returns the agent's current belief state, a distribution over ghost
#         locations conditioned on all evidence so far.
#         """
#         pass

# class ExactInference(InferenceModule):
#     """
#     The exact dynamic inference module should use forward-algorithm updates to
#     compute the exact belief function at each time step.
#     """

#     def initializeUniformly(self, gameState):
#         "Begin with a uniform distribution over ghost positions."
#         self.beliefs = util.Counter()
#         for p in self.legalPositions: self.beliefs[p] = 1.0
#         self.beliefs.normalize()

#     def observe(self, observation, gameState):
#         """Updates beliefs based on the distance observation and Pacman's
#         position.

#         When we enter this function pacman's distribution over
#         possible locations of the ghost are stored in self.beliefs

#         For any position p:
#         self.beliefs[p] = Pr(Xt=p | e_{t-1}, e_{t-2}, ..., e_1)

#         That is, pacman's distribution has already been updated by all
#         prior observations already.

#         This function should update self.beliefs[p] so that
#         self.beliefs[p] = Pr(Xt=p |e_t, e_{t-1}, e_{t-2}, ..., e_1)

#         That is, it should update pacman's distribution over the
#         ghost's locations to account for the passed observation.

#         noisyDistance (= the next observation e_t) is the estimated
#         Manhattan distance to the ghost you are tracking.

#         emissionModel = busters.getObservationDistribution(noisyDistance)
#         stores the probability of having observed noisyDistance given any
#         true distance you supply. That is
#         emissionModel[trueDistance] = Pr(noisyDistance | trueDistance).

#         Since our observations have to do with manhattanDistance with
#         no indication of direction, we take
#         Pr(noisyDistance | Xt=p) =
#             Pr(noisyDistance | manhattanDistance(p,packmanPosition))

#         That is, the probability of observing noisyDistance given that the
#         ghost is in position p is equal to the probability of having
#         observed noisyDistance given the trueDistance between p and the
#         pacman's current position.

#         self.legalPositions is a list of the possible ghost positions
#         (Only positions in self.legalPositions need to have
#          their probability updated)

#         A correct implementation will handle the following special
#         case:

#         * When a ghost is captured by Pacman, all beliefs should be
#           updated so that pacman believes the ghost to be in its
#           prison cell with probability 1, this position is
#           self.getJailPosition()

#           You can check if a ghost has been captured by Pacman by
#           checking if it has a noisyDistance of None (a noisy distance
#           of None will be returned if, and only if, the ghost is
#           captured, note 0 != None).

#         """
#         noisyDistance = observation
#         emissionModel = busters.getObservationDistribution(noisyDistance)
#         pacmanPosition = gameState.getPacmanPosition()

#         "*** YOUR CODE HERE ***"
#         #the code below updates pacman's beliefs so that it
#         #has a uniform distribution over all possible positions
#         #the ghost could be.
#         #
#         # Replace this code with a correct observation update
#         # Be sure to handle the "jail" edge case where the ghost is eaten
#         # and noisyDistance is None

#         #self.initializeUniformly(gameState)
#         """
#         allPossible = util.Counter()
#         for p in self.legalPositions:
#             trueDistance = util.manhattanDistance(p, pacmanPosition)
#             if emissionModel[trueDistance] > 0:
#                 allPossible[p] = 1.0
#         print "beliefs = ", self.beliefs, "\n"
#         print "allPossible = ", allPossible, "\n"
#         print "noisyDistance = ", noisyDistance, "\n"
#         print "emissionModel = ", emissionModel, "\n"
#         print "pacmanPosition  = ", pacmanPosition , "\n"
#         print "_____________________________________________________"

#         """
#         allPossible = util.Counter()
#         if noisyDistance is None:
#            # print "set the value of ghost being in location jail to 1"
#             for p in self.legalPositions:
#                 allPossible[p] = 0.0
#             allPossible[self.getJailPosition()] = 1.0
#         else:
#             #print "do everything normally"
#             for p in self.legalPositions:
#                 trueDistance = util.manhattanDistance(p, pacmanPosition)
#                 if emissionModel[trueDistance] > 0:
#                     allPossible[p] =  emissionModel[trueDistance]*self.beliefs[p]
#             #self.beliefs = allPossible.normalize()

#         "*** END YOUR CODE HERE ***"

#         allPossible.normalize()
#         self.beliefs = allPossible

#     def elapseTime(self, gameState):
#         """Update self.beliefs in response to a time step passing from the
#         current state.

#         When we enter this function pacman's distribution over
#         possible locations of the ghost are stored in self.beliefs

#         For any position p:
#         self.beliefs[p] = Pr(X_{t-1} = p | e_{t-1}, e_{t-2} ... e_1)

#         That is, pacman has a distribution over the previous time step
#         having taken into account all previous observations.

#         This function should update self.beliefs so that
#         self.beliefs[p] = P(Xt = p | e_{t-1}, e_{t_2} ..., e_1)

#         That is, it should update pacman's distribution over the
#         ghost's locations to account for progress in time.

#         The transition model (Pr(X_t|X_{t-1) may depend on Pacman's
#         current position (e.g., for DirectionalGhost).  However, this
#         is not a problem, as Pacman's current position is known.

#         In order to obtain the distribution over new positions for the
#         ghost, given its previous position (oldPos) as well as
#         Pacman's current position, use this line of code:

#           newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

#         newPosDist is a util.Counter object, where for each position p in
#         self.legalPositions,

#         newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )


#         newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )

#         You may also find it useful to loop over key, value pairs in
#         newPosDist, like:

#           for newPos, prob in newPosDist.items():
#             ...


#         HINT. obtaining newPostDist is relatively expensive.  If you
#               look carefully at the HMM "progress in time" equation
#               you will see that you can orgranize the computation so
#               that you use newPosDist[p] for all values of p (by,
#               e.g., the for loop above) before moving on the next
#               newPosDist (generated by another oldPos).

#         *** GORY DETAIL AHEAD ***

#         As an implementation detail (with which you need not concern yourself),
#         the line of code at the top of this comment block for obtaining
#         newPosDist makes use of two helper methods provided in InferenceModule
#         above:

#           1) self.setGhostPosition(gameState, ghostPosition)
#               This method alters the gameState by placing the ghost we're
#               tracking in a particular position.  This altered gameState can be
#               used to query what the ghost would do in this position.

#           2) self.getPositionDistribution(gameState)
#               This method uses the ghost agent to determine what positions the
#               ghost will move to from the provided gameState.  The ghost must be
#               placed in the gameState with a call to self.setGhostPosition
#               above.

#         It is worthwhile, however, to understand why these two helper
#         methods are used and how they combine to give us a belief
#         distribution over new positions after a time update from a
#         particular position.

#         """
#         "*** YOUR CODE HERE ***"
#         allPossible = util.Counter()
#         """possible useful things
#         # newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
#         for newPos, prob in newPosDist.items():
#             ...
#         """
#         for oldPos in self.legalPositions:
#             newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
#             for newPos, prob in newPosDist.items():
#                 #print "newPos = ", newPos, ", prob = ", prob
#                 allPossible[newPos]   += prob * self.beliefs[oldPos]

#         allPossible.normalize()
#         self.beliefs = allPossible
#         "*** END YOUR CODE HERE ***"

#     def getBeliefDistribution(self):
#         return self.beliefs

# class ParticleFilter(InferenceModule):
#     """
#     A particle filter for approximately tracking a single ghost.

#     Useful helper functions will include random.choice, which chooses an element
#     from a list uniformly at random, and util.sample, which samples a key from a
#     Counter by treating its values as probabilities.
#     """

#     def __init__(self, ghostAgent, numParticles=300):
#         InferenceModule.__init__(self, ghostAgent);
#         self.setNumParticles(numParticles)

#     def setNumParticles(self, numParticles):
#         self.numParticles = numParticles


#     def initializeUniformly(self, gameState):
#         """
#         Initializes a list of particles. Use self.numParticles for the number of
#         particles. Use self.legalPositions for the legal board positions where a
#         particle could be located.  Particles should be evenly (not randomly)
#         distributed across positions in order to ensure a uniform prior.

#         Note: the variable you store your particles in must be a list; a list is
#         simply a collection of unweighted variables (positions in this case).
#         Storing your particles as a Counter (where there could be an associated
#         weight with each position) is incorrect and may produce errors.
#         """
#         "*** YOUR CODE HERE ***"
#         self.Particles = []
#         #distribute particles to each position uniformly
#         particlesAtPoisition = self.numParticles/(len(self.legalPositions))
#         for pos in self.legalPositions:
#             for i in range(0, particlesAtPoisition,1):
#                 self.Particles.append(pos)
#         "*** END YOUR CODE HERE ***"


#     def observe(self, observation, gameState):
#         """
#         Update beliefs based on the given distance observation. Make sure to
#         handle the special case where all particles have weight 0 after
#         reweighting based on observation. If this happens, resample particles
#         uniformly at random from the set of legal positions
#         (self.legalPositions).

#         A correct implementation will handle two special cases:
#           1) When a ghost is captured by Pacman, all particles should be updated
#              so that the ghost appears in its prison cell,
#              self.getJailPosition()

#              As before, you can check if a ghost has been captured by Pacman by
#              checking if it has a noisyDistance of None.

#           2) When all particles receive 0 weight, they should be recreated from
#              the prior distribution by calling initializeUniformly. The total
#              weight for a belief distribution can be found by calling totalCount
#              on a Counter object

#         util.sample(Counter object) is a helper method to generate a sample from
#         a belief distribution.

#         You may also want to use util.manhattanDistance to calculate the
#         distance between a particle and Pacman's position.
#         """
#         noisyDistance = observation
#         emissionModel = busters.getObservationDistribution(noisyDistance)
#         pacmanPosition = gameState.getPacmanPosition()
#         "*** YOUR CODE HERE ***"
#         #initialize counter for use
#         allPossible = util.Counter()
#         if noisyDistance is None:
#            # Case when ghost is captured, same as ExactInference
#             for p in self.legalPositions:
#                 allPossible[p] = 0.0
#             allPossible[self.getJailPosition()] = 1.0
#         else:
#             # same as ExactInference except belief distribution instead of self.beliefs
#             for p in self.legalPositions:
#                 trueDistance = util.manhattanDistance(p, pacmanPosition)
#                 if emissionModel[trueDistance] > 0:
#                     allPossible[p] =  emissionModel[trueDistance]*self.getBeliefDistribution()[p]

#         allPossible.normalize()
#         self.beliefs = allPossible
#         # Need to check if all weights are zero
#         AllWeightZero = False
#         # totalcount was causing test to fail so used this instead
#         # loop that goes over every value and checks if they are all zero
#         for value in self.beliefs.values():
#             if value == 0:
#                 AllWeightZero = True
#                 continue
#             else:
#                 AllWeightZero = False
#                 break

#         #Handle cases appropriately
#         if AllWeightZero:
#             self.initializeUniformly(gameState)
#         else:
#             self.Particles = util.nSample(self.beliefs.values(),self.beliefs.keys(), self.numParticles)
#             # self.Particles = []
#             # for i in range(0,self.numParticles):
#             #     self.Particles.append(util.sample(self.beliefs))
#         "*** END YOUR CODE HERE ***"


#     def elapseTime(self, gameState):
#         """
#         Update beliefs for a time step elapsing.

#         As in the elapseTime method of ExactInference, you should use:

#           newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

#         to obtain the distribution over new positions for the ghost, given its
#         previous position (oldPos) as well as Pacman's current position.

#         util.sample(Counter object) is a helper method to generate a sample from
#         a belief distribution.
#         """
#         "*** YOUR CODE HERE ***"
#         #util.raiseNotDefined()
#         """From previous function
#                 for oldPos in self.legalPositions:
#             newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
#             for newPos, prob in newPosDist.items():
#                 #print "newPos = ", newPos, ", prob = ", prob
#                 allPossible[newPos]   += prob * self.beliefs[oldPos]

#         allPossible.normalize()
#         self.beliefs = allPossible

#         useful code
#         newPostDist = self.getPoisitonDistrubution(self.setGhostPosition(gameSTate, oldPos))

#         util.sample(Counter object) -> sample from belief distribution

#         code that adds particles
#                     self.Particles = []
#             for i in range(self.numParticles):
#                 self.Particles.append(util.sample(self.beliefs))
#         """
#         tempParticles = []
#         for location in self.Particles:
#             newPostDist = self.getPositionDistribution(self.setGhostPosition(gameState, location))
    
#             # self.Particles = util.nSample(self.beliefs.values(),self.beliefs.keys(), self.numParticles)
#             a = util.nSample(newPostDist.values(), newPostDist.keys(), 1)
#             # print a
#             tempParticles.append(a[0])
#             # print(tempParticles)

#         self.Particles = tempParticles


#         "*** END YOUR CODE HERE ***"



#     def getBeliefDistribution(self):
#         """
#         Return the agent's current belief state, a distribution over ghost
#         locations conditioned on all evidence and time passage. This method
#         essentially converts a list of particles into a belief distribution (a
#         Counter object)
#         """
#         "*** YOUR CODE HERE ***"
#         #initialize counter, and put every legal position in it
#         dist = util.Counter()
#         for position in self.legalPositions:
#             dist[position] = 0
#         #record how many times each position is occuring in self.Particles
#         for position in self.Particles:
#             dist[position] +=1
#         #normalize it and return
#         dist.normalize()
#         return dist
#         "*** END YOUR CODE HERE ***"


# class MarginalInference(InferenceModule):
#     """
#     A wrapper around the JointInference module that returns marginal beliefs
#     about ghosts.
#     """

#     def initializeUniformly(self, gameState):
#         "Set the belief state to an initial, prior value."
#         if self.index == 1:
#             jointInference.initialize(gameState, self.legalPositions)
#         jointInference.addGhostAgent(self.ghostAgent)

#     def observeState(self, gameState):
#         "Update beliefs based on the given distance observation and gameState."
#         if self.index == 1:
#             jointInference.observeState(gameState)

#     def elapseTime(self, gameState):
#         "Update beliefs for a time step elapsing from a gameState."
#         if self.index == 1:
#             jointInference.elapseTime(gameState)

#     def getBeliefDistribution(self):
#         "Returns the marginal belief over a particular ghost by summing out the others."
#         jointDistribution = jointInference.getBeliefDistribution()
#         dist = util.Counter()
#         for t, prob in jointDistribution.items():
#             dist[t[self.index - 1]] += prob
#         return dist

# class JointParticleFilter:
#     """
#     JointParticleFilter tracks a joint distribution over tuples of all ghost
#     positions.
#     """

#     def __init__(self, numParticles=600):
#         self.setNumParticles(numParticles)

#     def setNumParticles(self, numParticles):
#         self.numParticles = numParticles

#     def initialize(self, gameState, legalPositions):
#         "Stores information about the game, then initializes particles."
#         self.numGhosts = gameState.getNumAgents() - 1
#         self.ghostAgents = []
#         self.legalPositions = legalPositions
#         self.initializeParticles()

#     def initializeParticles(self):
#         """
#         Initialize particles to be consistent with a uniform prior.

#         Each particle is a tuple of ghost positions. Use self.numParticles for
#         the number of particles. You may find the `itertools` package helpful.
#         Specifically, you will need to think about permutations of legal ghost
#         positions, with the additional understanding that ghosts may occupy the
#         same space. Look at the `itertools.product` function to get an
#         implementation of the Cartesian product.

#         Note: If you use itertools, keep in mind that permutations are not
#         returned in a random order; you must shuffle the list of permutations in
#         order to ensure even placement of particles across the board. Use
#         self.legalPositions to obtain a list of positions a ghost may occupy.

#         Note: the variable you store your particles in must be a list; a list is
#         simply a collection of unweighted variables (positions in this case).
#         Storing your particles as a Counter (where there could be an associated
#         weight with each position) is incorrect and may produce errors.
#         """
#         "*** YOUR CODE HERE ***"
#         self.particles = []
       
#         iterProduct = itertools.product(self.legalPositions, repeat = self.numGhosts)
#         AllLocations = []
#         for x in iterProduct :
#             AllLocations.append(x)
#         random.shuffle(AllLocations)
#         for i in range(0, self.numParticles, 1):
#             for position in AllLocations:
#                 self.particles.append(position)
#         # random.shuffle(self.particles)

#         "*** END YOUR CODE HERE ***"


#     def addGhostAgent(self, agent):
#         """
#         Each ghost agent is registered separately and stored (in case they are
#         different).
#         """
#         self.ghostAgents.append(agent)

#     def getJailPosition(self, i):
#         return (2 * i + 1, 1)

#     def observeState(self, gameState):
#         """Resamples the set of particles using the likelihood of the noisy
#         observations.
#         To loop over the ghosts, use: for i in range(self.numGhosts):
#         Two special cases:
#         1) All particles get weight 0 due to the observation,
#            a new set of particles need to be generated from the initial
#            prior distribution by calling initializeParticles.
#         2) Otherwise after all new particles have been generated by
#            resampling you must check if any ghosts have been captured
#            by packman (noisyDistances[i] will be None if ghost i has
#            ben captured).

#            For each captured ghost, you need to change the i'th component
#            of every particle (remember that the particles contain a position
#            for every ghost---so you need to change the component associated
#            with the i'th ghost.). In particular, if ghost i has been captured
#            then the i'th component of every particle must be changed so
#            the i'th ghost is in its prison cell (position self.getJailPosition(i))

#             Note that more than one ghost might be captured---you need
#             to ensure that every particle puts every captured ghost in
#             its prison cell.

#         self.getParticleWithGhostInJail is a helper method to help you
#         edit a specific particle. Since we store particles as tuples,
#         they must be converted to a list, edited, and then converted
#         back to a tuple. This is a common operation when placing a
#         ghost in jail. Note that this function
#         creates a new particle, that has to replace the old particle in
#         your list of particles.
#         HINT1. The weight of every particle is the product of the probabilities
#                of associated with each ghost's noisyDistance observation
#         HINT2. When computing the weight of a particle by looking at each
#                ghost's noisyDistance observation make sure you check
#                if the ghost has been captured. Captured ghost's are ignored
#                in the weight computation (the particle's component for
#                the captured ghost is updated the precise position later---so
#                this corresponds to multiplying the weight by probability 1
#         """
#         pacmanPosition = gameState.getPacmanPosition()
#         noisyDistances = gameState.getNoisyGhostDistances()
#         if len(noisyDistances) < self.numGhosts:
#             return
#         emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]

#         "*** YOUR CODE HERE ***"
        
#         allPossible = util.Counter()
        
#         for particle_tuple in self.particles:
#             prob = 1
#             for i in range(0, self.numGhosts):
#                 if noisyDistances[i] is None: 
#                     particle_tuple = self.getParticleWithGhostInJail(particle_tuple, i)
#                 else:
#                     distance = util.manhattanDistance(particle_tuple[i], pacmanPosition)
#                     prob *= emissionModels[i][distance]
#             allPossible[particle_tuple] += prob

#         self.beliefs = allPossible
#         self.beliefs.normalize()
#         # loop that goes over every value and checks if they are all zero
#         AllWeightZero = False
#         for value in self.beliefs.values() :
#             if value == 0:
#                 AllWeightZero = True
#                 continue
#             else:
#                 AllWeightZero = False
#                 break
#         # Handle cases appropriately
#         if not AllWeightZero:
#             self.particles = []
            
#             for x in range(0,self.numParticles):
#                 self.particles.append(util.sample(self.beliefs))
#             return
    
#         self.initializeParticles()
#         for particle_tuple in self.particles:
#             for i in range(0,self.numGhosts):
#                 if noisyDistances[i] is None:
#                     particle_tuple = self.getParticleWithGhostInJail(particle_tuple, i)
            
            
#         "*** END YOUR CODE HERE ***"


#     def getParticleWithGhostInJail(self, particle, ghostIndex):
#         """
#         Takes a particle (as a tuple of ghost positions) and returns a particle
#         with the ghostIndex'th ghost in jail.
#         """
#         particle = list(particle)
#         particle[ghostIndex] = self.getJailPosition(ghostIndex)
#         return tuple(particle)

#     def elapseTime(self, gameState):
#         """
#         Samples each particle's next state based on its current state and the
#         gameState.

#         To loop over the ghosts, use:

#           for i in range(self.numGhosts):
#             ...

#         Then, assuming that `i` refers to the index of the ghost, to obtain the
#         distributions over new positions for that single ghost, given the list
#         (prevGhostPositions) of previous positions of ALL of the ghosts, use
#         this line of code:

#           newPosDist = getPositionDistributionForGhost(
#              setGhostPositions(gameState, prevGhostPositions), i, self.ghostAgents[i]
#           )

#         Note that you may need to replace `prevGhostPositions` with the correct
#         name of the variable that you have used to refer to the list of the
#         previous positions of all of the ghosts, and you may need to replace `i`
#         with the variable you have used to refer to the index of the ghost for
#         which you are computing the new position distribution.

#         As an implementation detail (with which you need not concern yourself),
#         the line of code above for obtaining newPosDist makes use of two helper
#         functions defined below in this file:

#           1) setGhostPositions(gameState, ghostPositions)
#               This method alters the gameState by placing the ghosts in the
#               supplied positions.

#           2) getPositionDistributionForGhost(gameState, ghostIndex, agent)
#               This method uses the supplied ghost agent to determine what
#               positions a ghost (ghostIndex) controlled by a particular agent
#               (ghostAgent) will move to in the supplied gameState.  All ghosts
#               must first be placed in the gameState using setGhostPositions
#               above.

#               The ghost agent you are meant to supply is
#               self.ghostAgents[ghostIndex-1], but in this project all ghost
#               agents are always the same.
#         """
#         newParticles = []
#         for oldParticle in self.particles:
#             newParticle = list(oldParticle) # A list of ghost positions
#             # now loop through and update each entry in newParticle...

#             "*** YOUR CODE HERE ***"
#             for i in range(0, self.numGhosts):
#                     newPosDist = getPositionDistributionForGhost(
#                             setGhostPositions(gameState, newParticle), i, self.ghostAgents[i])             
#                     newParticle[i] = util.nSample(newPosDist.values(), newPosDist.keys(), 1)[0]
   

#             "*** END YOUR CODE HERE ***"
#             newParticles.append(tuple(newParticle))
#         self.particles = newParticles


#     def getBeliefDistribution(self):
#         "*** YOUR CODE HERE ***"
#         # dist = util.Counter()

#         # #record how many times each position is occuring in self.Particles
#         # for position in self.particles:
#         #     dist[position] +=1
#         # #normalize it and return
#         # dist.normalize()
#         # return dist

#         #initialize counter, and put every legal position in it
#         dist = util.Counter()
#         for position in self.legalPositions:
#             dist[position] = 0
#         #record how many times each position is occuring in self.Particles
#         for positiontuple in self.particles:
#             dist[positiontuple] +=1.0
#         #normalize it and return
#         dist.normalize()
#         return dist
#         "*** END YOUR CODE HERE ***"


# # One JointInference module is shared globally across instances of MarginalInference
# jointInference = JointParticleFilter()

# def getPositionDistributionForGhost(gameState, ghostIndex, agent):
#     """
#     Returns the distribution over positions for a ghost, using the supplied
#     gameState.
#     """
#     # index 0 is pacman, but the students think that index 0 is the first ghost.
#     ghostPosition = gameState.getGhostPosition(ghostIndex+1)
#     actionDist = agent.getDistribution(gameState)
#     dist = util.Counter()
#     for action, prob in actionDist.items():
#         successorPosition = game.Actions.getSuccessor(ghostPosition, action)
#         dist[successorPosition] = prob
#     return dist

# def setGhostPositions(gameState, ghostPositions):
#     "Sets the position of all ghosts to the values in ghostPositionTuple."
#     for index, pos in enumerate(ghostPositions):
#         conf = game.Configuration(pos, game.Directions.STOP)
#         gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
#     return gameState

# inference.py
# ------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import itertools
import util
import random
import busters
import game

class InferenceModule:
    """
    An inference module tracks a belief distribution over a ghost's location.
    This is an abstract class, which you should not modify.
    """

    ############################################
    # Useful methods for all inference modules #
    ############################################

    def __init__(self, ghostAgent):
        "Sets the ghost agent for later access"
        self.ghostAgent = ghostAgent
        self.index = ghostAgent.index
        self.obs = [] # most recent observation position

    def getJailPosition(self):
        return (2 * self.ghostAgent.index - 1, 1)

    def getPositionDistribution(self, gameState):
        """
        Returns a distribution over successor positions of the ghost from the given gameState.
        You must first place the ghost in the gameState, using setGhostPosition below.
        """
        ghostPosition = gameState.getGhostPosition(self.index) # The position you set
        actionDist = self.ghostAgent.getDistribution(gameState)
        dist = util.Counter()
        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(ghostPosition, action)
            dist[successorPosition] = prob
        return dist

    def setGhostPosition(self, gameState, ghostPosition):
        """
        Sets the position of the ghost for this inference module to the specified
        position in the supplied gameState.
        Note that calling setGhostPosition does not change the position of the
        ghost in the GameState object used for tracking the true progression of
        the game.  The code in inference.py only ever receives a deep copy of the
        GameState object which is responsible for maintaining game state, not a
        reference to the original object.  Note also that the ghost distance
        observations are stored at the time the GameState object is created, so
        changing the position of the ghost will not affect the functioning of
        observeState.
        """
        conf = game.Configuration(ghostPosition, game.Directions.STOP)
        gameState.data.agentStates[self.index] = game.AgentState(conf, False)
        return gameState

    def observeState(self, gameState):
        "Collects the relevant noisy distance observation and pass it along."
        distances = gameState.getNoisyGhostDistances()
        if len(distances) >= self.index: # Check for missing observations
            obs = distances[self.index - 1]
            self.obs = obs
            self.observe(obs, gameState)

    def initialize(self, gameState):
        "Initializes beliefs to a uniform distribution over all positions."
        # The legal positions do not include the ghost prison cells in the bottom left.
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.initializeUniformly(gameState)

    ######################################
    # Methods that need to be overridden #
    ######################################

    def initializeUniformly(self, gameState):
        "Sets the belief state to a uniform prior belief over all positions."
        pass

    def observe(self, observation, gameState):
        "Updates beliefs based on the given distance observation and gameState."
        pass

    def elapseTime(self, gameState):
        "Updates beliefs for a time step elapsing from a gameState."
        pass

    def getBeliefDistribution(self):
        """
        Returns the agent's current belief state, a distribution over
        ghost locations conditioned on all evidence so far.
        """
        pass

class ExactInference(InferenceModule):
    """
    The exact dynamic inference module should use forward-algorithm
    updates to compute the exact belief function at each time step.
    """

    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        """
        Updates beliefs based on the distance observation and Pacman's position.
        The noisyDistance is the estimated manhattan distance to the ghost you are tracking.
        The emissionModel below stores the probability of the noisyDistance for any true
        distance you supply.  That is, it stores P(noisyDistance | TrueDistance).
        self.legalPositions is a list of the possible ghost positions (you
        should only consider positions that are in self.legalPositions).
        A correct implementation will handle the following special case:
          *  When a ghost is captured by Pacman, all beliefs should be updated so
             that the ghost appears in its prison cell, position self.getJailPosition()
             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).
        """
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        "*** YOUR CODE HERE ***"
        # jail position is (1, 1) not one of legal positions
        # print self.getJailPosition()
        # print noisyDistance
        # print emissionModel
        # print pacmanPosition
        # print self.beliefs
        # print self.legalPositions



# {1: 0.16492146596858642, 2: 0.16753926701570682, 3: 0.33507853403141363, 4: 0.16753926701570682, 5: 0.08376963350785341, 6: 0.041884816753926704, 7: 0.020942408376963352, 8: 0.010471204188481676, 9: 0.005235602094240838, 10: 0.002617801047120419}
# {(5, 4): 0.125, (3, 4): 0.125, (1, 4): 0.125, (7, 4): 0.125, (9, 4): 0.125, (5, 2): 0.125, (2, 4): 0.125, (8, 4): 0.125}
# [(1, 4), (2, 4), (3, 4), (5, 2), (5, 4), (7, 4), (8, 4), (9, 4)]

        # Replace this code with a correct observation update
        # Be sure to handle the "jail" edge case where the ghost is eaten
        # and noisyDistance is None

        allPossible = util.Counter()
        # for p in self.legalPositions:
        #     trueDistance = util.manhattanDistance(p, pacmanPosition)
        #     if emissionModel[trueDistance] > 0: allPossible[p] = 1.0

        if noisyDistance == None:
            allPossible = util.Counter()
            allPossible[self.getJailPosition()] = 1.0
        else:
            for location in self.legalPositions:
                distance = util.manhattanDistance(location, pacmanPosition)
                allPossible[location] = emissionModel[distance] * self.beliefs[location]
        # print self.beliefs

        "*** END YOUR CODE HERE ***"

        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        """
        Update self.beliefs in response to a time step passing from the current state.
        The transition model is not entirely stationary: it may depend on Pacman's
        current position (e.g., for DirectionalGhost).  However, this is not a problem,
        as Pacman's current position is known.
        In order to obtain the distribution over new positions for the
        ghost, given its previous position (oldPos) as well as Pacman's
        current position, use this line of code:
          newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
        Note that you may need to replace "oldPos" with the correct name
        of the variable that you have used to refer to the previous ghost
        position for which you are computing this distribution. You will need to compute
        multiple position distributions for a single update.
        newPosDist is a util.Counter object, where for each position p in self.legalPositions,
        newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )
        (and also given Pacman's current position).  You may also find it useful to loop over key, value pairs
        in newPosDist, like:
          for newPos, prob in newPosDist.items():
            ...
        *** GORY DETAIL AHEAD ***
        As an implementation detail (with which you need not concern
        yourself), the line of code at the top of this comment block for obtaining newPosDist makes
        use of two helper methods provided in InferenceModule above:
          1) self.setGhostPosition(gameState, ghostPosition)
              This method alters the gameState by placing the ghost we're tracking
              in a particular position.  This altered gameState can be used to query
              what the ghost would do in this position.
          2) self.getPositionDistribution(gameState)
              This method uses the ghost agent to determine what positions the ghost
              will move to from the provided gameState.  The ghost must be placed
              in the gameState with a call to self.setGhostPosition above.
        It is worthwhile, however, to understand why these two helper methods are used and how they
        combine to give us a belief distribution over new positions after a time update from a particular position
        """

        "*** YOUR CODE HERE ***"

        allPossible = util.Counter()
        for oldPos in self.legalPositions:
            newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
            for newPos, prob in newPosDist.items():
                allPossible[newPos] += prob*self.beliefs[oldPos]
            # allPossible[oldPos] *= self.beliefs[gameState.getPacmanPosition()]
            # allPossible[oldPos] *= self.beliefs[]
        self.beliefs = allPossible
            # print newPosDist
        # allPossible = util.Counter()
        # for oldPos in self.legalPositions:
        #     newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
        #     for newPos, prob in newPosDist.items():
        #         allPossible[oldPos] += prob*allPossible[oldPos]
        #     allPossible[oldPos] *=
        # self.beliefs = allPossible


        # util.raiseNotDefined()

    def getBeliefDistribution(self):
        return self.beliefs

class ParticleFilter(InferenceModule):
    """
    A particle filter for approximately tracking a single ghost.
    Useful helper functions will include random.choice, which chooses
    an element from a list uniformly at random, and util.sample, which
    samples a key from a Counter by treating its values as probabilities.
    """


    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent);
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles


    def initializeUniformly(self, gameState):
        """
          Initializes a list of particles. Use self.numParticles for the number of particles.
          Use self.legalPositions for the legal board positions where a particle could be located.
          Particles should be evenly (not randomly) distributed across positions in order to
          ensure a uniform prior.
          ** NOTE **
            the variable you store your particles in must be a list; a list is simply a collection
            of unweighted variables (positions in this case). Storing your particles as a Counter or
            dictionary (where there could be an associated weight with each position) is incorrect
            and will produce errors
        """
        "*** YOUR CODE HERE ***"
        count, self.particles = 0, []
        while count < self.numParticles:
            for position in self.legalPositions:
                if count < self.numParticles:
                    self.particles.append(position)
                    count += 1

    def observe(self, observation, gameState):
        """
        Update beliefs based on the given distance observation. Make
        sure to handle the special case where all particles have weight
        0 after reweighting based on observation. If this happens,
        resample particles uniformly at random from the set of legal
        positions (self.legalPositions).
        A correct implementation will handle two special cases:
          1) When a ghost is captured by Pacman, **all** particles should be updated so
             that the ghost appears in its prison cell, self.getJailPosition()
             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).
          2) When all particles receive 0 weight, they should be recreated from the
             prior distribution by calling initializeUniformly. The total weight
             for a belief distribution can be found by calling totalCount on
             a Counter object
        util.sample(Counter object) is a helper method to generate a sample from
        a belief distribution
        You may also want to use util.manhattanDistance to calculate the distance
        between a particle and pacman's position.
        """

        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()

        if noisyDistance == None: # Case 1
            self.particles = [self.getJailPosition()] * self.numParticles
        else:
            allPossible, oldBelief = util.Counter(), self.getBeliefDistribution()
            for location in self.legalPositions:
                distance = util.manhattanDistance(location, pacmanPosition)
                allPossible[location] += emissionModel[distance] * oldBelief[location]
            if not any(allPossible.values()): # Case 2
                self.initializeUniformly(gameState)
            else:
                temp = []
                for _ in range(0, self.numParticles):
                    temp.append(util.sample(allPossible)) #recreate samples based on distribution allPossible
                self.particles = temp

    def elapseTime(self, gameState):
        """
        Update beliefs for a time step elapsing.
        As in the elapseTime method of ExactInference, you should use:
          newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
        to obtain the distribution over new positions for the ghost, given
        its previous position (oldPos) as well as Pacman's current
        position.
        util.sample(Counter object) is a helper method to generate a sample from a
        belief distribution
        """
        "*** YOUR CODE HERE ***"

        tmpParticles = []
        for oldPos in self.particles:
            newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))
            tmpParticles.append(util.sample(newPosDist))
        self.particles = tmpParticles


        # util.raiseNotDefined()

    def getBeliefDistribution(self):
        """
          Return the agent's current belief state, a distribution over
          ghost locations conditioned on all evidence and time passage. This method
          essentially converts a list of particles into a belief distribution (a Counter object)
        """
        "*** YOUR CODE HERE ***"
        distribution = util.Counter()
        for element in self.particles:
            distribution[element] += 1
        distribution.normalize()
        return distribution

class MarginalInference(InferenceModule):
    "A wrapper around the JointInference module that returns marginal beliefs about ghosts."

    def initializeUniformly(self, gameState):
        "Set the belief state to an initial, prior value."
        if self.index == 1: jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.ghostAgent)

    def observeState(self, gameState):
        "Update beliefs based on the given distance observation and gameState."
        if self.index == 1: jointInference.observeState(gameState)

    def elapseTime(self, gameState):
        "Update beliefs for a time step elapsing from a gameState."
        if self.index == 1: jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        "Returns the marginal belief over a particular ghost by summing out the others."
        jointDistribution = jointInference.getBeliefDistribution()
        dist = util.Counter()
        for t, prob in jointDistribution.items():
            dist[t[self.index - 1]] += prob
        return dist

class JointParticleFilter:
    "JointParticleFilter tracks a joint distribution over tuples of all ghost positions."

    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initialize(self, gameState, legalPositions):
        "Stores information about the game, then initializes particles."
        self.numGhosts = gameState.getNumAgents() - 1
        self.ghostAgents = []
        self.legalPositions = legalPositions
        self.initializeParticles()

    def initializeParticles(self):
        """
        Initialize particles to be consistent with a uniform prior.
        Each particle is a tuple of ghost positions. Use self.numParticles for
        the number of particles. You may find the python package 'itertools' helpful.
        Specifically, you will need to think about permutations of legal ghost
        positions, with the additional understanding that ghosts may occupy the
        same space. Look at the 'product' function in itertools to get an
        implementation of the catesian product. Note: If you use
        itertools, keep in mind that permutations are not returned in a random order;
        you must shuffle the list of permutations in order to ensure even placement
        of particles across the board. Use self.legalPositions to obtain a list of
        positions a ghost may occupy.
          ** NOTE **
            the variable you store your particles in must be a list; a list is simply a collection
            of unweighted variables (positions in this case). Storing your particles as a Counter or
            dictionary (where there could be an associated weight with each position) is incorrect
            and will produce errors
        """
        "*** YOUR CODE HERE ***"
        possPositions = list(itertools.product(self.legalPositions, repeat = self.numGhosts))
        # print possPositions
        random.shuffle(possPositions)
        # if len(possPositions) >= self.numParticles:
        #     self.particles = possPositions[:selnumParticles]

        count, self.particles = 0, []
        while count < self.numParticles:
            for position in possPositions:
                if count < self.numParticles:
                    self.particles.append(position)
                    count += 1
                else:
                    break




    def addGhostAgent(self, agent):
        "Each ghost agent is registered separately and stored (in case they are different)."
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1);

    def observeState(self, gameState):
        """
        Resamples the set of particles using the likelihood of the noisy observations.
        To loop over the ghosts, use:
          for i in range(self.numGhosts):
            ...
        A correct implementation will handle two special cases:
          1) When a ghost is captured by Pacman, all particles should be updated so
             that the ghost appears in its prison cell, position self.getJailPosition(i)
             where "i" is the index of the ghost.
             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).
          2) When all particles receive 0 weight, they should be recreated from the
              prior distribution by calling initializeParticles. After all particles
              are generated randomly, any ghosts that are eaten (have noisyDistance of 0)
              must be changed to the jail Position. This will involve changing each
              particle if a ghost has been eaten.
        ** Remember ** We store particles as tuples, but to edit a specific particle,
        it must be converted to a list, edited, and then converted back to a tuple. Since
        this is a common operation when placing a ghost in the jail for a particle, we have
        provided a helper method named self.getParticleWithGhostInJail(particle, ghostIndex)
        that performs these three operations for you.
        """
        pacmanPosition = gameState.getPacmanPosition()
        noisyDistances = gameState.getNoisyGhostDistances()
        if len(noisyDistances) < self.numGhosts: return
        emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]

        "*** YOUR CODE HERE ***"
        allPossible = util.Counter()
        
        for particle_tuple in self.particles:
            prob = 1
            for i in range(0, self.numGhosts):
                if noisyDistances[i] is None: 
                    particle_tuple = self.getParticleWithGhostInJail(particle_tuple, i)
                else:
                    distance = util.manhattanDistance(particle_tuple[i], pacmanPosition)
                    prob *= emissionModels[i][distance]
            allPossible[particle_tuple] += prob

        self.beliefs = allPossible
        self.beliefs.normalize()
        # loop that goes over every value and checks if they are all zero
        AllWeightZero = False
        for value in self.beliefs.values() :
            if value == 0:
                AllWeightZero = True
                continue
            else:
                AllWeightZero = False
                break
        # Handle cases appropriately
        if not AllWeightZero:
            self.particles = []
            
            for x in range(0,self.numParticles):
                self.particles.append(util.sample(self.beliefs))
        else:
        
            self.initializeParticles()
            for particle_tuple in self.particles:
                for i in range(0,self.numGhosts):
                    if noisyDistances[i] is None:
                        particle_tuple = self.getParticleWithGhostInJail(particle_tuple, i)
                

        
        # allPossible = util.Counter()
        # for index, particle in enumerate(self.particles):
        #     partial = 1.0
        #     for i in range(self.numGhosts):
        #         if noisyDistances[i] == None: # Case 1
        #             particle = self.getParticleWithGhostInJail(particle, i)
        #         else:
        #             distance = util.manhattanDistance(particle[i], pacmanPosition)
        #             partial *= emissionModels[i][distance]
        #     allPossible[particle] += partial


        # if not any(allPossible.values()):
        #     self.initializeParticles()
        #     for index, particle in enumerate(self.particles):
        #         for i in range(self.numGhosts):
        #             if noisyDistances[i] == None:
        #                 particle = self.getParticleWithGhostInJail(particle, i)
        # else:
        #     allPossible.normalize()
        #     temp = []
        #     for _ in range(0, self.numParticles):
        #         temp.append(util.sample(allPossible))
        #     self.particles = temp

    def getParticleWithGhostInJail(self, particle, ghostIndex):
        particle = list(particle)
        particle[ghostIndex] = self.getJailPosition(ghostIndex)
        return tuple(particle)

    def elapseTime(self, gameState):
        """
        Samples each particle's next state based on its current state and the gameState.
        To loop over the ghosts, use:
          for i in range(self.numGhosts):
            ...
        Then, assuming that "i" refers to the index of the
        ghost, to obtain the distributions over new positions for that
        single ghost, given the list (prevGhostPositions) of previous
        positions of ALL of the ghosts, use this line of code:
          newPosDist = getPositionDistributionForGhost(setGhostPositions(gameState, prevGhostPositions),
                                                       i, self.ghostAgents[i])
        **Note** that you may need to replace "prevGhostPositions" with the
        correct name of the variable that you have used to refer to the
        list of the previous positions of all of the ghosts, and you may
        need to replace "i" with the variable you have used to refer to
        the index of the ghost for which you are computing the new
        position distribution.
        As an implementation detail (with which you need not concern
        yourself), the line of code above for obtaining newPosDist makes
        use of two helper functions defined below in this file:
          1) setGhostPositions(gameState, ghostPositions)
              This method alters the gameState by placing the ghosts in the supplied positions.
          2) getPositionDistributionForGhost(gameState, ghostIndex, agent)
              This method uses the supplied ghost agent to determine what positions
              a ghost (ghostIndex) controlled by a particular agent (ghostAgent)
              will move to in the supplied gameState.  All ghosts
              must first be placed in the gameState using setGhostPositions above.
              The ghost agent you are meant to supply is self.ghostAgents[ghostIndex-1],
              but in this project all ghost agents are always the same.
        """
        newParticles = []
        for oldParticle in self.particles:
            newParticle = list(oldParticle)
            "*** YOUR CODE HERE ***"
            for i in range(self.numGhosts):
                newPosDist = getPositionDistributionForGhost(setGhostPositions(gameState, newParticle),
                                                   i, self.ghostAgents[i])
                newParticle[i] = util.sample(newPosDist)
            "*** END YOUR CODE HERE ***"
            newParticles.append(tuple(newParticle))
        self.particles = newParticles

    def getBeliefDistribution(self):
        "*** YOUR CODE HERE ***"
        # distribution = util.Counter()
        # for element in self.particles:
        #     distribution[element] += 1.0
        # distribution.normalize()
        # return distribution

        dist = util.Counter()
        for position in self.legalPositions:
            dist[position] = 0
        #record how many times each position is occuring in self.Particles
        for positiontuple in self.particles:
            dist[positiontuple] +=1.0
        #normalize it and return
        dist.normalize()
        return dist

# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()

def getPositionDistributionForGhost(gameState, ghostIndex, agent):
    """
    Returns the distribution over positions for a ghost, using the supplied gameState.
    """

    # index 0 is pacman, but the students think that index 0 is the first ghost.
    ghostPosition = gameState.getGhostPosition(ghostIndex+1)
    actionDist = agent.getDistribution(gameState)
    dist = util.Counter()
    for action, prob in actionDist.items():
        successorPosition = game.Actions.getSuccessor(ghostPosition, action)
        dist[successorPosition] = prob
    return dist

def setGhostPositions(gameState, ghostPositions):
    "Sets the position of all ghosts to the values in ghostPositionTuple."
    for index, pos in enumerate(ghostPositions):
        conf = game.Configuration(pos, game.Directions.STOP)
        gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
    return gameState

