class DomainError(Exception):
    pass

class UserAlreadyExistsError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass


class ExerciseNotFoundError(DomainError):
    pass


class InvalidMuscleError(DomainError):
    def __init__(self, missing_ids: set[int]):
        self.missing_ids = missing_ids
        super().__init__(f"Invalid muscle IDs: {missing_ids}")