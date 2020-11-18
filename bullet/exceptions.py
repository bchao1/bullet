class MissingDependenciesError(Exception):
    def __init__(self, missing_dependencies):
        message = " ".join(
            [
                (
                    "'{dependant}' depends on '{dependency}' but '{dependency}' "
                    "was not provided."
                ).format(dependant=dependant, dependency=dependency)
                for dependant, dependency in missing_dependencies
            ]
        )
        super().__init__(message)
