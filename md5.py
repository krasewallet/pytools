import hashlib

def getFileMD5(f):
  with open(f, "rb") as fp:
    md5 = hashlib.md5()
    md5.update(fp.read())
    _hash = md5.hexdigest()
  return f'{_hash}'

if __name__ == "__main__":
  md5 = getFileMD5("3dd36cdd-7846-4aa2-bae3-347be47b6397.xfdp")
  print(md5)