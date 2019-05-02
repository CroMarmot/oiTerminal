from typing import Dict
from oiTerminal.Model.Problem import Problem


class Contest:
    def __init__(self, cid: str):
        self._id = cid
        self._problems: Dict[str, Problem] = {}
        self._name: str = ''
        self._url: str = ''

    @property
    def id(self):
        return self._id

    def addProblem(self, p:Problem):
        self._problems[p.id] = p

