__author__ = 'jinhongjun'
#coding=utf-8
from salt_api.models import Minion,Master,Log,Module
import json
import re
from api import Salt_http,get_result
def log_all(func):
    '''decorate func to get log'''
    def handle(host,module_name,arg):
        try:
            host_contain=host+'#'
            host_detail=Minion.objects.filter(ip__contains=host_contain)
            if len(host_detail)==0:
                return get_result(1,'no this ip %s' %host)
                raise NameError
            host_name=host_detail[0].name
            try:
                salt_name=Module.objects.get(name=module_name).salt_name
                Log.objects.create(host=host,
                                   module=module_name,
                                   arg=str(arg),
                                   action='start')
                result=func(host_name,salt_name,arg)
                if result['retcode']==0:
                    host_result=result['stdout'][host_name]
                    result['stdout']={
                                        host:host_result
                                    }
                Log.objects.create(host=host,
                                   module=module_name,
                                   arg=str(arg),
                                   action='end',
                                   result=str(result))
            except Exception,e:
                result=get_result(1,e.message)
        except Exception,e:
            result=get_result(1,e.message)
        finally:
            return result
    return handle

def exec_cmd(host,module_name,arg):
    '''change the module_name to the salt_name and exec the command'''
    result=exec_cmd_salt(host,module_name,arg)
    return result

@log_all
def exec_cmd_salt(host_name,salt_name,arg):
    '''exec command by salt'''
    for master in Minion.objects.get(name=host_name).master.all():
        http_result=exec_cmd_salt_http(master,host_name,salt_name,arg)
        if http_result['retcode']==1:
            pass
        else:
            break
    return http_result

def exec_cmd_salt_http(master,host_name,salt_name,arg):
    '''exec salt command by http'''
    master_ip=master.ip
    master_port=master.port
    master_token=master.token
    send_data={
        'tgt':host_name,
        'func':salt_name,
        'arg':arg
    }
    result=Salt_http().post(master_ip,master_port,master_token,'/cmd',send_data)
    return result

# def exec_cmd_salt_ssh(master,host_name,salt_name,arg):
#     '''exec salt command by ssh'''
#     master_ip=master.ip
#     cmd='salt %s %s ' %(host_name,salt_name)
#     if arg:
#         arg=' '.join(arg)
#         cmd=cmd+arg+' --out=json'
#     else:
#         cmd=cmd+'--out=json'
#     result=SSH_result(master_ip).get(host_name,cmd)
#     return result

def salt_key():
    Master_all=Master.objects.all()
    master_result=[]
    for master in Master_all:
        master_ip=master.ip
        master_port=master.port
        master_token=master.token
        master_detail={
            'master':master.ip
        }
        result=Salt_http().get(master_ip,master_port,master_token,'/key/all')
        if result['retcode']==0:
            master_detail['key']=result['stdout']
        else:
            master_detail['key']=result['stderr']
        master_result.append(master_detail)
    return master_result


def salt_key_accept(master,host):
    try:
        m_master=Master.objects.get(ip=master)
        master_ip=m_master.ip
        master_port=m_master.port
        master_token=m_master.token
        send_data={'host':host}
        result=Salt_http().post(master_ip,master_port,master_token,'/key/accept',send_data)
        if result['retcode']==0 and result['stdout']==host:
            kernel_data={
                'tgt':host,
                'func':'grains.item',
                'arg':('kernel',)
            }
            ip_data={
                'tgt':host,
                'func':'network.ip_addrs',
                'arg':()
            }
            kernel_result=Salt_http().post(master_ip,master_port,master_token,'/cmd',kernel_data)
            if kernel_result['retcode']==0:
                m_kernel=kernel_result['stdout'][host]['kernel']
            else:
                m_kernel='none'
            ip_result=Salt_http().post(master_ip,master_port,master_token,'/cmd',ip_data)
            if ip_result['retcode']==0:
                m_ip='#'.join(ip_result['stdout'][host])+'#'
            else:
                m_ip='none'
            if len(Minion.objects.filter(name=host))==0:
                aa=Minion(ip=m_ip,kernel=m_kernel,name=host)
                aa.save()
                aa.master.add(m_master)
            else:
                aa_master=[x.ip for x in Minion.objects.get(name=host).master.all()]
                if master in aa_master:
                    Minion.objects.filter(name=host).update(kernel=m_kernel,ip=m_ip)
                else:
                    Minion.objects.get(name=host).master.add(m_master)
            result=get_result(0,'done')
        else:
            result=get_result(1,'failed')
    except Exception,e:
        result=get_result(1,e.message)
    finally:
        return result


def salt_key_delete(master_ip,host):
    try:
        minion=Minion.objects.get(name=host)
        minion_name=minion.name
        master=Master.objects.get(ip=master_ip)
        master_port=master.port
        master_token=master.token
        send_data={'host':minion_name}
        m_result=Salt_http().post(master_ip,master_port,master_token,'/key/delete',send_data)
        if m_result['retcode']==0:
            minion.master.remove(master)
        result=get_result(0,'all done')
    except Exception,e:
        result=get_result(1,e.message)
    finally:
        return result

def salt_minion_init(master_ip,host):
    try:
        minion=Minion.objects.get(name=host)
        master=Master.objects.get(ip=master_ip)
        master_port=master.port
        master_token=master.token
        send_data={
            'tgt':host,
            'func':'saltutil.sync_all',
            'arg':()
        }
    # if minion.ip.lower()=='none':
        ip_data={
            'tgt':host,
            'func':'network.ip_addrs',
            'arg':()
        }
        ip_result=Salt_http().post(master_ip,master_port,master_token,'/cmd',ip_data)
        if ip_result['retcode']==0:
            m_ip='#'.join(ip_result['stdout'][host])+'#'
        else:
            m_ip='none'
        minion.ip=m_ip
        minion.save()
        if minion.kernel.lower()=='none':
            kernel_data={
                'tgt':host,
                'func':'grains.item',
                'arg':('kernel',)
            }
            kernel_result=Salt_http().post(master_ip,master_port,master_token,'/cmd',kernel_data)
            if kernel_result['retcode']==0:
                m_kernel=kernel_result['stdout'][host]['kernel']
            else:
                m_kernel='none'
            minion.kernel=m_kernel
            minion.save()
        elif minion.kernel.lower()=='linux':
            pass
        elif minion.kernel.lower()=='windows':
            cp_data={
                'tgt':host,
                'func':'cp.get_dir',
                'arg':('salt://file/chardet', 'C:\\salt\\bin\\Lib',)
            }
            cp_result=Salt_http().post(master_ip,master_port,master_token,'/cmd',cp_data)
        else:
            pass
        m_result=Salt_http().post(master_ip,master_port,master_token,'/cmd',send_data)
        if m_result['retcode']==0:
            result=m_result
        else:
            result=m_result
    except Exception,e:
        result=get_result(1,e.message)
    finally:
        return result

def salt_module_name():
    try:
        private_module=Module.objects.filter(private_status=False)
        module_list=[{"name":x.name,"describe":x.describe} for x in private_module]
        result=get_result(0,module_list)
    except Exception,e:
        result=get_result(1,e.message)
    finally:
        return result
