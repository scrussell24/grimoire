class GrimoireInvalidOption(Exception):
    def __init__(self, option):
        super().__init__(
            f"Option ({option.__name__}) is a function. Remember to include"
            " the option as an argument to your page function"
        )


class GrimoireUnknownPageOptions(Exception):
    def __init__(self, options):
        super().__init__(
            f"Unknown page options: {options}. Make sure the options match the "
            " name of an existing page function."
        )


class GrimoireNoStartPage(Exception):
    def __init__(self):
        super().__init__(
            f"No start page was added. Remember to include the keyword arg"
            " start=True to your stories first page."
        )
