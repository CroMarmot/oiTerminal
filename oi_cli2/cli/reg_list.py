from typing import Callable, Dict, List, Tuple, Union
from oi_cli2.cli.adaptor.AtCoderAdaptor import AtCoder, AtcoderGen
from oi_cli2.cli.adaptor.CodeforcesAdaptor import CodeforcesGen
from oi_cli2.custom.Codeforces.Codeforces import Codeforces
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.Provider2 import Provider2

reg_list: Dict[str, Callable[[Account, Provider2], BaseOj]] = {
    Codeforces.__name__: CodeforcesGen,
    AtCoder.__name__: AtcoderGen,
}