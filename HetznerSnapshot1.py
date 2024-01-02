#!/usr/bin/env python3

# Create Hetzner snapshot

from datetime import datetime
from time import sleep
import json
import requests
import traceback

# Get from @getidsbot
alarm_telegram_id='xxxxxxxx'

# Get from @BotFather
telegram_token='xxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# API Hetzner timeout (sec)
api_timeout=60

# API token https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/)
api_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Backup server name
server_name='server1'

# Backup timeout 
backup_timeout=1200

# Snapshot template name
snapshot_templ_name="server1_autobackup_"

def SendMsgToRelegram(chat='',msg=''):
    if len(chat) and len(msg)>0:
        msg_data={"chat_id": chat, "text": msg}
        rapi=requests.post('https://api.telegram.org/bot'+telegram_token+'/sendMessage', data=json.dumps(msg_data), headers={'Content-Type': 'application/json','X-Token': api_token},timeout=api_timeout)    
    try:
        rapi.raise_for_status()
    except requests.HTTPError as expt:
        print('ERR010 - TelegramAPIErrorCode: '+str(expt.response.status_code)+' Status:'+str(rapi.text))
        exit(0)
    result=json.loads(rapi.text)
    return result

def getServers():
    rapi=requests.get('https://api.hetzner.cloud/v1/servers', headers={'Content-Type': 'application/json','Authorization': 'Bearer '+api_token},timeout=api_timeout)
    try:
        rapi.raise_for_status()
    except requests.HTTPError as expt:
        SendMsgToRelegram(chat=alarm_telegram_id,msg='ERR001 - HetznerAPIErrorCode: '+str(expt.response.status_code)+' Status:'+str(rapi.text))
        exit(0)
    result=json.loads(rapi.text)
    return result

def getBackup():
    rapi=requests.get('https://api.hetzner.cloud/v1/images?type=snapshot', headers={'Content-Type': 'application/json','Authorization': 'Bearer '+api_token},timeout=api_timeout)
    try:
        rapi.raise_for_status()
    except requests.HTTPError as expt:
        SendMsgToRelegram(chat=alarm_telegram_id,msg='ERR002 - HetznerAPIErrorCode: '+str(expt.response.status_code)+' Status:'+str(rapi.text))
        exit(0)
    result=json.loads(rapi.text)
    return result

def DeleteBackup(id):
    rapi=requests.delete('https://api.hetzner.cloud/v1/images/'+str(id), headers={'Content-Type': 'application/json','Authorization': 'Bearer '+api_token},timeout=api_timeout)
    try:
        rapi.raise_for_status()
    except requests.HTTPError as expt:
        SendMsgToRelegram(chat=alarm_telegram_id,msg='ERR003 - Hetzner APIErrorCode: '+str(expt.response.status_code)+' Status:'+str(rapi.text))
        exit(0)

def CreateBackup(snapshot_name='Snapshot',server_uid=''):
    snapshot_data={'description':snapshot_name,'type':'snapshot'}
    rapi=requests.post('https://api.hetzner.cloud/v1/servers/'+str(server_uid)+'/actions/create_image', data=json.dumps(snapshot_data), headers={'Content-Type': 'application/json','Authorization': 'Bearer '+api_token},timeout=api_timeout)
    try:
        rapi.raise_for_status()
    except requests.HTTPError as expt:
        SendMsgToRelegram(chat=alarm_telegram_id,msg='ERR004 - Hetzner APIErrorCode: '+str(expt.response.status_code)+' Status:'+str(rapi.text))
        exit(0)
    result=json.loads(rapi.text)
    return result
    
try:
    servers=getServers()
    server_uid='0'
    for server in servers['servers']:
        if server['name']==server_name:
            server_uid=server['id']
            break
    if server_uid==0:
        raise RuntimeError('ERR005 - Hetzner getServers() failed')
    
    backups_data=getBackup()
    d=1
    for backup_data in backups_data['images']:
        print(backup_data)
        if (backup_data['description'].find(snapshot_templ_name)>-1) and backup_data['status']=='available':
            DeleteBackup(backup_data['id'])
            d+=1
    if d>1: 
        new_backup_data=CreateBackup(snapshot_templ_name+str(datetime.now()),server_uid)
        sleep(backup_timeout)
        new_backup_info=getBackup()
        m=1
        for new_info in new_backup_info['images']:
            if (new_info['description'].find(snapshot_templ_name)>-1) and new_info['status']=='available':
                m+=1
                
        if m==1:
            raise RuntimeError('ERR004 - Hetzner Snapshot creation failed')
                
    SendMsgToRelegram(chat=alarm_telegram_id,msg='INFO001 - HetznerSnapshotScript OK')
            
except Exception as inst:
    if str(inst).find('ERR0')<0:
        err='ERR099 - HetznerSnapshotScript fatal error. Details:'+str(inst)
    else:
        err=str(inst)
    print(err)
    SendMsgToRelegram(chat=alarm_telegram_id,msg=err+ ' '+traceback.format_exc())
finally:
    exit(0)
