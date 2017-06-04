import os
import sys
import subprocess


def function_parser(argv):
    print ("Parsing fuctions..")
    tagName = os.path.basename(argv[1])
    tagFileName = tagName + "_function_tags"

    if (os.path.exists(tagFileName) != True):
        ctagCommand ="ctags -R -x --c++-kinds=+p --fields=iaSnt --languages=c++ \
                    --exclude=*.h "+ argv[1] +"| grep function > "+ tagFileName
        os.system(ctagCommand)

    tagFile = open(tagFileName)
    functionString=[]
    for line in tagFile:
        lineSplit = line.split()
        functionString.append(lineSplit[3] + " " + lineSplit[2] + " " + lineSplit[0])
    print ("Parsing Done")
    return functionString

def diff_file(argv):
    print ("Diff strings..")
    diffCommand = ["diff", "--changed-group-format='%>'", "--unchanged-group-format=''"]
    diffString = []
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
                diffString.append(diffResult)

    if ( diffString == []):
        print("No difference discovered")
        sys.exit(0)

    print("Diff Done")
    return diffString

def extract_modified_function(funcString, diffString):

    '''
    Compare Diff line and Function line
    '''
    print ("Starting compare...")
    answer = []
    for i in range(len(diffString)-1):
        minDiff = float('inf')
        diffString_split = diffString[i].split()
        fileName1 = diffString_split[0]
        diffLine  = diffString_split[1]

        for j in range(len(funcString)-1):
            funcString_split = funcString[j].split()
            fileName2 = funcString_split[0]            
            functionLine = funcString_split[1]
            functionName = funcString_split[2]

            if (fileName1 == fileName2):
                diffLineNum = int(diffLine) - int(functionLine)
                if(diffLineNum > 0 and minDiff > diffLineNum):
                    minDiff = diffLineNum
                    diffFunc = functionName
                    diffFile = fileName1

        if (minDiff != float('inf')):
            answer.append(diffFunc+"\t"+diffFile+"\n")

    if answer == []:
        print ("No function modified")
        sys.exit(0)

    answer = list(set(answer))
    answerFile = open("answer.txt","w")
    answerFile.write(''.join(answer))
    answerFile.close()
    print ("Check answer.txt")

def main(argv):
    if (len(argv) < 3):
        print("Usage: python [fileName] [Unpatched directory] [patched directory]")
        sys.exit(0)
    fString = function_parser(argv)
    diffString = diff_file(argv)
    extract_modified_function(fString, diffString)

if __name__ == "__main__":
    main(sys.argv)