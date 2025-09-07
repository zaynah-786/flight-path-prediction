the core of this project is the haversine formula - this formula is used to find the shortest distance between two points on the surface of a sphere (the Earth), also known as the "great-circle distance", this is a more accurate way to measure distance than using a flat map, especially over long distances.

the haversine formula is a direct application of the law of haversines from spherical trigonometry, the formula can be broken down into three main parts, which are then implemented in the code.

1. calculating a

this first step calculates a value that represents the square of half the central angle between the two points.

a = sin²(Δφ/2) + cos(φ₁)⋅cos(φ₂)⋅sin²(Δλ/2)

φ₁, φ₂: the latitudes of the two points.
λ₁, λ₂: the longitudes of the two points.
Δφ: the difference in latitude.
Δλ: the difference in longitude.

2. calculating c
the second step uses the value of a to find the actual central angle c in radians.

c = 2 * atan2(√a, √(1-a))

3. calculating distance d
lastly, we multiply the central angle c by the radius of the Earth r to get the final distance d.

d = r * c
