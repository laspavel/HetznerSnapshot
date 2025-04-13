# HetznerSnapshot – Automated Snapshot Creation for Hetzner Cloud

A Python-based utility to automate the creation and deletion of snapshots for Hetzner Cloud servers using the Hetzner API. This tool facilitates regular backups and integrates with Telegram for notifications.

## 📌 Features

* **Snapshot Creation**: Automatically create snapshots of specified Hetzner Cloud servers.
* **Snapshot Deletion**: Remove old snapshots matching a defined naming pattern.
* **Telegram Notifications**: Receive real-time updates on snapshot operations via Telegram.

## ⚙️ Requirements

* Python 3.6+: Ensure Python is installed on your system.
* Docker: Required for building the standalone binary.

## 🚀 Installation

1) Clone the repository:​

```bash
git clone https://github.com/laspavel/HetznerSnapshot.git
cd HetznerSnapshot
```

2) Build the Binary Using Docker: 

```bash
docker build --no-cache --file Dockerfile.build --tag hetznersnapshot2_build .
docker run --rm -v $(pwd):/dist hetznersnapshot2_build
chmod +x HetznerSnapshot2
```

This process will generate a standalone binary named HetznerSnapshot.bin in the project directory.

## 🛠️ Configuration

Configure the application using a .env file. An example configuration is provided in .env.example:

```ini
# Hetzner API token
HETZNER_API_TOKEN=your_hetzner_api_token

# Telegram bot token
TELEGRAM_TOKEN=your_telegram_bot_token

# Telegram chat ID for notifications
TELEGRAM_CHAT_ID=your_telegram_chat_id

# Name of the server to snapshot
SERVER_NAME=your_server_name

# Snapshot name prefix
SNAPSHOT_PREFIX=your_snapshot_prefix_

# Timeout for snapshot creation in seconds
BACKUP_TIMEOUT=1200
```
Rename .env.example to .env and replace the placeholder values with your actual credentials and preferences.

## 🧪 Usage

### Manual Execution
Run the script directly from the terminal:​

```bash
./HetznerSnapshot.bin
```

Ensure that the .env file is present in the same directory as the binary.


### Scheduled Execution with Cron

1) Automate the snapshot process by scheduling it with cron:

Open the crontab editor:

```bash
crontab -e
```
2) Add the following line to schedule the script (e.g., daily at 2 AM):

```
0 2 * * * /path/to/HetznerSnapshot/HetznerSnapshot2
```

Replace /path/to/HetznerSnapshot/ with the actual path to your project directory.

This setup will run the snapshot script daily at 2 AM, logging output to /var/log/HetznerSnapshot2.log.

## 📄 License

MIT License.​

## 🤝 Contributions

Suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

## 📬 Contact

Author: [laspavel](https://github.com/laspavel)

Feel free to reach out with questions or ideas.

---
