#!/usr/env python

# cli arguments
import sys
# for file/directory operations
import os
# for copying directories
import shutil
# for catching errors
import errno
# date operations
from datetime import datetime

# where the testing will be done
PROJECT_DIR = '/Users/jimshields/Documents/Coding/hacker_school/myvcs/test_dir'
VCS_FOLDER = '.myvcs'

# part 1 - basic backups

# 1 - single backup

def initialize(name=VCS_FOLDER):
	"""create the initial folder if it's not yet there"""
	# get the source and destination
	src = PROJECT_DIR
	dest = os.path.join(src, name)

	# if the destination doesn't exist, create it
	if not os.path.exists(dest):
		os.mkdir(dest)
		head = os.path.join(dest, 'head')
		times = os.path.join(dest, 'times')
		open_write_close(head, '')
		open_write_close(times, '')
		print "Created:\nrepository: %s\nhead: %s\ntimelog: %s" % (dest, head, times)
	else:
		print "%s has already been initialized." % (name)

def create_snapshot(src, name=VCS_FOLDER):
	"""recursively copy all of the files and directories from src to dest"""

	snapshots = list_snapshots(name)
	dest = os.path.join(src, name)

	if not snapshots:
		snapshot = 1
		current = 1
		snapshot_dest = os.path.join(dest, str(snapshot))
		track_current_snapshot(snapshot)
		track_time(snapshot)
		os.mkdir(snapshot_dest)
		copy_tree(src, snapshot_dest, name)
	else:
		snapshot = max(snapshots) + 1
		current = int(current_snapshot())
		if max(snapshots) != current:
			print "You can't back up from an old snapshot! Get to the current snapshot and then back it up."
		else:
			snapshot_dest = os.path.join(dest, str(snapshot))
			track_current_snapshot(snapshot)
			track_time(snapshot)

			os.mkdir(snapshot_dest)
			copy_tree(src, snapshot_dest, name)

def copy_tree(src, dest, ignore_name=VCS_FOLDER):
	"""copy the tree from src to dest
	   ignore ignore_name"""

	for item in os.listdir(src):
		if item != ignore_name:
			s = os.path.join(src, item)
			d = os.path.join(dest, item)
			if os.path.isdir(s):
				print "Copying directory..."

				try:
					shutil.copytree(s, d)
				except OSError as e:
					# if it already exists
					if e.errno == errno.EEXIST:
						print "Path exists: %s" % (d)
			else:
				shutil.copy2(s, d)

def remove_tree(folder, ignore_name=VCS_FOLDER):
	"""recursively remove all files and folders from specified folder
	   ignore ignore_name"""
	for item in os.listdir(folder):
		if item != ignore_name:
			print 'Removing %s' % (item)
			f = os.path.join(folder, item)
			if os.path.isdir(f):
				shutil.rmtree(f)
			else:
				os.remove(f)

def revert(snapshot_dir, snapshot, dest):
	"""revert to the given snapshot"""
	track_current_snapshot(snapshot)
	reversion_dir = os.path.join(snapshot_dir, snapshot)
	remove_tree(dest)
	copy_tree(reversion_dir, dest, 'myvcs')

def latest(snapshot_dir, dest):
	"""revert to the latest snapshot"""
	snapshots = list_snapshots()
	latest_snapshot = str(max(snapshots))
	revert(snapshot_dir, latest_snapshot, dest)

def list_snapshots(name=VCS_FOLDER):
	"""get a list of all snapshots"""
	dest = os.path.join(PROJECT_DIR, name)
	snapshots = [int(i) for i in os.listdir(dest) if i not in ['head', 'times']]
	return snapshots

# part 2 - metadata
def track_current_snapshot(snapshot, name=VCS_FOLDER):
	"""track the current snapshot"""
	tracking_file = os.path.join(PROJECT_DIR, name, 'head')
	open_write_close(tracking_file, str(snapshot), overwrite=True)

def track_time(snapshot, name=VCS_FOLDER):
	time_file = os.path.join(PROJECT_DIR, name, 'times')
	now = stringify_time(datetime.now())
	open_write_close(time_file, '%s, %s\n' % (snapshot, now))

def open_write_close(file, contents, overwrite=False):
	if overwrite:
		f = open(file, 'w')
	else:
		f = open(file, 'a')
	f.write(contents)
	f.close()

def current_snapshot(name=VCS_FOLDER):
	"""display the current snapshot"""
	tracking_file = os.path.join(PROJECT_DIR, name, 'head')
	f = open(tracking_file, 'r')
	return f.read()
	f.close()	

def stringify_time(time):
	return time.strftime("%Y%m%d%H%M%S")

# parse the cli args
commands = [command for command in sys.argv]

# do things based on the commands
if len(commands) > 1:
	if commands[1] == 'init':
		initialize()
	elif commands[1] == 'snapshot':
		create_snapshot(PROJECT_DIR, VCS_FOLDER)
	elif commands[1] == 'revert':
		if not commands[2]:
			print "You need a snapshot to revert to!"
		else:
			snapshot_dir = os.path.join(PROJECT_DIR, VCS_FOLDER)
			snapshot = commands[2]
			revert(snapshot_dir, snapshot, PROJECT_DIR)
	elif commands[1] == 'latest':
		snapshot_dir = os.path.join(PROJECT_DIR, VCS_FOLDER)
		latest(snapshot_dir, PROJECT_DIR)
	elif commands[1] == 'current':
		print current_snapshot()