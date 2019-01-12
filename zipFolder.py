#coding:utf-8
import zipfile
import argparse
import os

def zipFolder(baseDir,zip_name):
  z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
  for dirpath, dirnames, filenames in os.walk(baseDir):
    fpath = dirpath.replace(baseDir,'') #这一句很重要，不replace的话，就从根目录开始复制
    for filename in filenames:
      z.write(os.path.join(dirpath, filename),os.path.join(fpath, filename))
      print(os.path.join(dirpath, filename))
  z.close()

def unzip(zip_name,baseDir):
  z = zipfile.ZipFile(zip_name, 'r')
  z.extractall(path=baseDir)
  z.close()

if __name__ =="__main__":
  parser = argparse.ArgumentParser(description="python zip/unzip tools")
  parser.add_argument("src")
  parser.add_argument("dst")
  parser.add_argument("-u","--unzip",action="store_true")
  args = parser.parse_args()
  if args.unzip:
    unzip(args.src,args.dst)
  else:
    zipFolder(args.src,args.dst)