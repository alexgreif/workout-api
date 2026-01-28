class InvalidMuscleError(Exception):
    def __init__(self, missing_ids: set[int]):
        self.missing_ids = missing_ids
        super().__init__(f"Invalid muscle IDs: {missing_ids}")