# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:53:47 2022

@author: Tumbl
"""

from numpy import sqrt, pi, sin, cos, arctan

from util import pointLineSide, distanceSegmentPoint2

class RotatedRectangle:
    """
    Object for storing a rotatable rectangle.
    Assumes a coordinate system wherein the positive x-axis faces to the left,
    while the positive y-axis faces down (as used in pygame).
    """

    def __init__(self, x, y, length, thickness):
        """
        Creates a new RotatedRectangle centred on a given point,
        with a rotation of zero ('length' going along the x-axis,
        'thickness' going along the y-axis), initialising the corner-points too.

        Parameters
        ----------
        x : float
            The horizontal centre of the rectangle.
        y : TYPE
            The vertical centre of the rectangle (increasing y moving downwards).
        length : float
            The length of the rectangle (dimension parallel to its axis of rotation).
        thickness : float
            The thickness of the rectangle (dimension perpendicular to its axis of rotation).

        Returns
        -------
        None.

        """
        # coordinates of the centre
        self.x = x
        self.y = y

        # dimensions of the rectangle
        self.length = length  # (horizontal width when rotation = 0)
        self.thickness = thickness  # (vertical width when rotation = 0)

        # useful for calculating where the points should be
        self.hypotenuse = sqrt((0.5 * length) ** 2 + (0.5 * thickness) ** 2)
        self.angleOffset = arctan(thickness / length)

        # in radians, measured anticlockwise from the positive x-axis
        self.rotation = 0

        self.points = [None, None, None, None]

        self.set_rotation(0)

    def set_rotation(self, new_rotation):
        """
        Sets the rotation of the rectangle to a new rotation (measured in radians, anticlockwise from the positive x-axis).

        Parameters
        ----------
        new_rotation : float
            The angle in radians anticlockwise from the positive x-axis to the new rotation angle.

        Returns
        -------
        None.

        """
        self.rotate(new_rotation - self.rotation)
    
    def set_position(self, new_x, new_y):
        """
        Re-centers the rectangle on a given point, translating all boundary points along with it.

        Parameters
        ----------
        new_x : float
            The x-coordinate of the new centrepoint.
        new_y : float
            The y-coordinate of the new centrepoint.

        Returns
        -------
        None.

        """
        self.move(new_x - self.x, new_y - self.y)

    def rotate(self, angle):
        """
        Rotates the rectangle by a given angle (measured in radians, anticlockwise from the positive x-axis).

        Parameters
        ----------
        angle : float
            The angle in radians anticlockwise from the positive x-axis to the add to the current rotation.

        Returns
        -------
        None.

        """
        self.rotation = self.rotation + angle

        self.points[0] = [
            self.x + self.hypotenuse * cos(
                self.rotation + self.angleOffset),
            self.y - self.hypotenuse * sin(
                self.rotation + self.angleOffset)]
        self.points[1] = [
            self.x + self.hypotenuse * cos(
                self.rotation - self.angleOffset),
            self.y - self.hypotenuse * sin(
                self.rotation - self.angleOffset)]
        self.points[2] = [
            self.x + self.hypotenuse * cos(
                self.rotation + pi + self.angleOffset),
            self.y - self.hypotenuse * sin(
                self.rotation + pi + self.angleOffset)]
        self.points[3] = [
            self.x + self.hypotenuse * cos(
                self.rotation + pi - self.angleOffset),
            self.y - self.hypotenuse * sin(
                self.rotation + pi - self.angleOffset)]

    def move(self, delta_x, delta_y):
        """
        Moves the rectangle by a given amount, translating all boundary points along with it.

        Parameters
        ----------
        delta_x : float
            How far to move in the x-direction.
        delta_y : float
            How far to move in the y-direction.

        Returns
        -------
        None.

        """
        self.x = delta_x
        self.y = delta_y
        
        for i in range(4):
            self.points[i][0] += delta_x
            self.points[i][1] += delta_y
            
    def contains_point(self, point):
        """
        Check whether a point is inside the rectangle.

        Parameters
        ----------
        point : float array
            The point to test.
            [0]: x-coordinate of the point.
            [1]: y-coordinate of the point.

        Returns
        -------
        bool
            True if the point is inside the rectangle, otherwise False.

        """
        for i in range(4):
            if i < 3:
                if pointLineSide(self.points[i], self.points[i + 1], point) > 0:
                    return False
            elif pointLineSide(self.points[i], self.points[0], point) > 0:
                return False
        
        return True
    
    def overlaps_circle(self, centre, radius):
        """
        Check whether there is any overlap between a circle and the rectangle.

        Parameters
        ----------
        centre : float array
            The centre of the circle.
            [0]: x-coordinate of the centre.
            [1]: y-coordinate of the centre.
        radius : float
            The radius of the circle.

        Returns
        -------
        bool
            True if the centre of the circle is inside the rectangle
            and/or the circle covers any of the boundary lines of the rectangle, otherwise False.

        """
        if self.contains_point(centre):
            return True
        
        for i in range(4):
            if i < 3:
                if distanceSegmentPoint2(self.points[i], self.points[i + 1], centre) <= radius ** 2:
                    return True
            elif distanceSegmentPoint2(self.points[i], self.points[0], centre) <= radius ** 2:
                return True
        
        return False
    
    def overlaps_rot_rect(self, other):
        """
        Check whether there is any overlap between this RotatedRectangle and another.
        Note that it is sufficient to check whether any or the corner points of each
        rectangle are contained within the other rectangle.

        Parameters
        ----------
        other : RotatedRectangle
            The rotated rectangle to test.

        Returns
        -------
        bool
            True if the rectangles overlap, otherwise False.

        """
        for point in other.points:
            if self.contains_point(point):
                return True
        for point in self.points:
            if other.contains_point(point):
                return True
        return False
        
