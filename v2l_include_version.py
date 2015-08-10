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


def include_setup(user_path):    
    
    l_conf_file = user_path+".ssh/config"
    v_hosts = user_path+".ssh/vagrant_hosts"
    v_include = "include %s" % v_hosts
    
    try:
        l_config = open(l_conf_file, "r+" )
    except IOError:
        print "Error opening %s." % l_conf_file
    
    l_conf_read = l_config.read()   
    print l_conf_read 
    
    try:       
        comments = '''#--- Included by v2l for local vagrant aliases. Do not manually edit this section. ---#'''
        
        if comments not in l_conf_read:
            print "I couldn't find the comment"
            l_config.seek(0, os.SEEK_END)
            l_config.write("\n%s\n\n" % comments)
            
        if v_include not in l_conf_read: 
            print "I couldn't find the include line"
            l_config.seek(0, os.SEEK_END)   
            l_config.write(v_include+'\n')
            
    except IOError:
        print "Failed to write to %s" % l_conf_file
        
    l_config.close()
    return v_hosts



def vagrant_hosts(user_path):
    
    v_output = ['vagrant', 'ssh-config'] 
    egrep = "Host |HostName|Port"
    v_grep = ['egrep', egrep]
    vm_info = subprocess.Popen(v_output, stdout=subprocess.PIPE)
    vm_grep = subprocess.check_output(v_grep, stdin=vm_info.stdout)
    
    print "Making the following hosts available outside of Vagrant:"
    print vm_grep
    
    v_hosts = open(include_setup(user_path), "w+")
    v_hosts.write(vm_grep)
    v_hosts.close()

# Main
user = getpass.getuser()
user_path = find_sys(user)
vagrant_hosts(user_path) 


