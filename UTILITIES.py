
import re
import json

#==============================================================================#

INDENT = '   '

def dumpObj(obj, level=''):

    level += INDENT
    oType = type(obj)
#    print('[', oType, ']', end = '')
    if obj == None:
        print("[None]", end = "")
    elif oType is dict:
        print("\n" + level + '{', end = '')
        for ky in obj.keys():
            print("\n" + level + str(ky) + ": ", end='')
            dumpObj(obj[ky], level)
        print('\n' + level + '}', end = '')
    elif oType is list:
        print('[', end = '')
        for itm in obj:
            dumpObj(itm, level)
        print(' ]', end = '')
    elif oType is str:
        print(' ' + obj, end = '')
    elif oType is int:
        print(" {:d}".format(obj), end = '')
    elif oType is float:
        print(" {:.3f}".format(obj), end = '')
    elif oType is bool:
        print(" {}".format(obj), end = '')
    else:
        print(obj.__module__, obj.__class__.__name__, 'object:', end = '')
        dumpObj(obj.__dict__, level)
#        print('--', obj, end = '')

#==============================================================================#

class myEncoder(json.JSONEncoder):
    def default(self, obj):
        oType = type(obj)
#        print("==>", oType)
        m = re.match(r"<class\s+\'([^.]+)\.(\w+)\'>", str(oType))
        if m:
#            print("==>", m.group(2))
            obj.__dict__["_MODULE"] = m.group(1)
            obj.__dict__["_OBJ_CLASS"] = m.group(2)
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)

#==============================================================================#

def dumpJSON(filename, obj):

    f = open(filename, "w")
    s = json.dumps(obj, cls = myEncoder, indent = 3)
    f.write(s)
    f.close()

#==============================================================================#

def dumpJSONstr(obj):

    s = json.dumps(obj, cls = myEncoder, indent = 3)
    return s

#==============================================================================#

def myObjDecoder(d):
    obj = d
    moduleName = d.get("_MODULE")
    modClass = d.get("_OBJ_CLASS")
    if moduleName and modClass:
        module = __import__(moduleName)
        class_ = getattr(module, modClass)
        obj = class_()
        obj.__dict__ = d
    return obj

#==============================================================================#

def loadJSON(filename):
    f = open(filename, "r")
    obj = json.load(f, object_hook = myObjDecoder)
    f.close()
    return obj

#==============================================================================#

def select(dbX, tags):
#   print(dbX, "==>", tags)
   v = None
   k = tags.pop(0)
#  print(k)
   v = dbX.get(k)
   if v and (len(tags) > 0):
      v = select(v, tags)
   return v

#==============================================================================#

def insert(dbX, tags, v):
#   print("insert:", dbX, "==>", tags, "=", v)
   k = tags.pop(0)
#   print(k)
   d = dbX.get(k)
   if d == None:
      d = {}
      dbX[k] = d
   if len(tags) > 0:
      insert(d, tags, v)
   else:
      dbX[k] = v

#==============================================================================#

# test code

if __name__ == '__main__':

    import MEASUREMENT

    myData = {
               'N': {'TMAX': {0: 29.1, 1: 34.6, 2: -45.6, 3: 56.8}, 'TMIN': {0: 1.0, 1: 2.1, 2: -3.2, 3: 4.3}},
               'S': {'TMIN': {0: 26.0, 1: 43.1, 2: -5.2, 3: 5.3}, 'TMAX': {0: 79.1, 1: 74.6, 2: -75.6, 3: 76.8}}
            }

    print()
    dumpObj(myData)
    print("\n")

    print("select:", select(myData, ['N', 'TMIN', 2]))
    print("select:", select(myData, ['S', 'TMIN', 2]))

    print("select:", select(myData, ['Q', 'TMIN', 2]))
    print("select:", select(myData, ['N', 'TMAX', 3]))


    print("select:", select(myData, ['N', 'ZONK', 'TMAX', 3, 'HELP']))


    insert(myData, ['N', 'SNOW', 6], 6666.6)
    insert(myData, ['S', 'SNOW', 2], 2222.2)
    insert(myData, ['N', 'SNOW', 3], 3333.3)
    insert(myData, ['N', 'SNOW', 0], 0.0)

    insert(myData, ['E', 'SNOW', 6], 6666.6)
    insert(myData, ['E', 'SNOW', 2], 2222.2)
    insert(myData, ['W', 'SNDP', 3], 3333.3)
    insert(myData, ['W', 'SNDP', 0], 0.0)

    print("\nmyData = ", end = "")
    dumpObj(myData)
    print()

    print("\nmyData = ", end = "")
    print(dumpJSONstr(myData))
    print()
