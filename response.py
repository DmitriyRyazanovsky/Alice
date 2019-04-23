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

    def setText(self, text):
        self.res['response']['text'] = text

    def addButton(self, title, url=None):
        if not 'buttons' in self.res['response']:
            self.res['response']['buttons'] = []

        button = {}
        button['title'] = title
        if url:
            button['url'] = url
        button['hide'] = True

        self.res['response']['buttons'].append(button)

    def setImage(self, id, title=None):
        self.res['response']['card'] = {}
        self.res['response']['card']['type'] = 'BigImage'
        if title:
            self.res['response']['card']['title'] = title
        self.res['response']['card']['image_id'] = id

    def endSession(self):
        self.res['response']['end_session'] = True
