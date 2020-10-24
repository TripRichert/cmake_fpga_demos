import re
import os

def generateCmdlineDiction(args):
    mydictionary = {}
    definitionList = []
    currentKey = ""
    for arg in args:
        if (re.match("-.+", arg)):
            if (len(currentKey) > 0):
                mydictionary[currentKey] = definitionList
            currentKey = arg[1:]
            definitionList = []
        else:
            definitionList.append(arg)
    if (len(currentKey) > 0):
        mydictionary[currentKey] = definitionList
    return mydictionary

def expand_dictionary(dictionary):
    for keypair in dictionary:
        entry_list = keypair[1]
        index = 0
        edited = 0
        while index < len(entry_list):
            entry = entry_list[index]
            if entry in dictionary.keys():
                for nested_entry in dictionary[entry]:
                    if not nested_entry in entry_list:
                        entry_list.append(nested_entry)
                        edited = 1
            index = index + 1
        if edited == 1:
            dictionary[keypair[0]] = entry_list
    return dictionary
                
def read_dependency_tree_file(filename):
    dirname = os.path.dirname(filename)
    deptree_dictionary = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.isspace():
                assert re.subn("<=", '', line)[1] == 1
                key_pair = line.split("<=")
                entry_list = []
                entry_str = key_pair[1].strip()
                for entry in entry_str.split(" "):
                    entry = os.path.join(*entry.split("/"))
                    entry = os.path.join(dirname, entry)
                    entry = os.path.realpath(entry)
                    entry_list.append(entry)
                keyname = key_pair[0].strip()
                keyname = os.path.join(*keyname.split("/"))
                keyname = os.path.join(dirname, keyname)
                keyname = os.path.realpath(keyname)
                deptree_dictionary[keyname] = entry_list
    deptree_dictionary = expand_dictionary(deptree_dictionary)
    return deptree_dictionary

def read_filelist_file(filename):
    dirname = os.path.dirname(filename)
    entry_list = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.isspace():
                entry = line.strip()
                entry = os.path.join(*entry.split("/"))
                entry = os.path.join(dirname, entry)
                entry = os.path.realpath(entry)
                entry_list.append(entry)
    return entry_list
