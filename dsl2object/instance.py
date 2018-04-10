class Instance:
    def __init__(self, name, identifier = ""):
        self.name = name
        self.identifier = identifier

    def full_name(self):
        if len(self.identifier) > 0:
            return "{} {}".format(self.name, self.identifier)
        else:
            return self.name


class InstanceFactory:
    """Takes a string in format "<first part> <second part>" or "<single part>"
    and creates an instances."""
    def createInstances(self,d):
        data = d.split()
        if len(data) == 2:
            delimited = data[1].split("/")
            return [ Instance(data[0], d) for d in delimited ]
        else:
            return [ Instance(data[0]) ]