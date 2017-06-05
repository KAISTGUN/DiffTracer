import os
import sys
import subprocess
import numpy as np

def function_parser(argv):
    print ("Parsing fuctions..")
    ctagCommand ='ctags -x -R --c++-kinds=-cdeglmnpstuv \
    --languages=c++ --exclude=*.h --exclude=*.cc '+ argv[1]
    ctagResult = subprocess.check_output(ctagCommand.split())    
    funcDic=dict()
    index = 0
    nameList = []
    for line in ctagResult.split('\n'):
        if (line ==''):
            continue
        lineSplit = line.split()
        functionName = lineSplit[0]
        # Dealing with Specific case 'operator'
        if (functionName == 'operator'):
            functionName = lineSplit[0] + lineSplit[1]
            numIndex = 2
            while True:
                if(lineSplit[numIndex].isdigit()):
                    functionLine = lineSplit[numIndex]
                    fileName = lineSplit[numIndex+1]
                    break
                numIndex+=1
        else:
            functionLine = lineSplit[2]
            fileName = lineSplit[3]
        functionLine = int(functionLine)
        # If a file is already searched..
        if (fileName in nameList) == True :
            dupIndex = nameList.index(fileName)
            funcDic[dupIndex]['func'].append([functionName])
            funcDic[dupIndex]['line'] = np.append(funcDic[dupIndex]['line'],functionLine)
        else:
            funcDic[index] = {'filename': fileName, 'func': [functionName],'line': np.array([functionLine])}
            nameList.append(fileName)
            index+=1

    print ("Parsing Done")
    return funcDic

def diff_file(argv):
    print ("Diff strings..")
    diffCommand = ["diff", "--changed-group-format='%>'", "--unchanged-group-format=''"]
    diffString = ''
    directories = os.walk(argv[1])
    split = argv[2].split('/')[0]

    for (path, _, files) in directories:
        for filename in files:
            Path1 = path
            Path1 = split +'/'+ '/'.join(Path1.split('/')[1:]) +'/'+filename
            Path2 = os.path.join(path,filename)
            if (filename.split(".")[-1] != "cpp" or os.path.exists(Path1) != True ):
                continue
            diffCommand.append("--new-line-format="+Path2+"' %dn %L'")
            diffCommand.append(Path1)
            diffCommand.append(Path2)
            pipe = subprocess.Popen(diffCommand,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            diffCommand = diffCommand[:-3]
            diffResult = pipe.stdout.read().replace('\'','')
            if diffResult != '':
                diffString += diffResult

    if ( diffString == ''):
        print("No difference discovered")
        sys.exit(0)

    diffDic = dict()
    nameList = []
    index = 0
    for line in diffString.split('\n'):
        lineSplit = line.split()
        if(lineSplit == []):
            break
        fileName = lineSplit[0]
        diffLine  = int(lineSplit[1])
        if (fileName in nameList) == True :
            dupIndex = nameList.index(fileName)
            diffDic[dupIndex]['line'] = np.append(diffDic[dupIndex]['line'],diffLine)
        else:
            diffDic[index] = {'filename': fileName, 'line': np.array([diffLine])}
            nameList.append(fileName)
            index+=1

    print("Diff Done")
    return diffDic

def extract_modified_function(funcDic, diffDic,argv):

    '''
    Compare Diff line and Function line
    funcDic = {'filname':,'functioname':,'line:'}
    diffDic = {'filname':,'line:'}
    '''
    print ("Starting compare...")
    answer = []
    prevFunc=""
    changedLine = 0

    for i in range(len(diffDic)-1):
        fileName1 = diffDic[i]['filename']
        for j in range(len(funcDic)-1):
            fileName2 = funcDic[j]['filename']
            if (fileName1 == fileName2):
                ansStr1 = fileName1+"\t"
                ansStr2 = ''
                for k in range(len(diffDic[i]['line'])):
                    changedLine += 1
                    lineDiff = funcDic[j]['line'] - diffDic[i]['line'][k]
                    if np.min(lineDiff) <= 0:
                          minus = [float('-inf') if var > 0 else var for var in lineDiff]
                          funcIndex = np.argmax(minus)
                          diffFunc = funcDic[j]['func'][funcIndex][0]
                          if diffFunc == prevFunc:
                              continue
                          ansStr2 += diffFunc+","
                          prevFunc = diffFunc
                answer.append(ansStr1+ansStr2[:-1]+"\n")
                break

    if answer == []:
        print ("No function modified")
        sys.exit(0)

    ansfile = ("answer__"+argv[1]+'__'+argv[2]).replace('/','_')
    answer.append("Total Patched Line: " + str(changedLine))
    ans = ''.join(answer)
    print("Total Patched Line: " + str(changedLine))

    answerFile = open(ansfile,"w")
    answerFile.write(ans)
    answerFile.close()
    print ("Your result has been saved in "+ansfile)

def main(argv):
    if (len(argv) < 3):
        print("Usage: python [fileName] [Unpatched directory] [patched directory]")
        sys.exit(0)
    fString = function_parser(argv)
    diffDic = diff_file(argv)
    extract_modified_function(fString, diffDic, argv)

if __name__ == "__main__":
    main(sys.argv)
