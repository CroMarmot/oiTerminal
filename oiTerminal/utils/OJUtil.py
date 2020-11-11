# TODO not important support lowercase and more, cf,codeforces,Codeforces -> Codeforces
class OJUtil(object):
    @staticmethod
    def short2full(short_name) -> str:
        ret = {
            "cf": platformsClassName.Codeforces,
            "ac": platformsClassName.AtCoder,
        }.get(short_name)
        if ret is None:
            raise Exception(f'not support oj short name "{short_name}"')
        return ret

    @staticmethod
    def get_supports():
        return [
            # 'Aizu',
            # 'HDU',
            # 'FZU', FZU 体验太差老是访问不了，还是不要支持好了
            # 'POJ',
            # 'WUST',
            # 'ZOJ',
            platformsClassName.Codeforces,
            platformsClassName.AtCoder,
        ]
