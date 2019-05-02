class FolderState:
    _oj: str
    _id: str
    _lang: str
    _up_lang: str

    def __init__(self, oj: str = '', sid: str = '', lang: str = '', up_lang: str = ''):
        self._oj = oj
        self._id = sid
        self._lang = lang
        self._up_lang = up_lang

    @property
    def oj(self):
        return self._oj

    @oj.setter
    def oj(self, value):
        self._oj = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

    @property
    def up_lang(self):
        return self._up_lang

    @up_lang.setter
    def up_lang(self, value):
        self._up_lang = value
