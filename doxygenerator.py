import argparse
import os
import sys
import pathlib

def createArgumentParser():

    parser = argparse.ArgumentParser(
        description='''
        This generator is aimed to create doxygen documentation with call-by/called-by graphs and
        UML diagrams.
        "doxygen" & "graphviz" packages must be installed in the system. To install them do the
        following: "sudo apt install -y doxygen graphviz".
        After script executed enter the destinanion folder and open /html/index.html with any
        browser you prefer.
        '''
    )

    parser.add_argument(
        '-s',
        '--source',
        action='store',
        required=True,
        help='''
        Uses for indicating the source code folder from where doxygen
        generation starts.
        '''
    )
    parser.add_argument(
        '-d',
        '--destination',
        action='store',
        required=True,
        help='''
        Uses for indicating the destination folder to where doxygen
        generation puts the result.
        '''
    )
    parser.add_argument(
        '-e',
        '--exclude',
        nargs='*',
        help='''
        Uses for indicating folder(s) relatively to <source> that should not be
        involved in doxygen generation.
        '''
    )

    return parser


def createDestinationFolderIfNeed(destinationPath):

    resultPath = pathlib.Path(destinationPath)
    resultPath.mkdir(parents=True, exist_ok=True)


def validateUserInput(sourcePath, destinationPath, excludePathsList):

    result = True

    if not sourcePath:
        print(
            '''Invalid value for "source" value: {sp}'''
            .format(sp=sourcePath)
        )
        result = False

    elif not destinationPath:
        print(
            '''Invalid value for "destination" value: {dp}'''
            .format(dp=destinationPath)
        )
        result = False

    elif not os.path.isdir(sourcePath):
        print(
            '''No directory exists for "source" value: {sp}'''
            .format(sp=sourcePath)
        )
        result = False

    elif not os.path.isdir(destinationPath):
        print(
            '''No directory exists for "destination" value: {dp}'''
            .format(dp=destinationPath)
        )
        result = False

    elif not os.path.exists('Doxyfile'):
        print(
            '''No "Doxyfile" doxygen configuration file was found in {cwd}'''
            .format(cwd=os.getcwd())
        )
        result = False

        if excludePathsList:

          for excludePath in excludePathsList:
              if not os.path.isdir(excludePath):
                  print(
                      'No directory exists for "exclude" value: {ep}'
                      .format(ep=excludePath)
                  )

                  result = False

    return result


def convertListToDoxygenList(list):

    if len(list) == 1:
        return str(list[0])

    else:
        result = ''

        for item in list:
            result += item + ' \\' + '\n'

        # Removing excess ' \\n' symbols for the last line
        result = result[:-3]

        return result


def parametrizeDoxyfile(sourcePath, destinationPath, excludePathsList, doxyfileUserPath):

    templateFile = open('Doxyfile', 'r')
    templateFileContent = templateFile.read()
    templateFile.close()

    templateFileContent = templateFileContent.replace(
        "{SOURCE_PATH}",
        sourcePath
    )
    templateFileContent = templateFileContent.replace(
        "{DESTINATION_PATH}",
        destinationPath
    )

    if excludePathsList:
        templateFileContent = templateFileContent.replace(
            "{EXCLUDE_PATHS}",
            convertListToDoxygenList(absExcludePathsList)
        )

    resultFile = open(doxyfileUserPath, 'w')
    resultFile.write(templateFileContent)
    resultFile.close()


def runDoxyGeneration(doxyfileUserPath):

    return os.system('doxygen {dxgConf}'.format(dxgConf=doxyfileUserPath))


if __name__ == '__main__':

    parser = createArgumentParser()
    args = parser.parse_args()

    sourcePath = args.source
    destinationPath = args.destination
    excludePathsList = args.exclude

    createDestinationFolderIfNeed(destinationPath)

    doxyfileUserPath = destinationPath + '/' + 'DoxyfileUser'

    absExcludePathsList = []

    if excludePathsList:

        # NOTE: Due to doxygen claims abs paths for exclusion it is required to convert
        # user's relative path to abs.
        absPathOfSourceDir = os.path.abspath(sourcePath)

        for excludePath in excludePathsList:
            absExcludePathsList.append(absPathOfSourceDir + '/' + excludePath)

    if not validateUserInput(sourcePath,destinationPath, absExcludePathsList):
        sys.exit('EXECUTION PREVENTED DUE TO ERRORS')

    else:
        print(
            '\n****************************************\n'
            '\n * Generating doxygen documentation for "{sp}" folder.'
            '\n * Excluded paths are "{ep}".'
            '\n * Result will be stored in "{dp}" folder.\n'
            '\n****************************************\n'
                .format(
                    sp=sourcePath,
                    ep=excludePathsList if excludePathsList else "empty",
                    dp=destinationPath
                )
        )

    parametrizeDoxyfile(
        sourcePath,
        destinationPath,
        absExcludePathsList,
        doxyfileUserPath
    )

    result = runDoxyGeneration(doxyfileUserPath)

    if result == 0:
        print(
            '\n========================================\n'
            'Navigate to {dp}{sep}html{sep} and open "index.html" via any browser you prefer.'
                .format(
                    dp=destinationPath[:-1] if destinationPath[-1] == '/' else destinationPath,
                    sep=os.sep
                )
        )