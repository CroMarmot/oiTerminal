class FakeCipher:
  def encrypt(self, data: str) -> str:
    return '[' + data + ']'

  def decrypt(self, data: str) -> str:
    return data[1:-1]
