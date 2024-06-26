import os
import re

class AmunLogParser:
    
    def __init__(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    self.filename = filename
                    content = f.read()
                    self.content_list = content.strip().split('\n')
            except IOError:
                self.content_list = None
        else:
            self.content_list = None
			
    def amun_request_handler_log_parser(self):
        if self.content_list is None:
            return None

        log_data = {}
        log_data['IP'] = {}
        log_data['stages'] = {}
        log_data['port_scanned'] = {}

        pattern1 = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\S+) \[amun_request_handler\] unknown vuln \(Attacker: (\S+) Port: (\d+), Mess: \[(.*)\] \((\d*)\) Stages: \[(.*)\]\)'
        pattern2 = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\S+) \[amun_request_handler\] incomplete vuln \(Attacker: (\S+) Port: (\d+), Mess: \[(.*)\] \((\d*)\) Stages: \[(.*)\]\)'
        pattern3 = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\S+) \[amun_request_handler\] PortScan Detected on Port: (\d+) \((\S+)\)' 

        for line in self.content_list:
        
            match1 = re.match(pattern1, line)
            match2 = re.match(pattern2, line)
            match3 = re.match(pattern3, line)

            if match1 or match2:
                if match1:
                    match = match1
                else:
                    match = match2

                attackerIP = match.group(3)
                log_data = self.update_log_data(log_data, 'IP', attackerIP)

                stage_list = match.group(7).split(", ")
                if len(stage_list) == 1 and stage_list[0] != '':
                    log_data = self.update_log_data(log_data, 'stages', stage_list[0])
                elif len(stage_list) > 1:
                    for stage in stage_list:
                        log_data = self.update_log_data(log_data, 'stages', stage)
                else:
                    continue
            elif match3:
                own_port = int(match3.group(3))
                attackerIP = match3.group(4)
                log_data = self.update_log_data(log_data, 'port_scanned', own_port)
                log_data = self.update_log_data(log_data, 'IP', attackerIP)
            # no match, not amun log file-- how to handle??
            else:
                continue
 
        return log_data


    def update_log_data(self, log_data, key, value):
        if log_data[key].get(value):
            log_data[key][value] += 1
        else:
            log_data[key][value] = 1
       
        return log_data

				
    # only develop this one, leave others alone
    # def amun_request_handler_log_parser(self):


    # def amun_server_log_parser(self):

    # def download_log_parser(self):
           
    # def exploits_log_parser(self):
            
    # def shellcode_manager_log_parser(self):

    # def submissions_log_parser(self):

    # develop log parser for other type of logs here...