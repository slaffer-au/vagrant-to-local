#!/usr/bin/python

import os
import sys
import subprocess
import getpass
import re


def find_sys(user):

    platform = sys.platform
    if platform == 'linux2':
        user_path = '/home/%s/' % user
    elif platform == 'darwin':
        user_path = '/Users/%s/' % user
    else:
        print "Platform type unknown!"
        exit
    return user_path


def setup(user_path):    
    
    l_conf_file = user_path+".ssh/config"
    v_marker = "#aaaa"
    
    try:
        l_config = open(l_conf_file, "r+" )
    except IOError:
        print "Error opening %s." % l_conf_file
    
    l_conf_read = l_config.read()   
    
    try:       
        comments = '''#--- Included by v2l for local vagrant aliases. Do not manually edit between markers. ---#\n'''
        
        if comments not in l_conf_read:
            print "I couldn't find the comment"
            l_config.seek(0, os.SEEK_END)
            l_config.write("\n%s\n\n" % comments)
            
        if v_marker not in l_conf_read: 
            print "I couldn't find the marker"
            l_config.seek(0, os.SEEK_END)   
            l_config.write(v_marker+'\n'+v_marker+'\n')
            
    except IOError:
        print "Failed to write to %s" % l_conf_file
        
    l_config.close()
    
    return l_conf_file



def vagrant_hosts():
    
    v_output = ['vagrant', 'ssh-config'] 
    egrep = "Host |HostName|Port"
    v_grep = ['egrep', egrep]
    
    try:
        vm_info = subprocess.Popen(v_output, stdout=subprocess.PIPE)
        vm_grep = subprocess.check_output(v_grep, stdin=vm_info.stdout)
    except subprocess.CalledProcessError:
        print "Not a Vagrant directory"
    
    print "Making the following hosts available outside of Vagrant:"
    print vm_grep
    
    return str(vm_grep)


def read_it(user_path):
    
    v_hosts = open(setup(user_path), "r+")    
    v_hosts_read = v_hosts.read()
    v_hosts.close()
    
    print "This is v_hosts_read:\n%s " % v_hosts_read
    return v_hosts_read


def sub_it(vm_grep, v_hosts_read):
    
    if not vm_grep:
        print "Couldn't find previous Vagrant SSH configuration."
        return v_hosts_read
    
    v_hosts_grep = re.compile('#aaaa\n(.*?)#aaaa', re.DOTALL)
    v_hosts_write = re.sub(v_hosts_grep, '#aaaa\n'+vm_grep+'#aaaa' , v_hosts_read)
    
    print "This is what we're writing now:\n%s " % v_hosts_write
    return v_hosts_write


def write_it(v_hosts_write):
    
    if not v_hosts_write:
        exit
        
    v_hosts = open(setup(user_path), "w+")
    v_hosts.write(str(v_hosts_write))
    v_hosts.close()
    

# Main
user = getpass.getuser()
user_path = find_sys(user)
write_it(sub_it(vagrant_hosts(), read_it(user_path))) 



