class NearEarthObject:

    def __init__(self, id, name, estimated_size, distance, approach_date):
        self.id = id
        self.name = name
        self.estimated_size = estimated_size
        self.distance = distance
        self.approach_date = approach_date

    def get_info(self):
        return self.id + ' ' + self.name + ' ' + str(self.estimated_size) + ' ' + \
               str(self.distance) + ' ' + self.approach_date


def get_near_earth_object_from_dict(data):
    id = data['id']
    name = data['name']
    estimated_size = data['estimated_diameter']
    approach_date = data['close_approach_data'][0]['close_approach_date']
    distance = data['close_approach_data'][0]['miss_distance']
    return NearEarthObject(id, name, estimated_size, distance, approach_date)
