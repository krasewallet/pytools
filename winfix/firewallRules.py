import winreg,urllib.parse,os,argparse
baseRegPath = r'SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\FirewallRules'

def rmRulesByDir(folder):
  key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE,baseRegPath,access=winreg.KEY_ALL_ACCESS )
  i = 0
  subDels = []
  while True:
    try:
      name, value, regType = winreg.EnumValue(key, i)
      rules = value.split('|')
      rulesDict = {}
      for rule in rules:
        rulesDict.update(urllib.parse.parse_qsl(rule,keep_blank_values=True))
      if 'App' in rulesDict:
        print(rulesDict['App'],f'{folder}')
        pos = rulesDict['App'].find(f'{folder}')
        if pos == 0:
          subDels.append(name)
    except Exception as e:
      break
    finally:
      i += 1
  for subkey in subDels:
    winreg.DeleteValue(key,subkey)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    args = parser.parse_args()
    rmRulesByDir(args.folder)