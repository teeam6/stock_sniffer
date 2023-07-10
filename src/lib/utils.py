
import subprocess
import config
import os
import logging
import pendulum


class Utils: 
    def __init__(self):
        self.cfg = config.Config(os.path.join(os.path.dirname(os.path.realpath(__file__)), "stock_sniffer.cfg"))
        
        curr_date = pendulum.now().strftime('%d-%m-%Y')
        if self.cfg['general.local_testing'] is False:
            logging.basicConfig(filename=f'{self.cfg["general.log_path"]}/{curr_date}.log', filemode='a+',
                                format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                                level='DEBUG')
        else:
            logging.basicConfig(filename='{}.log'.format(curr_date), filemode='a+',
                                format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                                level='DEBUG')
        self._debug = lambda x: self.log(x, 'debug') if self.cfg['debug'] else None
        self._error = lambda x: self.log(x, 'error')
        self._warning = lambda x: self.log(x, 'warning')
        self._log = lambda x: self.log(x, 'info')
        self._success = lambda x: self.log(x, 'success')

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
            'crit': lambda: logging.critical(message),
            'success': lambda: logging.info(message)
        }[ltype]()
        print(cl[ltype.upper()]+ltype.upper()+' '+message+cl['INFO'])

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
             
    

