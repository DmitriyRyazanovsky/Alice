class Response:
    def __init__(self, request):
        self.res = {
            'session': request.json['session'],
            'version': request.json['version'],
            'response': {
                'end_session': False,
                'buttons': []
            }
        }

    def setText(self, text):
        self.res['response']['text'] = text

    def addButton(self, title):
        self.res['response']['buttons'].append(
            {
                'title': title,
                'hide': True
            })
