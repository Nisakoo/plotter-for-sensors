class Sensor:
    def __init__(self, id, name=None):
        self.id = id

        self.rescale = False
        self.max_value = 0.0
        self.min_value = 0.0

        self.scale_max = 0.0
        self.scale_min = 0.0

        self.bias = 0.0
        
        if name is None:
            self.name = f"Неизвестный ({self.id})"
        else:
            self.name = name

    def set_name(self, new_name: str) -> None:
        self.name = new_name

    def to_scale(self, values: list) -> list:
        if self.rescale:
            new_values = list()
            dt = self.max_value - self.min_value
            new_dt = self.scale_max - self.scale_min

            for value in values:
                new_values.append(
                    round(new_dt * (value + self.bias) / (dt + 1e-7) + self.scale_min, 3)
                )

            return new_values
        
        return values
    
    def __repr__(self):
        return self.name