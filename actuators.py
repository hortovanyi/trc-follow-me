class Actuators:
    def __init__(self):
        self.steering = 0.0     # normalised steering values [-1,1]

        self.counter = 0.0  # TODO remove - just for testing
        self.incrementor = 0.1

    def update(self, data):
        print(data)
        ds = str(data).split(',')
        if ds[0].startswith("steering"):
            self._steering_update(ds)

        # TODO remove this - only used for testing
        self.steering = self.counter
        self.counter += self.incrementor
        if self.counter > 0.99:
            self.incrementor = -0.1
        elif self.counter < -0.99:
            self.incrementor = 0.1

    def _steering_update(self, data):
        try:
            self.steering = float(data[1])

        except ValueError:
            print("%s isnt a float for steering" % (data[1]))

    def __str__(self):
        return "<Actuators: steering: %f />" % (self.steering)
