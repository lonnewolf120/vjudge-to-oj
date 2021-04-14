from . import apiHandler
import os
import errno

apicaller = apiHandler.ApiCaller()
path = os.path.dirname(__file__)

class Problem:
    # 1. judgeSlug(mapped from the folder name. i.e: Submissions>UVA)
    # 2. problemId(collected from subfolder of judge submissions. i.e: Submissions>UVA>104)
    # 3. problemName(collected from UVa api)
    # 4. Solutions
    #     1. Submission Code(all the files inside a problem id. i.e: Submissions>UVA>104>123124.cpp)
    #     2. Language mapping(from solution extention. i.e: Submissions>UVA>104>1231123.cpp)

    judgeSlug = str()
    problemNumber = str()
    solutions = list()
    localDir = str()

    def __init__(self, problemDir, problemNumber, judgeSlug = "UVA"):
        self.localDir = problemDir
        self.judgeSlug = judgeSlug
        self.problemNumber = problemNumber
        self.solutions.clear()

    def getName(self):
        return self.judgeSlug + " " + self.problemNumber + " - " + self.problemName

    def __str__(self):
        return self.judgeSlug + " - " + self.problemName + " (sols: " + str(len(self.solutions)) + ")"

class Solution:
    problemNumber = str()
    problemName = str()
    solutionExt = str()
    solutionCode = str()

    def __init__(self, submissionDir, problemNumber, problemName):
        print(f"{problemNumber} submission dir: " + submissionDir)
        self.problemNumber = problemNumber
        self.problemName = problemName
        self.solutionExt = submissionDir.split('.')[-1]
        with open(submissionDir, 'r') as code:
            self.solutionCode = code.read()

    def __str__(self):
        return self.problemNumber + " - " + self.problemName

class UvaProblem(Problem):
    problemId = str()
    problemName = str()
    savingPath = path + os.sep + "Submitted" + os.sep + "UVA"

    def __init__(self, problemDir, problemNumber, judgeSlug = "UVA"):
        super().__init__(problemDir, problemNumber, judgeSlug)
        problemData = apicaller.getUvaProblemDataUsingProblemNumberOffline(problemNumber)
        self.problemId = str(problemData[0])
        self.problemName = str(problemData[1])
        solCnt = 0
        for subName in os.listdir(problemDir):
            self.solutions.append(list([Solution(problemDir + os.sep + subName, problemNumber, self.problemName), solCnt]))
            solCnt = solCnt + 1

    """
    Important when saving solution.
    Fobidden printable ascii characters while saving:-

    Linux/Unix:
    / (forward slash)
    
    Windows:
    < (less than)
    > (greater than)
    : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)

    """

    def fileNameCleaner(self, fileName):
        forbidden = {'/', '\\', '<', '>', ':', '"', '|', '?', '*'}
        newName = ""
        for c in fileName:
            if(c not in forbidden):
                newName = newName + str(c)
        return newName

    def saveSolution(self, solutionId, submissionId):
        fileName = self.problemNumber + " - " + self.problemName
        fileName = fileName + "(" + str(solutionId) + ", " + str(submissionId) + ")." + self.solutions[solutionId][0].solutionExt
        fileName = self.fileNameCleaner(fileName)
        savePath = self.savingPath + os.sep + fileName
        print("Saving on : ", savePath)
        with self.safe_open_w(savePath) as f:
            f.write(self.solutions[solutionId][0].solutionCode)

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
            if(os.path.exists(path)):
                print("path created on ", path)
            else:
                print("path not created")
            
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def safe_open_w(self, path):
        ''' Open "path" for writing, creating any parent directories as needed.
        '''
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'w')

class CodeForcesProblem(Problem):
    problemId = str()
    problemName = str()
    savingPath = path + os.sep + "Submitted" + os.sep + "CodeForces"

    def __init__(self, problemDir, problemNumber, judgeSlug = "CodeForces"):
        super().__init__(problemDir, problemNumber, judgeSlug)
        problemData = apicaller.getCodeForcesProblemDataUsingProblemNumber(problemNumber)
        self.problemId = str(problemData[0])
        self.problemName = str(problemData[1])
        solCnt = 0
        for subName in os.listdir(problemDir):
            self.solutions.append(list([Solution(problemDir + os.sep + subName, problemNumber, self.problemName), solCnt]))
            solCnt = solCnt + 1

    """
    Important when saving solution.
    Fobidden printable ascii characters while saving:-

    Linux/Unix:
    / (forward slash)
    
    Windows:
    < (less than)
    > (greater than)
    : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)

    """

    def fileNameCleaner(self, fileName):
        forbidden = {'/', '\\', '<', '>', ':', '"', '|', '?', '*'}
        newName = ""
        for c in fileName:
            if(c not in forbidden):
                newName = newName + str(c)
        return newName

    def saveSolution(self, solutionId, submissionId):
        fileName = self.problemNumber + " - " + self.problemName
        fileName = fileName + "(" + str(solutionId) + ", " + str(submissionId) + ")." + self.solutions[solutionId][0].solutionExt
        fileName = self.fileNameCleaner(fileName)
        savePath = self.savingPath + os.sep + fileName
        print("Saving on : ", savePath)
        with self.safe_open_w(savePath) as f:
            f.write(self.solutions[solutionId][0].solutionCode)

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
            if(os.path.exists(path)):
                print("path created on ", path)
            else:
                print("path not created")
            
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def safe_open_w(self, path):
        ''' Open "path" for writing, creating any parent directories as needed.
        '''
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'w')

