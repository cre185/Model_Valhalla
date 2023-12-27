

class DateTimeFormater:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self.format_datetime(response.data)
            response._is_rendered = False
            response.render()
        except BaseException:
            pass
        return response

    def format_datetime(self, data):
        if isinstance(data, list):
            for item in data:
                self.format_datetime(item)
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(key, str) and key == 'add_time':
                    data[key] = value.split(
                        'T')[0] + ' ' + value.split('T')[1][:5]
                self.format_datetime(value)
