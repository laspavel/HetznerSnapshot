# Create Hetzner snapshot #

Create Hetzner snapshot

**Requirements:**
* python3 and python3-pip

**Configuration:**

Update script parameters:
* alarm_telegram_id - telegram id for send creating snapshot status.
* telegram_token - 
* api_timeout - API Hetzner timeout (sec)
* api_token - Hetzner API token ([See documentation](https://docs.hetzner.com/cloud/api/getting-started/generating-api-token/))
* server_name - ServerName for backup
* backup_timeout - Time after which the status will be checked.
* snapshot_templ_name - Snapshot template name  (Example, final name for snapshot_templ_name='server1_autobackup_' - server1_autobackup_2024-01-02 09:20:41.634323)

**Usage in terminal:**
```
python3 HetznerSnapshot1.py
```

**Usage in cron:**
```
45 4 * * 1 opc cd /home/opc/scripts && python3 HetznerSnapshot1.py
```

## License ##

MIT / BSD

## Author Information ##

This script was created in 2024 by [Pavel Lashkevych](https://laspavel.top/).