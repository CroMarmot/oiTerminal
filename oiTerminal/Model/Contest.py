from typing import Dict
from oiTerminal.Model.Problem import Problem


class Contest:
    def __init__(self, cid: str):
        self._id = cid
        self.problems: Dict[str, Problem] =

    @property
    def id(self):
        return self._id
