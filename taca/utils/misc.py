""" Miscellaneous or general-use methods
"""
import hashlib
import os
import smtplib
import subprocess
import sys

from datetime import datetime
from email.mime.text import MIMEText


def send_mail(subject, content, receiver):
    """ Sends an email

    :param str subject: Subject for the email
    :param str content: Content of the email
    :param str receiver: Address to send the email
    """
    msg = MIMEText(content)
    msg['Subject'] = "TACA - {}".format(subject)
    msg['From'] = 'TACA'
    msg['to'] = receiver

    s = smtplib.SMTP('localhost')
    s.sendmail('TACA', [receiver], msg.as_string())
    s.quit()


def call_external_command(cl, with_log_files=False, prefix=None):
    """ Executes an external command

    :param string cl: Command line to be executed (command + options and parameters)
    :param bool with_log_files: Create log files for stdout and stderr
    """
    if type(cl) == str:
        cl = cl.split(' ')
    command = os.path.basename(cl[0])
    stdout = sys.stdout
    stderr = sys.stderr

    if with_log_files:
        if prefix:
            command = '{}_{}'.format(prefix, command)
        stdout = open(command + '.out', 'wa')
        stderr = open(command + '.err', 'wa')
        started = "Started command {} on {}".format(' '.join(cl), datetime.now())
        stdout.write(started + '\n')
        stdout.write(''.join(['=']*len(cl)) + '\n')

    try:
        subprocess.check_call(cl, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError, e:
        e.message = "The command {} failed.".format(' '.join(cl))
        raise e
    finally:
        if with_log_files:
            stdout.close()
            stderr.close()


def call_external_command_detached(cl, with_log_files=False, prefix=None):
    """ Executes an external command

        :param string cl: Command line to be executed (command + options and parameters)
        :param bool with_log_files: Create log files for stdout and stderr
        """
    if type(cl) == str:
        cl = cl.split(' ')
    command = os.path.basename(cl[0])
    stdout = sys.stdout
    stderr = sys.stderr

    if with_log_files:
        if prefix:
            command = '{}_{}'.format(prefix, command)
        stdout = open(command + '.out', 'wa')
        stderr = open(command + '.err', 'wa')
        started = "Started command {} on {}".format(' '.join(cl), datetime.now())
        stdout.write(started + '\n')
        stdout.write(''.join(['=']*len(cl)) + '\n')

    try:
        p_handle = subprocess.Popen(cl, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError, e:
        e.message = "The command {} failed.".format(' '.join(cl))
        raise e
    finally:
        if with_log_files:
            stdout.close()
            stderr.close()
    return p_handle

def days_old(date, date_format="%y%m%d"):
    """ Return the number days between today and given date

        :param string date: date to ckeck with
        :param date_format: the format of given 'date' string
    """
    try:
        time_dif = datetime.today() - datetime.strptime(date,date_format)
    except ValueError:
        return None
    return time_dif.days

def hashfile(afile, hasher='sha1', blocksize=65536):
    """ Calculate the hash digest of a file with the specified algorithm and 
        return it.
        
        This solution was adapted from http://stackoverflow.com/a/3431835
    
        :param string afile: the file to calculate the digest for
        :param string hasher: the hashing algorithm to be used, default is sha1
        :param int blocksize: the blocksize to use, default is 65536 bytes
        :returns: the hexadecimal hash digest or None if input was not a file
    """ 
    if not os.path.isfile(afile):
        return None
    hashobj = hashlib.new(hasher)
    with open(afile,'rb') as fh:
        buf = fh.read(blocksize)
        while len(buf) > 0:
            hashobj.update(buf)
            buf = fh.read(blocksize)
    return hashobj.hexdigest()
    
def query_yes_no(question, default="yes", force=False):
    """Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user. "default"
    is the presumed answer if the user just hits <Enter>. It must be
    "yes" (the default), "no" or None (meaning an answer is required
    of the user). The force option simply sets the answer to default.
    The "answer" return value is one of "yes" or "no".

    :param question: the displayed question
    :param default: the default answer
    :param force: set answer to default
    :returns: yes or no
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        if not force:
            choice = raw_input().lower()
        else:
            choice = "yes"
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                                 "(or 'y' or 'n').\n")
