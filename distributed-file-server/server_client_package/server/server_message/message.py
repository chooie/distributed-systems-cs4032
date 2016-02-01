from collections import OrderedDict


def remove_empty_elements(arr):
    return filter(None, arr)


def remove_whitespace_from_elements(arr):
    return map(lambda x: x.strip(), arr)


def message_to_dict(message):
    message_dict = OrderedDict()
    message_lines = message.split('\n')

    # Remove empty elements
    message_lines = remove_empty_elements(message_lines)
    for message_line in message_lines:
        line_words = message_line.split(':')
        line_words = remove_whitespace_from_elements(line_words)

        key = line_words[0]
        value = line_words[1]

        message_dict[key] = value
    return message_dict


def get_message_dict_type(values):
    return values.keys()[0]
