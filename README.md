# HetznerSnapshot – Automated Snapshot Creation for Hetzner Cloud

HetznerSnapshot is a lightweight Python script designed to automate the creation of snapshots for Hetzner Cloud servers. It integrates with Telegram to provide real-time notifications about the snapshot creation status.​

## 📌 Features

* Automated snapshot creation for specified Hetzner Cloud servers​
* Customizable snapshot naming with timestamp support​
* Configurable API and backup timeouts​
* Telegram integration for status notifications​
* Suitable for scheduling via cron for regular backups​
* SimpleBackups Help Center

## ⚙️ Requirements

* Python 3.x​
* Hetzner Cloud API token with appropriate permissions​
* Telegram bot token and chat ID (for notifications)​

## 🚀 Installation

1) Clone the repository:​

```bash
git clone https://github.com/laspavel/HetznerSnapshot.git
cd HetznerSnapshot
```

2) Install dependencies:​
The script uses standard Python libraries. If any additional packages are required, install them using:

```bash
pip install -r requirements.txt
```

## 🛠️ Configuration

Before running the script, update the following parameters in HetznerSnapshot1.py:​

* alarm_telegram_id: Telegram chat ID to receive notifications​
* telegram_token: Token for your Telegram bot​
* api_timeout: Timeout for Hetzner API requests (in seconds)​
* api_token: Your Hetzner Cloud API token​
* server_name: Name of the Hetzner server to snapshot​
* backup_timeout: Time to wait before checking snapshot status (in seconds)​
* snapshot_templ_name: Template for naming snapshots (e.g., server1_autobackup_ will result in names like server1_autobackup_2024-01-02 09:20:41.634323)​

## 🧪 Usage

### Manual Execution
Run the script directly from the terminal:​

```bash
python3 HetznerSnapshot1.py
Scheduled Execution with Cron
```

### Scheduled Execution with Cron
To automate snapshot creation, add a cron job. For example, to run the script every Monday at 4:45 AM:​

```bash
45 4 * * 1 cd /path/to/HetznerSnapshot && python3 HetznerSnapshot1.py
```

Replace ```/path/to/HetznerSnapshot``` with the actual path to the script directory.​

## 📄 License

MIT License.​

## 🤝 Contributions

Suggestions and improvements are welcome! Feel free to open an issue or submit a pull request.

## 📬 Contact

Author: [laspavel](https://github.com/laspavel)

Feel free to reach out with questions or ideas.

---
