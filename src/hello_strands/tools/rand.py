from strands import tool


@tool
def get_rand_message():
    """Return a random silly message for the user.

    Use this whenever the user asks for a funny message, a random message,
    something to cheer them up, or just wants to see what you come up with.
    Do not use for serious or informational requests.

    Returns:
        A short, silly message string.
    """
    return "CAT IN THE HAT IS A FAT CAT"
