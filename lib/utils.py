try:
    import configparser
    import subprocess
    import os
    import datetime
    import logging
#    import paramiko
    from time import gmtime, strftime, time
    from random import choice
except ImportError as e:
    raise Exception("Could not import required libraries: "+str(e))

class Utils:
    def __init__(self):
        self.cfg = self.parse_system_config('GENERAL_SETTINGS')
        
        cur_date = datetime.datetime.now().strftime('%d-%m-%Y')
        if self.cfg['local_testing'] == "False":
            logging.basicConfig(filename='{}/log/{}.log'.format(self.cfg['raw_path'], cur_date), filemode='a+',
                                format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                                level='DEBUG')
        else:
            logging.basicConfig(filename='{}.log'.format(cur_date), filemode='a+',
                                format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                                level='DEBUG')
        self._debug = lambda x: self.log(x, 'debug') if self.cfg['debug'] else None
        self._error = lambda x: self.log(x, 'error')
        self._warning = lambda x: self.log(x, 'warning')
        self._log = lambda x: self.log(x, 'info')
        # self.impalaWorker = choice(self.cfg['impala_worker'].split(','))
            
        # self.username = "govadmin"

    def log(self, message, ltype='info'):
        cl={'HEADER':'\033[95m',    #PURPLE
            'OKBLUE':'\033[94m',    #DARK PURPLE
            'DEBUG':'\033[96m',     #CYAN
            'SUCCESS':'\033[92m',   #GREEN
            'WARNING':'\033[93m',   #YELLOW
            'ERROR':'\033[91m',     #RED
            'INFO':'\033[0m',       #NORMAL WHITE
            'BOLD':'\033[1m',       #BOLD
            'CRIT':'\033[4m'        #UNDERLINE
            }
        {
            'info': lambda: logging.info(message),
            'debug': lambda: logging.debug(message),
            'warning': lambda: logging.warning(message),
            'error': lambda: logging.exception(message),
            'crit': lambda: logging.critical(message)
        }[ltype]()
        print(cl[ltype.upper()]+ltype.upper()+' '+message+cl['INFO'])

    @staticmethod
    def parse_system_config(section):
        config = configparser.RawConfigParser()
        config_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.cfg")
        config.read(config_location)

        conf = dict(config.items(section))
        return conf


    def get_shell_output(self, command, az=False):
        try:
            output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT).stdout.readlines()
        except subprocess.CalledProcessError as exc:
            self.log("Shell command failed with code: {}\n{}".format(exc.returncode, exc.output), 'error')
            return False
        if az:
            output = [i.decode("utf-8").rstrip() for i in output]

        return output

#    @staticmethod
#    def execute_shell(command):
#
#        try:
#            out = subprocess.call(command, shell=True)
#        except Exception as e:
#            print('Could not perform command, the wrong command was: ')
#            print(command)
#            print('The error was: ' + str(e))
#            return False
#
#        if out == 0:
#            return True
#        else:
#            print("Could not perform command", command)
#            return False

#    @staticmethod
#    def remote_sh(self, target_host, command, vm_user, vm_psswd=None, ignore_error=False): 
#        try: 
#            ssh_client = paramiko.SSHClient()
#            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#            ssh_client.connect(hostname=target_host, username=vm_user, password=vm_psswd)
#            stdin, stdout, stderror = ssh_client.exec_command(command)
#        except Exception as e:
#            self._error('Cannot execute powershell command: \n'+command)
#            self._error('[Exception details]\nHost:{}\nError:{}'.format(target_host, str(e)))
             
    

