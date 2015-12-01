def add_newline_at_end_if_missing(string):
    if string[-2:] != "\n":
        string += "\n"
    return string
