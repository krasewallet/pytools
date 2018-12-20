#coding:utf-8
import argparse
import PIL.Image
import re

def imageTool(options):
  img = PIL.Image.open(options.source)
  if options.bk:
    p = PIL.Image.new('RGBA', img.size, (255,255,255))
    p.paste(img, (0, 0, img.size[0],img.size[1]), img)
    img = p
  maps = {}
  if options.icon_size:
    maps["sizes"] = [(options.icon_size,options.icon_size)]
  if options.scale:
    m = re.match(r"(\d+)\*(\d+)",options.scale)
    img = img.resize(tuple(map(int,m.groups())))
  img.save(options.output,**maps)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="python image tools")
  parser.add_argument("source")
  parser.add_argument("output")
  parser.add_argument("--scale") 
  parser.add_argument("--icon_size",type=int)
  parser.add_argument("--bk")

  args = parser.parse_args()

  imageTool(args)