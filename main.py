from sys import executable
from subprocess import check_call
if __name__=='__main__':
    from os import path
    if path.isfile("all_checks_done.txt")==False:
        check_call([executable,'check_package.py'])
        message = "Please do not delete this file.\nDo not write anything in this file.\nDo not change the destination of this file.\nThis file is only for the purpose to insure that all the checks are done.\nThe checking of the package is only done for the first time to avoid recurring time delay.\n\n\nANY CHANGE IN THIS FILE COULD LEAD TO BREAKING DOWN OF THE APP."
        file = open("all_checks_done.txt","w+")
        message.split('\n')
        file.writelines(["%s" % line for line in message])
        check_call([executable,'youtube.py'])
    
    else:
        check_call([executable,'youtube.py'])