"""
Cluster class for k-Means clustering

This file contains the class cluster, which is the second part of the assignment.  With
this class done, the visualization can display the centroid of a single cluster.

"""
import math
import random
import numpy


# For accessing the previous parts of the assignment
import a6dataset


class Cluster(object):
    """
    A class representing a cluster, a subset of the points in a dataset.

    A cluster is represented as a list of integers that give the indices in the dataset
    of the points contained in the cluster.  For instance, a cluster consisting of the
    points with indices 0, 4, and 5 in the dataset's data array would be represented by
    the index list [0,4,5].

    A cluster instance also contains a centroid that is used as part of the k-means
    algorithm.  This centroid is an n-D point (where n is the dimension of the dataset),
    represented as a list of n numbers, not as an index into the dataset. (This is because
    the centroid is generally not a point in the dataset, but rather is usually in between
    the data points.)
    """
    # IMMUTABLE ATTRIBUTES (Fixed after initialization with no DIRECT access)
    # Attribute _dataset: The Dataset for this cluster
    # Invariant: _dataset is an instance of Dataset
    #
    # Attribute _centroid: The centroid of this cluster
    # Invariant: _centroid is a point (tuple of int/float) whose length is
    #equal to the dimension of _dataset.
    #
    # MUTABLE ATTRIBUTES (Can be changed at any time, via addIndex, or clear)
    # Attribute _indices: the indices of this cluster's points in the dataset
    # Invariant: _indices is a list of ints. For each element ind in _indices,
    # 0 <= ind < _dataset.getSize()

    # Part A
    def getIndices(self):
        """
        Returns the indices of points in this cluster

        This method returns the indices directly (not a copy). Any changes made to this
        list will modify the cluster.
        """
        # IMPLEMENT ME
        return self._indices


    def getCentroid(self):
        """
        Returns the centroid of this cluster.

        This getter method is to protect access to the centroid, and prevent someone
        from changing it accidentally. Because the centroid is a tuple, it is not
        necessary to copy the centroid before returning it.
        """
        # IMPLEMENT ME
        return self._centroid


    def __init__(self, dset, centroid):
        """
        Initializes a new empty cluster with the given centroid

        Parameter dset: the dataset
        Precondition: dset is an instance of Dataset

        Parameter centroid: the cluster centroid
        Precondition: centroid is a tuple of dset.getDimension() numbers
        """
        # IMPLEMENT ME
        #enforce preconditions
        assert isinstance(dset,a6dataset.Dataset)
        assert a6dataset.is_point(centroid)
        assert len(centroid) == dset.getDimension()

        #set attributes for a new empty cluster
        self._dataset = dset
        self._indices = []
        self._centroid = centroid


    def addIndex(self, index):
        """
        Adds the given dataset index to this cluster.

        If the index is already in this cluster, this method leaves the
        cluster unchanged.

        Precondition: index is a valid index into this cluster's dataset.
        That is, index is an int >= 0, but less than the dataset size.
        """
        # IMPLEMENT ME
        assert type(index)==int and index>=0 and index<self._dataset.getSize()
        if index not in self._indices:
            self._indices.append(index)


    def clear(self):
        """
        Removes all points from this cluster, but leaves the centroid unchanged.
        """
        # IMPLEMENT ME
        self._indices.clear()


    def getContents(self):
        """
        Returns a new list containing copies of the points in this cluster.

        The result is a list of points (tuples of int/float). It has to be computed
        from the list of indices.
        """
        # IMPLEMENT ME
        #accumulator
        newlist = []

        #loop through cluster point indices
        for x in self._indices:
            newlist.append(self._dataset.getPoint(x))
        return newlist


    # Part B
    def distance(self, point):
        """
        Returns the euclidean distance from point to this cluster's centroid.

        Parameter point: The point to be measured
        Precondition: point is a tuple of numbers (int or float), with the same dimension
        as the centroid.
        """
        # IMPLEMENT ME
        assert a6dataset.is_point(point) and len(point) == len(self._centroid)

        #accumulators
        accumulator = []
        substract = 0

        #loop through point's indices, subtract cluster's centroid from point
        for x in range(len(point)):
            subtract = point[x]-self._centroid[x]
            accumulator.append((subtract)**2)

        #accumulator
        sum = 0

        #loop through elements in accumulator, add differences
        for x in accumulator:
            sum = sum + x

        #return distance
        return math.sqrt((sum))


    def getRadius(self):
        """
        Returns the maximum distance from any point in this cluster, to the centroid.

        This method loops over the contents of this cluster to find the maximum distance
        from the centroid.
        """
        # IMPLEMENT ME
        #accumulators
        max = 0
        distance = 0

        #loop through cluster contents, find max distance
        for x in self.getContents():
            distance = self.distance(x)
            if distance > max:
                max = distance

        #return max distance
        return max


    def update(self):
        """
        Returns True if the centroid remains the same after recomputation; False otherwise.

        This method recomputes the centroid of this cluster. The new centroid is the
        average of the of the contents (To average a point, average each coordinate
        separately).

        Whether the centroid "remained the same" after recomputation is determined by
        numpy.allclose. The return value should be interpreted as an indication of
        whether the starting centroid was a "stable" position or not.

        If there are no points in the cluster, the centroid. does not change.
        """
        # IMPLEMENT ME
        #if no points centroid doesn't change, return true
        if len(self.getContents()) == 0:
            return True

        #placeholder of new centroid
        newCent = []

        #First set each coordinator in the new point to be 0
        for i in range(self._dataset.getDimension()):
            newCent.append(0)

        #Then get the sum of the first coordinates of all the points in the
        #cluster then second coordinates, third and so on
        for i in range(len(newCent)):
            for j in range(len(self.getContents())):
                newCent[i] = self.getContents()[j][i] + newCent[i]

        #For each coordinate in the new centroid point, divide by the number of
        #points
        for i in range(len(newCent)):
            newCent[i] = newCent[i]/len(self.getContents())

        #Check if the new centroid is the same as the old, if yes return True
        if numpy.allclose(list(self._centroid), newCent) == True:
            return True
        #If changed, change the centroid to be new one, and return False
        else:
            self._centroid = newCent
            return False


    # PROVIDED METHODS: Do not modify!
    def __str__(self):
        """
        Returns a String representation of the centroid of this cluster.
        """
        return str(self._centroid)+':'+str(self._indices)

    def __repr__(self):
        """
        Returns an unambiguous representation of this cluster.
        """
        return str(self.__class__) + str(self)
