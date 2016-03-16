__author__ = 'jinhongjun'
#coding=utf-8
import paramiko
import httplib,json

def get_result(retcode,result):
    a={}
    if retcode==0:
        a['retcode']=retcode
        a['stderr']=''
        a['stdout']=result
    else:
        a['retcode']=retcode
        a['stderr']=result
        a['stdout']=''
    return a

class SSH_result:
    '''get the result of command by ssh'''
    def __init__(self, host):
        self.host = host
        self.key = "/root/.ssh/id_rsa.pub"
        self.ssh = paramiko.SSHClient()
    def get(self,tgt,cmd):
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, 22, 'root', key_filename=self.key)
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            data=stdout.read()
            self.ssh.close()
            try:
                tmp_result=json.loads(data)
                result={
                    'retcode':0,
                    'stdout':tmp_result,
                    'stderr':''
                    }
            except Exception,e:
                result={
                    'retcode':1,
                    'stdout':'',
                    'stderr':e.message+' '+str(data)
                    }
        except Exception,e:
            result={
                'retcode':2,
                'stdout':'',
                'stderr':e.message
                }
        finally:
            return result
class Salt_http:
    '''get the result of command by http'''
    def __init__(self):
        pass
    def post(self,master,port,token,path,data,method='POST'):
        try:
            header = {"token" :token, "Content-Type": "application/json"}
            conn = httplib.HTTPConnection(master, port)
            conn.connect()
            content = json.dumps(data)
            conn.request(method, path, content, header)
            result = json.loads(conn.getresponse().read())
            conn.close()
        except Exception,e:
            result=get_result(1,e.message)
        finally:
            return result

    def get(self,master,port,token,path,method='GET'):
        try:
            header = {"token" :token, "Content-Type": "application/json"}
            conn = httplib.HTTPConnection(master, port)
            conn.connect()
            conn.request(method, path,'',header)
            result = json.loads(conn.getresponse().read())
            conn.close()
        except Exception,e:
            result=get_result(1,e.message)
        finally:
            return result
