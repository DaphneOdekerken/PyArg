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
        if required_color == 'light-green':
            return '#4c9bd6'
        if required_color == 'light-red':
            return '#ff393c'
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
        if required_color == 'light-green':
            return '#4ae2cb'
        if required_color == 'light-red':
            return '#ff2c5f'
    if required_color == 'black':
        return '#000000'
    raise NotImplementedError
