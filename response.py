class Response:
    def __init__(self, request):
        self.res = {
            'session': request.json['session'],
            'version': request.json['version'],
            'response': {
                'end_session': False
            }
        }

    def addText(self, text):
        if not 'text' in self.res['response']:
            self.res['response']['text'] = text
        else:
            self.res['response']['text'] += ' ' + text

    def addButton(self, title):
        if not 'buttons' in self.res['response']:
            self.res['response']['buttons'] = []

        self.res['response']['buttons'].append(
            {
                'title': title,
                'hide': True
            })
