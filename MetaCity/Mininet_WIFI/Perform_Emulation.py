import json
from subprocess import call,Popen
import datetime
import shutil
import os
import subprocess
from pathlib import Path
import time
class Perform_Emulation(object):
    def __init__(self,filename,path=None):
        if not path:
            self.path = os.path.split(os.path.realpath(__file__))[0]+'/'+r'Network_Topology/'
        else:
            self.path=path
        self.filename=filename
        self.file=Path(self.path+self.filename)
        if not self.file.exists():
            raise Exception("This file(%s) does not exist"%(self.filename))

    def perform(self):

        command=" ".join(['sudo', 'mn','-c','&&','sudo','python3',str(self.file.absolute())])
        p=subprocess.Popen(command,shell=True)
        # output, err = p.communicate()
        p.poll()
        if p.returncode == None:
            print("The Emulation Ended Successfully")
            self.cleandata(files=[str(self.file.absolute()).replace('.py','.json')])
            return True
        else:
            print("The Emulation Ended abnormally")
            return False

    def check_status(self,outcome=None,flag={"status":'completed'}):
        result=None
        status=None
        if outcome:
            result=  Path(self.path + outcome)
        else:
            result = Path(str(self.file.absolute()).replace('.py','.json'))

        if result.exists():
            with result.open(mode='r') as f:
                data=json.load(f)
                for f,v in flag.items():
                    if not data.get(f,None) or data.get(f,None)!=v:
                        status = (False, None)
                        break

                if not status:
                    status = (True, str(result.absolute()))
        else:
            status = (False,None)

        return status

    def cleandata(self,files=[],directories=[]):
        for f in files:
            file=Path(f)
            if file.exists():
                file.unlink()

        for d in directories:
            directory= Path(d)
            if directory.exists():
                shutil.rmtree(str(directory.absolute()),ignore_errors=True)

