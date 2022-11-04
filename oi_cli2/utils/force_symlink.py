import os
import errno


def force_symlink(src: str, dst: str):
  try:
    os.symlink(src, dst)
  except OSError as e:
    if e.errno == errno.EEXIST:
      os.remove(dst)
      os.symlink(src, dst)
