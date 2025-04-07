from geopy.distance import geodesic

def is_within_radius(student_coords, class_coords, max_distance_m=50):
    distance = geodesic(student_coords, class_coords).meters
    return distance <= max_distance_m
