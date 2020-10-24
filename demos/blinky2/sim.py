#license at bottom of file

from edalize import *
import os
import sys, re
import deptree


def main(argv):
    cmdDictionary = deptree.generateCmdlineDiction(argv)

    assert 'outdir' in cmdDictionary
    assert 'name'    in cmdDictionary
    assert 'topname' in cmdDictionary
    assert 'topfile' in cmdDictionary
    assert 'deptree_file' in cmdDictionary

    files = []

    hdlfiledeps = deptree.read_dependency_tree_file(cmdDictionary['deptree_file'][0])
    hdlfiles = hdlfiledeps[cmdDictionary['topfile'][0]]
    files = []
    for filename in hdlfiles:
        files.append({'name': filename, 'file_type': 'verilogSource'})
    files.append({'name': cmdDictionary['topfile'][0], 'file_type': 'verilogSource'})


    parameters = {'vcd' : {'datatype' : 'bool', 'paramtype' : 'plusarg'}}
    if 'parameters' in cmdDictionary:
        paramDictionary = deptree.generateCmdlineDiction(cmdDictionary['parameters'][1:]) 
        for param in paramDictionary:
            parameters[param] = {'datatype' : paramDictionary[param][0], 'default': paramDictionary[param][1], 'paramtype' : 'vlogparam'}

    tool = 'icarus'

    name = cmdDictionary['name'][0]
    topname = cmdDictionary['topname'][0]
    work_dir = cmdDictionary['outdir'][0]

    edam = {
        'files'        : files,
        'name'         : name,
        'parameters'   : parameters,
        'toplevel'     : topname
    }

    backend = get_edatool(tool)(edam=edam,
                                work_root=work_dir)

    os.makedirs(work_dir)
    backend.configure()

    backend.build()

    args = {'vcd' : True}
    backend.run(args)

if __name__ == "__main__":
   main(sys.argv[1:])


###############################################################################
# MIT LICENSE
###############################################################################

#Copyright 2020 Trip Richert

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
