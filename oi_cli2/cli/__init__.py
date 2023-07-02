from oi_cli2.custom.AtCoder.AtCoder import AtCoder
from oi_cli2.custom.Codeforces.Codeforces import Codeforces

from oi_cli2.cli.adaptor.AtcoderAdaptor import AtcoderGen
from oi_cli2.cli.adaptor.CodeforcesAdaptor import CodeforcesGen

reg_list = [
    [Codeforces.__name__, CodeforcesGen],
    [AtCoder.__name__, AtcoderGen],
]