## Using SSH - Troubleshooting Guide

This document details how to remotely access your beaglebone from the command line using SSH
It currently covers 
* basic login
* passwordless login
You will need to know the IP of your beaglebone before starting, if unsure please see the **networking tutorial** _LINK HERE_ for details on how to set this up

Troubleshooting:

1. "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!"

- if this message comes up, it usually means that you have switched to accessing another beaglebone which has the same IP address as the previous one
- this can also happen when switching to a new SD card using the same beaglebone (effectively the same thing)
- to resolve this, we need to remove our local reference to the, as follows (where 192.168.2.14 is the IP of your beaglebone)
$ ssh-keygen -R 192.168.2.14
- you should see:
/Users/grahambooth/.ssh/known_hosts updated.
Original contents retained as /Users/grahambooth/.ssh/known_hosts.old
- now login again and it should work

* TUTORIAL: Passwordless login

- logging into the beaglebone the traditional way (i.e. $ ssh debian@192.168.x.x) requires a password, which can become tedious to enter
- a passwordless approach involves generating a secure SSH public key on the device that connects to the beaglebone (the host)
- this key is then copied onto the beaglebone itself, the host becomes "trusted" and the password is no longer needed to gain access

* Generating a public SSH key on the host (i.e. a laptop)

- go into the hosts home directory
$ cd ~/
- check if an .ssh directory already exists
$ ls -al
- if not then create one (if there is then check if there is a id_rsa.pub
$ mkdir .ssh
- now go into the .ssh directory
$ cd .ssh
- invoke the command to generate the public key:
$ ssh-keygen -t rsa -C "yourname@yourdomain.ext"
or
$ ssh-keygen -b 1024 -t rsa -f id_rsa -P ""
- NOTE: choose the best of the above two approaches
- press enter when prompted for a file in which to save the key
- press enter when asked for a passphrase (no passphrase means no password is required on login)

* Copying the public key from the laptop to the beaglebone

- go into the local ssh directory, if you are not there already
$ cd ~/.ssh
-  
$ cat id_rsa.pub
- copy the response into the clipboard
- log into the beagle as normal (entering the password)
$ ssh debian@192.168.2.14
- cd into the home directory
$ /debian/home/
- create 

- go into the laptop's home directory
$ cd ~/
- check if an .ssh directory already exists
$ ls -al
- if not then create one (if there is then check if there is a id_rsa.pub
$ mkdir .ssh
- now go into the .ssh directory
$ cd .ssh
- check if an 'authorized_keys' file exists
$ ls -a
- if not, create one
$ touch authorized_keys
- edit the 'authorized_keys' file
$ nano authorized_keys
- paste the context of the clipboard onto a new line at the bottom of the file, then use CTRL+X to exit, choosing Y when prompted whether to save
- log out of the beaglebone 
$ exit
- log back in again, and no password should be required
$ ssh debian@192.168.2.14

Troubleshooting

- Here are a couple of common problems and ways to fix them:

1. Public key (on the host) does not feature within authorized_keys (on the beaglebone)

- many problems can stem from this mismatch
- to double check, view the public key of the host, as follows:
$ cat ~/.ssh/id_dsa.pub
- now remove the sd card from the beaglebone, mount it on your laptop, then:
$ cat /Volumes/rootfs/home/debian/.ssh/authorized_keys
- check to see if any item within authorized_keys matches the host public key
- using this knowledge it should be possible to regain entry to the beaglebone and re-add the host's public key to beagle bone's authorized_keys as above

2. Inaccurate known_hosts file on the host machine

- the known_hosts file on the host machine may contain the wrong key for the beaglebone
- (this has happened to me in the past, not sure why exactly)
- edit the host machine's known_hosts file:
$ sudo nano ~/.ssh/known_hosts
- look for the line which matches the IP of the beaglebone you are trying to connect to e.g. line beginning 192.168.2.14 
- cut the line from the CTRL+K. then exit using CTRL+X, choosing Y when prompted whether to save
- attempt to access the beaglebone again via ssh e.g.
$ ssh debian@192.168.2.14
- login should now be possible
