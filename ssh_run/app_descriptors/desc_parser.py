#!/usr/bin/env python
import argparse, json, sys, re
from string import Template

class TaskDescriptor:
    def __init__(self, jsonString):
        jsonTree = json.loads(jsonString)
        self.name = jsonTree['name']
        self.arguments = dict()
        for arg in jsonTree['arguments']:
            self.arguments[arg['name']] =\
                {'string': Template(arg['string']), 'type': arg['type'],\
                'required': arg['required'] if 'required' in arg else False}
        self.commandLine = Template(jsonTree['commandLine'])
    def insertParameters(self, parameters):
        substList = dict();
        for key in parameters:
            substList[key] =\
            self.arguments[key]['string'].substitute(x = parameters[key])
        return re.sub(r'\$[a-zA-Z]\w+', '', self.commandLine.safe_substitute(substList))
    def getArgsParser(self):
        parser = argparse.ArgumentParser()
        for key in self.arguments:
            argType = self.arguments[key]['type']
            if argType == 'int':
                argType = int
            elif argType == 'string':
                argType = str
            if argType == 'presence':
                parser.add_argument('--' + key, default = argparse.SUPPRESS,\
                                    required = self.arguments[key]['required'],\
                                    action = 'store_true')
            else:
                parser.add_argument('--' + key, default = argparse.SUPPRESS,\
                                    required = self.arguments[key]['required'],\
                                    type = argType)
        return parser
#inputString = open(sys.argv[1], 'r').read()
#taskDescriptor = TaskDescriptor(inputString)
#print(taskDescriptor.insertParameters(\
#    vars(taskDescriptor.getArgsParser().parse_args(sys.argv[2:]))))
