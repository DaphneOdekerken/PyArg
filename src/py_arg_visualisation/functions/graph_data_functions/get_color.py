def get_color(required_color: str, color_blind_mode: bool) -> str:
    if color_blind_mode:
        if required_color == 'gray':
            return '#dddddd'
        if required_color == 'blue':
            return '#6D90E3'
        if required_color == 'green':
            return '#2c7bb6'
        if required_color == 'yellow':
            return '#ffffbf'
        if required_color == 'red':
            return '#d7191c'
    else:
        if required_color == 'gray':
            return '#AAAAAA'
        if required_color == 'blue':
            return '#6DCDE3'
        if required_color == 'green':
            return '#2ac2ab'
        if required_color == 'yellow':
            return '#fff2cc'
        if required_color == 'red':
            return '#e60c3f'
    raise NotImplementedError
