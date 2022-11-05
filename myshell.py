import zipfile
import sys

def checkDirectory(addres,pWay,allFiles):
    if addres=="~":
        return ""
    elif addres==".." or addres=="-":
        if addres=='':
            return pWay
        else:
            pWay="/"+pWay
            k=len(pWay)-1
            while pWay[k]!="/":
                pWay=pWay[:-1]
                k-=1
            pWay=pWay[:-1]
            pWay=pWay[1:]
            return pWay
    elif  "/root" in addres:
        addres=addres.replace("/root",'')
        if addres in allFiles:
            return addres
        return "cd: can't cd to "+addres+": No such file or directory"
    elif pWay=='' and (addres+'/') in allFiles:
        return addres
    elif pWay+'/'+addres+'/' in allFiles:
        return pWay+'/'+addres
    else:
        return "cd: can't cd to "+addres+": No such file or directory"

def checkFile(addres,pWay,allFiles):
    if  "/root" in addres:
        addres=addres.replace("/root/",'')
        if addres in allFiles:
            return addres
        return "cat: can't open "+addres+": No such file or directory"
    elif pWay+'/'+addres in allFiles:
        return pWay+'/'+addres
    else:
        return "cat: can't open "+addres+": No such file or directory"

def CAT(outAdr,nameArch):
    with zipfile.ZipFile(nameArch) as myzip:
        with myzip.open(outAdr,'r') as myfile:
            lines = [x.decode('utf8').strip() for x in myfile.readlines()]#декод в текст
            for line in lines:
                print(line)

def PWD(help_way):
    if help_way=="":
        print ("/root")
    else:
        print("/root/"+help_way+"/")


def ls(wayL,allFiles):
    counter=wayL.count('/')
    wayL+='/'
    for i in allFiles:
        if wayL=='/':
            if wayL in i and i!=wayL:
                if counter== (i.count('/')):
                    if i[-1]!='/':
                        print(i[len(wayL):],end="    ")
                    else:
                        print(i[len(wayL)-1:-1],end="    ")
                elif (counter== ((i.count('/')-1)) and (i[-1]=='/')):
                    print(i[len(wayL)-1:-1],end="    ")
        else:
            if wayL in i and i!=wayL:
                if counter== (i.count('/')-1):
                    if i[-1]!='/':
                        print(i[len(wayL):],end="    ")
                    else:
                        print(i[len(wayL)-1:-1],end="    ")
                elif (counter== ((i.count('/')-2)) and (i[-1]=='/')):
                    print(i[len(wayL):-1],end="    ")


if __name__ == "__main__":
    try:
        a = sys.argv[1]
    except IndexError:
        exit()
    constWay='/root: '
    way=''
    pWay=""
    z = zipfile.ZipFile(a, 'r')                     
    allFiles=(z.namelist())                         
    cmd = input(constWay)
    while cmd != "exit":
        cmd=cmd.split(" ")
        if cmd[0] == "pwd":
            PWD(pWay)
        elif cmd[0] == "cat":
            temp_out=checkFile(cmd[1],pWay,allFiles)
            if "cat: can't open" in temp_out:
                print(temp_out)
            else:
                CAT(temp_out,a)
        elif cmd[0] == "ls":
            _=pWay
            ls(_,allFiles)
            print()
        elif cmd[0] == "cd":
            temp=(checkDirectory(cmd[1],pWay,allFiles))
            if "can't cd into " in temp:
                pass
                print(temp)
            else:
                pWay=temp
        else:
            print(cmd[0]+ " not found")
        cmd = input("root/"+pWay+": ")