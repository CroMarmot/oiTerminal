from oiTerminal.utils.enc import AESCipher


def test_enc():
    pwd = 'password'
    msg = 'message'
    # different result each time
    assert (AESCipher(pwd).encrypt(msg) != AESCipher(pwd).encrypt(msg))
    # successful decode
    assert (msg == AESCipher(pwd).decrypt(AESCipher(pwd).encrypt(msg)))


def test_enc_longger():
    pwd = 'passwo rdoi Terminalhey'
    msg = 'm中文LVIUGD essage *&G#IBV)(!&_)RYP(GBP*&T_#*'
    # different result each time
    assert (AESCipher(pwd).encrypt(msg) != AESCipher(pwd).encrypt(msg))
    # successful decode
    assert (msg == AESCipher(pwd).decrypt(AESCipher(pwd).encrypt(msg)))
