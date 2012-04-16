# #LDNRealtime Live Router Stats

## Operation:
1. Configure your router (I used a Cisco 2621XM) to expose SNMP data on your local subnet. (You can expose it a lot easier potentially, if you have a public IP)2. edit the "R" value in poller.py and linepoller.py, to set the Router's IP address/
3. Install Redis.
4. Install SNMP Tools (snmpget)
5. Create an Amazon EC2 micro instance. 
6. Create a VM on a machine inside your network.
7. Create some SSH keys on your local VM, and deploy those to login to your EC2 instance passwordlessly.
8. Run poller.py and linepoller.py every 30 ish seconds.
9. I did this with `watch -n 30 python poller.py`

## How it works:
1. snmpget grabs the counters for fa0/0 and fa0/1. 
2. Simple code calculates a delta.
3. Insanely simple code creates a blob of JSON
4. This is saved to a file in tmp/
5. subprocess shells out to scp, using a public key authentication, and uploads it to the EC2 instance (or wherever you want).
6. Apache running on the EC2 instance (with AddType application/json .json) presents it to the GeckoBoard.

