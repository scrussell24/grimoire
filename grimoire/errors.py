class GrimoireInvalidOptionError(Exception):
    def __init__(self, option):
        super().__init__(
            f"Option ({option.__name__}) is a function. Remember to include"
            "the option as an argument to your page function"
        )
