# -*- coding: utf-8 -*-
"""
Utility functions for rotated-rectangle collision maths.
Assumes a coordinate system wherein the positive x-axis faces to the left,
while the positive y-axis faces down (as used in pygame).

Created on Thu Oct 13 12:17:28 2022

@author: Tumbl
"""
from numpy import sign, sqrt


def pointLineSide(start, end, point):
    """
    Determines on which side of the given line the point is.
    Credit to LibGDX.Intersector class.

    Parameters
    ----------
    start : float array
        The start of the line.
        [0]: x-coordinate of the start.
        [1]: y-coordinate of the start.
    end : float array
        The end of the line.
        [0]: x-coordinate of the end.
        [1]: y-coordinate of the end.
    point : float array
        The point to test.
        [0]: x-coordinate of the point.
        [1]: y-coordinate of the point.

    Returns
    -------
    int
        1 if the point is to the left of the line,
        -1 if it is to the right,
        or 0 if it is on the line.
        Left and right are relative to the line's direction which goes from start to end.
    
    """
    return sign((end[0] - start[0]) * -(point[1] - start[1]) - -(end[1] - start[1]) * (point[0] - start[0]))

def distanceSegmentPoint2(start, end, point):
    """
    Finds the shortest squared distance between a point and a line segment.
    Credit to LibGDX.Intersector class.

    Parameters
    ----------
    start : float array
        The start of the line.
        [0]: x-coordinate of the start.
        [1]: y-coordinate of the start.
    end : float array
        The end of the line.
        [0]: x-coordinate of the end.
        [1]: y-coordinate of the end.
    point : float array
        The point.
        [0]: x-coordinate of the point.
        [1]: y-coordinate of the point.

    Returns
    -------
    float
        The shortest distance from the line segment to the point, squared.

    """
    length2 = (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
    
    if length2 == 0:
        return (point[0] - start[0]) ** 2 + (point[1] - start[1]) ** 2
    
    t = ((point[0] - start[0]) * (end[0] - start[0]) + (point[1] - start[1]) * (end[1] - start[1])) / length2
    
    if t <= 0:
        # Point is 'before' the start of the line segment, so closest to the startpoint.
        return (point[0] - start[0]) ** 2 + (point[1] - start[1]) ** 2
    if t >= 1:
        # Point is 'past' the end of the line segment, so closest to the endpoint.
        return (point[0] - end[0]) ** 2 + (point[1] - end[1]) ** 2
    
    nearest = [
        start[0] + t * (end[0] - start[0]),
        start[1] + t * (end[1] - start[1])]
    
    return (point[0] - nearest[0]) ** 2 + (point[1] - nearest[1]) ** 2
