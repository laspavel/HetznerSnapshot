#!/usr/bin/env python3

import os
import time
import json
import logging
import traceback
import requests
from datetime import datetime
from dotenv import load_dotenv

# === Load environment ===
load_dotenv()

HETZNER_API_TOKEN = os.getenv('HETZNER_API_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
SERVER_NAME = os.getenv('SERVER_NAME')
SNAPSHOT_PREFIX = os.getenv('SNAPSHOT_PREFIX', 'autobackup_')
BACKUP_TIMEOUT = int(os.getenv('BACKUP_TIMEOUT', 1200))
POLL_INTERVAL = 15

API_TIMEOUT = 60
LOG_FILE = '/var/log/HetznerSnapshot1.log'

logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

def send_telegram_message(msg):
    if TELEGRAM_CHAT_ID and TELEGRAM_TOKEN:
        try:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": msg
            }
            response = requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
                json=payload,
                timeout=API_TIMEOUT
            )
            response.raise_for_status()
        except Exception as e:
            logging.warning(f"Failed to send Telegram message: {e}")

def hetzner_request(method, endpoint, **kwargs):
    url = f'https://api.hetzner.cloud/v1/{endpoint}'
    headers = {'Authorization': f'Bearer {HETZNER_API_TOKEN}','Content-Type': 'application/json'}
    response = requests.request(method, url, headers=headers, timeout=API_TIMEOUT, **kwargs)
    response.raise_for_status()
    return response.json()

def get_server_id(name):
    servers = hetzner_request('GET', 'servers')['servers']
    for server in servers:
        if server['name'] == name:
            return server['id']
    raise RuntimeError(f"Server '{name}' not found")

def list_snapshots():
    return hetzner_request('GET', 'images?type=snapshot')['images']

def delete_snapshot(snapshot_id):
    hetzner_request('DELETE', f'images/{snapshot_id}')
    logging.info(f"Deleted old snapshot ID: {snapshot_id}")

def create_snapshot(server_id, snapshot_name):
    payload = {'description': snapshot_name,'type': 'snapshot'}
    hetzner_request('POST', f'servers/{server_id}/actions/create_image', json=payload)
    logging.info(f"Requested snapshot creation: {snapshot_name}")

def wait_for_snapshot(snapshot_name):
    deadline = time.time() + BACKUP_TIMEOUT
    while time.time() < deadline:
        snapshots = list_snapshots()
        for snap in snapshots:
            if snap['description'] == snapshot_name and snap['status'] == 'available':
                logging.info("Snapshot ready.")
                return True
        logging.info("Waiting for snapshot...")
        time.sleep(POLL_INTERVAL)
    return False

def main():
    try:
        snapshot_name = SNAPSHOT_PREFIX + datetime.now().strftime("%Y%m%d_%H%M%S")
        logging.info(f"Starting backup for server: {SERVER_NAME}")

        server_id = get_server_id(SERVER_NAME)

        # Удаляем предыдущие снапшоты с этим префиксом
        for snapshot in list_snapshots():
            if snapshot['description'].startswith(SNAPSHOT_PREFIX) and snapshot['status'] == 'available':
                delete_snapshot(snapshot['id'])

        # Создаём новый снапшот
        create_snapshot(server_id, snapshot_name)

        # Ждём его готовности
        if not wait_for_snapshot(snapshot_name):
            raise RuntimeError(f"Snapshot not available after {BACKUP_TIMEOUT} seconds")

        msg = f"✅ Hetzner snapshot created: {snapshot_name}"
        logging.info(msg)
        send_telegram_message(msg)

    except Exception as e:
        error_msg = f"❌ Backup failed: {e}\n{traceback.format_exc()}"
        logging.error(error_msg)
        send_telegram_message(error_msg)

if __name__ == '__main__':
    main()
