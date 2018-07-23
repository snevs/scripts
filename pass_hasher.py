#!/usr/bin/env python3
__author__ = "roconsta"
__version__ = "1.3"
 
from passlib.hash import sha512_crypt
import getpass as get
import datetime as d
import getopt
from subprocess import call
import signal
import sys
import re
 
yel, grn, mgt, red, rst = "\x1b[1;33m", "\x1b[1;32m", "\x1b[1;35m", "\x1b[1;31m", "\x1b[0m"
inow = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
 
print(mgt+ inow, "This script is intended to generate salt hashed passwords for Linux machines.")
print(inow, "This script will hash the password and then verify if it's valid or not.")
print(inow, "The password verificationconsists of verifying a secret using an existing hash.")
print(inow, "This checks if a secret matches against the one stored inside the specified hash.\n", rst)
 

def pass_gen():
    """This script is asking the user to insert the plain password and
       then it uses that password to generate a hash/salt which can then
       be deployed using Ansible on all the servers via the password-change plan.
       Used Passlib Python module and hash verification:
       https://pythonhosted.org/passlib/lib/passlib.ifc.html#passlib.ifc.PasswordHash.verify
    """
 
    users = ('setup', 'root', 'oracle')
 
    for i in users:
        inow = d.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        passin = get.getpass(inow + " Enter a password for "+ i+ ": ")
        if len(passin) == 0:
            print(inow+red,"Error: Empty input. Skipping...", rst)
        elif len(passin) < 12:
            print(inow + red, "Error: password is not at least 12 characters long. Skipping...", rst)
        elif passin.isdigit():
            print(inow+red,"Error: input password cannot consist of numbers only. Skipping...", rst)
        else:
            hash = sha512_crypt.hash(passin)
            print(inow, "Password for", i, "is:\n"+ inow, yel+ hash+ rst)
            result = sha512_crypt.verify(passin, hash)
            if result:
                print(inow, "The password is "+grn+"OK\n"+rst + inow,
                "####################################")
            else:
                print(inow, "The password is "+red+"NOK\n"+rst + inow,
                    "###################################")
 
if __name__ == "__main__":
    try:
        pass_gen()
    except KeyboardInterrupt:
        print("\n"+red+ "CTRL-C pressed. Exiting...", rst)
        sys.exit(0)
 
##EOF
