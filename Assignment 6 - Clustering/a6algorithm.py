"""
Primary algorithm for k-Means clustering

This file contains the Algorithm class for performing k-means clustering.  While it is
the last part of the assignment, it is the heart of the clustering algorithm.  You
need this class to view the complete visualizer.

"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6dataset
import a6cluster

# Part A
def valid_seeds(value, size):
    """
    Returns True if value is a valid list of seeds for clustering.

    A list of seeds is a k-element list OR tuple of integersa between 0 and size-1.
    In addition, no seed element can appear twice.

    Parameter valud: a value to check
    Precondition: value can be anything

    Paramater size: The database size
    Precondition: size is an int > 0
    """
    # IMPLEMENT ME
    #enforce precondition
    assert type(size)==int and size>0

    #check for valid list of seeds and return Boolean accordingly
    good = True
    if type(value) == list or type(value) == tuple:
        for k in value:
            if type(k)==int and k>=0 and k<=size-1 and not value.count(k)>1:
                good = True
            else:
                return False
    else:
        return False
    return good


class Algorithm(object):
    """
    A class to manage and run the k-means algorithm.

    The method step() performs one step of the calculation.  The method run() will
    continue the calculation until it converges (or reaches a maximum number of steps).
    """
    # IMMUTABLE ATTRIBUTES (Fixed after initialization with no DIRECT access)
    # Attribute _dataset: The Dataset for this algorithm
    # Invariant: _dataset is an instance of Dataset
    #
    # Attribute _cluster: The clusters to use at each step
    # Invariant: _cluster is a non-empty list of Cluster instances

    # Part B
    def getClusters(self):
        """
        Returns the list of clusters in this object.

        This method returns the cluster list directly (it does not copy).  Any changes
        made to this list will modify the set of clusters.
        """
        # IMPLEMENT ME
        return self._cluster


    def __init__(self, dset, k, seeds=None):
        """
        Initializes the algorithm for the dataset ds, using k clusters.

        If the optional argument seeds is supplied, those seeds will be a list OR
        tuple of indices into the dataset. They specify which points should be the
        initial cluster centroids. Otherwise, the clusters are initialized by randomly
        selecting k different points from the database to be the cluster centroids.

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter k: the number of clusters
        Precondition: k is an int, 0 < k <= dset.getSize()

        Paramter seeds: the initial cluster indices (OPTIONAL)
        Precondition: seeds is None, or a list/tuple of valid seeds.
        """
        # IMPLEMENT ME
        #enforce preconditions
        assert isinstance(dset, a6dataset.Dataset)
        assert type(k)==int and k>0 and k<=dset.getSize()
        assert seeds is None or valid_seeds(seeds, dset.getSize())

        # If seeds is None, get random sample indices
        if seeds is None:
            seeds = random.sample(range(dset.getSize()),k)

        # Set dataset
        self._dataset=dset

        # Set cluster to empty list
        self._cluster = []
        for s in seeds:
            cl = a6cluster.Cluster(dset,dset.getPoint(s))
            self._cluster.append(cl)


    # Part C
    def _nearest(self, point):
        """
        Returns the cluster nearest to point

        This method uses the distance method of each Cluster to compute the distance
        between point and the cluster centroid. It returns the Cluster that is closest.

        Ties are broken in favor of clusters occurring earlier in the list returned
        by getClusters().

        Parameter point: The point to compare.
        Precondition: point is a tuple of numbers (int or float). Its length is the
        same as the dataset dimension.
        """
        # IMPLEMENT ME
        assert a6dataset.is_point(point)
        assert len(point) == self._dataset.getDimension()

        # Set the default nearestCluster to be the first cluster
        closestCluster = self._cluster[0]

        # Set the default nearestDistance to be the distance from the points
        # to the centroid of the first cluster
        closestDistance = closestCluster.distance(point)

        # Loop through all clusters, if the distance < nearestDistance, set
        # nearestDistance to the current distance and set the nearestCluster
        # to current cluster
        for x in self._cluster:
            distance = x.distance(point)
            if distance < closestDistance:
                closestDistance = distance
                closestCluster = x

        #return cluster nearest to point
        return closestCluster


    def _partition(self):
        """
        Repartitions the dataset so each point is in exactly one Cluster.
        """
        # First, clear each cluster of its points.
        for x in self._cluster:
            x.clear()

        #Then, for each point in the dataset,find the nearest cluster and
        #add the point to that cluster.
        for y in range(len(self._dataset.getContents())):
            nearest = self._nearest(self._dataset.getContents()[y])
            nearest.addIndex(y)


    # Part D
    def _update(self):
        """
        Returns True if all centroids are unchanged after an update; False otherwise.

        This method first updates the centroids of all clusters'.  When it is done, it
        checks whether any of them have changed. It returns False if just one has
        changed. Otherwise, it returns True.
        """
        # IMPLEMENT ME
        #loop through elements in cluster; append True/False according to
        #if centroids are updated
        for x in self._cluster:
            list = []
            if x.update() == True:
                list.append(True)
            else:
                list.append(False)

        #if just one has changed return False
        if list.count(True) >= 1:
            return True
        else:
            return False


    def step(self):
        """
        Returns True if the algorithm converges after one step; False otherwise.

        This method performs one cycle of the k-means algorithm. It then checks if
        the algorithm has converged and returns the appropriate result (True if
        converged, false otherwise).
        """
        # In a cycle, we partition the points and then update the means.
        # IMPLEMENT ME
        #repartition
        self._partition()

        #update
        return self._update()


    # Part D
    def run(self, maxstep):
        """
        Continues clustering until either it converges or performs maxstep steps.

        After the maxstep call to step, if this calculation did not converge, this
        method will stop.

        Parameter maxstep: The maximum number of steps to perform
        Precondition: maxstep is an int >= 0
        """
        # Call k_means_step repeatedly, up to maxstep times, until the
        #algorithm converges. Stop once you reach maxstep iterations even if
        #the algorithm has not converged.
        # You do not need a while loop for this.  Just write a for-loop,
        #and exit the for-loop (with a return) if you finish early.
        # IMPLEMENT ME
        #enforce precondition
        assert type(maxstep)==int and maxstep>=0

        #loop through indices in maxstep, check for convergence/max num steps
        for x in range(maxstep):
            if self.step()==True:
                return