class SpojProblem(Problem):
    problemId = str()
    problemName = str()
    savingPath = path + os.sep + "Submitted" + os.sep + "SPOJ"

    def __init__(self, problemDir, problemNumber, judgeSlug="Spoj"):
        super().__init__(problemDir, problemNumber, judgeSlug)
        # problemData = apicaller.getSPOJSolveData(problemNumber)
        # self.problemId = str(problemData[0])
        self.problemName = str(problemNumber)
        solCnt = 0
        for subName in os.listdir(problemDir):
            self.solutions.append(
                list([Solution(problemDir + os.sep + subName, problemNumber, self.problemName), solCnt]))
            solCnt = solCnt + 1

    """
    Important when saving solution.
    Fobidden printable ascii characters while saving:-

    Linux/Unix:
    / (forward slash)

    Windows:
    < (less than)
    > (greater than)
    : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)

    """

    def fileNameCleaner(self, fileName):
        forbidden = {'/', '\\', '<', '>', ':', '"', '|', '?', '*'}
        newName = ""
        for c in fileName:
            if (c not in forbidden):
                newName = newName + str(c)
        return newName

    def saveSolution(self, solutions):
        fileName = self.judgeSlug + " - " + solutions.problemNumber + " - Accepted."
        fileName = fileName + solutions.solutionExt
        fileName = self.fileNameCleaner(fileName)
        savePath = self.savingPath + os.sep + fileName
        print("Saving on : ", savePath)
        with self.safe_open_w(savePath) as f:
            f.write(solutions.solutionCode)

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
            if (os.path.exists(path)):
                print("path created on ", path)
            else:
                print("path not created")

        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def safe_open_w(self, path):
        ''' Open "path" for writing, creating any parent directories as needed.
        '''
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'w')

class LightojProblem(Problem):
    problemHandle = str()
    problemName = str()
    savingPath = path + os.sep + "Submitted" + os.sep + "LightOJ"

    def __init__(self, problemDir, problemNumber, judgeSlug="LightOJ"):
        super().__init__(problemDir, problemNumber, judgeSlug)
        problemData = apicaller.getLojProblemDataUsingProblemNumber(problemNumber)
        self.problemHandle = str(problemData['handle'])
        self.problemName = str(problemData['name'])
        solCnt = 0
        for subName in os.listdir(problemDir):
            self.solutions.append(
                list([Solution(problemDir + os.sep + subName, problemNumber, self.problemName), solCnt]))
            solCnt = solCnt + 1

    """
    Important when saving solution.
    Fobidden printable ascii characters while saving:-

    Linux/Unix:
    / (forward slash)

    Windows:
    < (less than)
    > (greater than)
    : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)

    """

    def fileNameCleaner(self, fileName):
        forbidden = {'/', '\\', '<', '>', ':', '"', '|', '?', '*'}
        newName = ""
        for c in fileName:
            if (c not in forbidden):
                newName = newName + str(c)
        return newName

    def saveSolution(self, solutionId, submissionId):
        fileName = self.problemNumber + " - " + self.problemName
        fileName = fileName + "(" + str(solutionId) + ", " + str(submissionId) + ")." + self.solutions[solutionId][
            0].solutionExt
        fileName = self.fileNameCleaner(fileName)
        savePath = self.savingPath + os.sep + fileName
        print("Saving on : ", savePath)
        with self.safe_open_w(savePath) as f:
            f.write(self.solutions[solutionId][0].solutionCode)

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
            if (os.path.exists(path)):
                print("path created on ", path)
            else:
                print("path not created")

        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def safe_open_w(self, path):
        ''' Open "path" for writing, creating any parent directories as needed.
        '''
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'w')
