def get_color(required_color: str, color_blind_mode: bool) -> str:
    if color_blind_mode:
        if required_color == 'gray':
            return '#919191'
        if required_color == 'blue':
            return '#6D90E3'
        if required_color == 'dark-blue':
            return '#3D60B3'
        if required_color == 'green':
            return '#40cfff'
        if required_color == 'yellow':
            return '#FEFE62'
        if required_color == 'red':
            return '#ffb763'
        if required_color == 'light-green':
            return '#a6e9ff'
        if required_color == 'light-red':
            return '#ffe6c9'
        if required_color == 'dark-yellow':
            return '#f1dd4b'
    else:
        if required_color == 'gray':
            return '#DDDDDD'
        if required_color == 'blue':
            return '#6DCDE3'
        if required_color == 'dark-blue':
            return '#3D60B3'
        if required_color == 'green':
            return '#2ac2ab'
        if required_color == 'yellow':
            return '#fff2cc'
        if required_color == 'dark-yellow':
            return '#AAAA00'
        if required_color == 'red':
            return '#e60c3f'
        if required_color == 'light-green':
            return '#82e3d5'
        if required_color == 'light-red':
            return '#f76e8e'
    if required_color == 'black':
        return '#000000'
    raise NotImplementedError
