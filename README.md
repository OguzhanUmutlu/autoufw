# 🔥 AutoUFW

**A dynamic UFW management tool for managing IP access to your server in real time.**

AutoUFW is a Python script that monitors incoming connections on specified ports (e.g., a Minecraft server), allows you to review unknown IPs, and easily decide whether to allow or ban them — all via an interactive terminal interface.

---

## 📌 Features

* 🔍 **Live Monitoring**: Listens for connections on custom TCP ports using `tcpdump`.
* ✅ **Allow or Ban**: Easily whitelist or blacklist new IP addresses interactively.
* 🔐 **UFW Integration**: Automatically manages `ufw` (Uncomplicated Firewall) rules based on your decisions.
* 🧠 **Persistent Memory**: Keeps track of:

  * Allowed IPs (`ips.txt`)
  * Banned IPs (`bad_ips.txt`)
  * Ports to listen on (`ports.txt`)
* 🧾 **Rule Cleanup**: Automatically removes outdated or unlisted IP rules from UFW.
* 🔧 **Multi-Port Support**: Monitor one or multiple ports.
* 🖥️ **Command Interface**: Includes a mini-command console for managing state (`clear`, `list`, `status`, `exit`).
* 📓 **Commenting**: Add descriptions to allowed IPs for clarity.
* ⚙️ **Threaded**: Each port is monitored in its own thread for responsiveness.
* 💼 **Linux Compatible**: Designed for Linux systems using `sudo` and UFW.

---

## 🚀 Installation

```bash
git clone https://github.com/OguzhanUmutlu/autoufw
cd autoufw
```

Ensure `tcpdump` and `ufw` are installed:

```bash
sudo apt install tcpdump ufw
```

Run the script:

```bash
sudo python3 main.py
```

---

## 📝 Usage

### 1. **Configure Your Ports**

Edit `ports.txt` and list the ports you want to monitor, one per line. For example:

```
25565
80
443
```

### 2. **Start Monitoring**

Run the script (preferably in a persistent terminal like `tmux`):

```bash
sudo python3 main.py
```

Each time a new IP attempts to connect to any listed port, it will be added to a pending queue.

### 3. **Interact with the Script**

At any time, press **Enter** to interact.

Available commands:

* `clear`: Clear the pending IP queue.
* `list`: Show pending IPs, allowed IPs, banned IPs, and monitored ports.
* `status`: Show current UFW status.
* `exit`: Cleanly stop the script and kill tcpdump processes.

### 4. **Review New IPs**

You’ll be prompted for each new IP:

```
New IP detected: 123.45.67.89
[A]llow, [B]an, [S]kip?
```

* **A**: Allow IP — adds to `ips.txt`, applies UFW rules, and optionally add a comment.
* **B**: Ban IP — adds to `bad_ips.txt` and ignores it from now on.
* **S**: Skip — take no action for now.

---

## 💡 Recommended Setup (Persistent Monitoring)

To keep the script running in the background on a terminal-only server:

```bash
sudo apt install tmux
tmux new -s autoufw
sudo python3 main.py
```

To detach from tmux: press `Ctrl + B`, then `D`.
To reattach later:

```bash
tmux ls
tmux attach -t autoufw
```

---

## 🔄 Editing IPs Manually

* To **unban** an IP: remove it from `bad_ips.txt` and restart the script.
* To **remove an allowed IP**: delete it from `ips.txt`, and UFW rules will be cleaned on next check.

---

## ⚠️ Notes

* Requires `sudo` access to use `tcpdump` and modify firewall rules.
* Only works on Linux systems that use `ufw`.

---

## 📁 Files

* `main.py`: Main script.
* `ips.txt`: Whitelisted IPs (you can add manually too).
* `bad_ips.txt`: Blacklisted IPs (ignored forever).
* `ports.txt`: List of ports to monitor (one per line).

---

## 📜 License

MIT License — use freely, modify as you like, give credit when possible.
