__author__ = 'jinhongjun'
#coding=utf-8
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
