#!/usr/bin/python
import argparse, json, sys, re
from desc_parser import TaskDescriptor
from string import Template
import systems.Lomonosov
import systems.Regatta

accounts = dict()
accounts["lomonosov"] = dict(login="somelogin", key="somekey")
accounts["regatta"] = dict(login="somelogin", key="somekey")

if sys.argv[1] == "submit":
    inputString = open(sys.argv[1], 'r').read()
    taskDescriptor = TaskDescriptor(inputString)
    commandLine = taskDescriptor.insertParameters(\
        vars(taskDescriptor.getArgsParser().parse_args(sys.argv[3:])))
    print(commandLine)
    if sys.argv[2] == "lomonosov":
        rsh = systems.Lomonosov.connect(accounts["lomonosov"]["login"], accounts["lomonosov"]["key"])
        print(rsh.submit(commandLine))
    elif sys.argv[2] == "regatta":
        rsh = systems.Regatta.connect(accounts["regatta"]["login"], accounts["regatta"]["key"])
        print(rsh.submit(commandLine))
elif sys.argv[1] == "status":
    jobid = sys.argv[3]
    if sys.argv[2] == "lomonosov":
        rsh = systems.Lomonosov.connect(accounts["lomonosov"]["login"], accounts["lomonosov"]["key"])
        print(rsh.status(jobid))
    elif sys.argv[2] == "regatta":
        rsh = systems.Regatta.connect(accounts["regatta"]["login"], accounts["regatta"]["key"])
        print(rsh.status(jobid))
