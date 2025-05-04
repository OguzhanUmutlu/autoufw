# autoufw
A python script that listens for a given list of ports and lets you filter out IP addresses and allow them to access that port using UFW api. Made for Linux.

This is useful if you have a private Minecraft server with a public IP.

The default ports.txt includes the 25565 (default Minecraft port).

You can change it to the port you use or even add multiple by adding a new line and putting the port there.

Run the python script preferably in `sudo` and in a screen package like `tmux` so that it can run in the background (Useful if you are using a terminal based server)

## Installation

First clone it: `git clone https://github.com/OguzhanUmutlu/autoufw`

Then get in the folder `cd autoufw`

Now just run it (preferably) in sudo mode: `sudo python3 main.py`

When you want to add an IP just get in the `tmux` instances by listing the instances with `tmux ls` and selecting the ID of the screen by using `tmux attach -t ID_HERE`. Then write `clear`, press enter. This will clear the queue of the IPs. Now let your friend try to join the server, now get back to the instance, press Enter. This will now show all the IPs that tried to reach the server. You can Allow the IP, Ban the IP or Skip it. Banning it will result in it being ignored from that point on. You can unban it by editing the `bad_ips.txt` file and restarting the python script.
