# #LDNRealtime Live Router Stats

## Operation:

1. Configure your router (I used a Cisco 2621XM) to expose SNMP data on your local subnet. (You can expose it a lot easier potentially, if you have a public IP)
2. Edit the "R" value in poller.py and linepoller.py, to set the Router's IP address/
3. Install Redis.
4. Install SNMP Tools (snmpget)
5. ~~Create an Amazon EC2 micro instance.~~
6. Create a VM on a machine inside your network.
7. Create some SSH keys on your local VM, and deploy those to login to your VM instance passwordlessly.
8. Run poller.py every 30 ish seconds.
9. I did this with `watch -n 30 python poller.py`
9. Run web.py every 30 seconds too. (this builds core.html from the template)
9. Run tweet.py every 120 seconds. (this runs the twitter bot/service)
9. Run rotate every 3600 seconds. (this stops the redis hashes getting too huge)

## How it works:
1. snmpget grabs the counters for fa0/0 
2. Simple code calculates a delta.
3. Jinja2 template describes the outline of the page, and the code drops the Redis data into the data: block in the page.
4. The page is written to core.html
5. There's an insanely simple tweepy script to post to twitter.
6. There's another script to see how big the redis hashes are getting, and rotate them out of the way every hour or so (if they're big)

## Example Output
http://www.wibblesplat.com

