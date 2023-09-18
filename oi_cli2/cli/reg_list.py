from typing import Callable, Dict
from oi_cli2.cli.adaptor.AtCoderAdaptor import AtCoder, AtcoderGen
from oi_cli2.cli.adaptor.Codeforces.CodeforcesAdaptor import CodeforcesGen
from oi_cli2.cli.adaptor.Codeforces.Codeforces import Codeforces
from oi_cli2.model.Account import Account
from oi_cli2.model.BaseOj import BaseOj
from oi_cli2.utils.Provider2 import Provider2

reg_list: Dict[str, Callable[[Account, Provider2], BaseOj]] = {
    Codeforces.__name__: CodeforcesGen,
    AtCoder.__name__: AtcoderGen,
}
