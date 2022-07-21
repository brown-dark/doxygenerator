# doxygenerator

The script is aimed to generate [doxygen](https://doxygen.nl/) documentation along with call-by/called-by graphs and UML class diagrams for C/C++ projects.
Although it simplifies the configuration process, the one can change the configuration via [doxywizard](https://www.doxygen.nl/manual/doxywizard_usage.html) which is being installed via standard installer on Windows and can be installed running `apt install doxygen-gui` on Linux. For UML class diagrams it is required a [graphviz](https://graphviz.org/) package to be installed. The result of the generation is a set of HTML pages. The one has to open an _index.html_ page in order to start browsing.

# prerequirements

- python v3
- doxygen
- graphviz

# limitations

It is required to always keep the _Doxyfile_ configuration file near the _doxygenerator.py_ script.

Also, after installing doxygen and graphviz on Windows it is required to add them to PATH system environment variables so that they can be reachable from the command line.

# usage

For correct script running it is required to indicate the path to source code for which the doxygen documentation shall be generated and the destination path where the result of generation shall be stored:
```
python3 doxygenerator.py --source path/to/source/ --destination path/to/where/store/result
```
Sometimes it is required to skip some folders (e.g. build folders) in source path. For that one need to specify these folders relatively to source path after exclude flag:
```
python3 doxygenerator.py --source path/to/source/ --destination path/to/where/store/result --exclude folder1 folderN
```
Most projects are big and the process of file indexing via file manager may take a lot of time. It is recomended to open the result _index.html_ file also via command line:
```
cd path/to/where/store/result/html
firefox index.html
```
In case the one forgot something there is an instruction of usage:
```
python3 doxygenerator.py --help
```