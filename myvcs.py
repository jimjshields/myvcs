# cli arguments
import sys
# for file/directory operations
import os
# for copying directories
import shutil
# for catching errors
import errno


# part 1 - basic backups

# 1 - single backup
def create_and_copy(name):
	"""recursively copy all of the files and directories from src to dest"""

	# get the source and destination
	src = os.getcwd()
	dest = os.path.join(src, name)

	# if the destination doesn't exist, create it
	if not os.path.exists(dest):
		os.mkdir(dest)
		print "Created %s" % (dest)

	snapshots = [int(snapshot) for snapshot in os.listdir(dest)]

	if not snapshots:
		dest = os.path.join(dest, '1')
		copy_tree(src, dest, name)
	else:
		dest = os.path.join(dest, str(max(snapshots) + 1))
		copy_tree(src, dest, name)

def copy_tree(src, dest, name):
	for item in os.listdir(src):
		if item != name:
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

def remove_tree(folder, ignore_name):
	for item in os.listdir(folder):
		print 'Removing current files/folders...'
		if item != ignore_name:
			f = os.path.join(folder, item)
			if os.path.isdir(f):
				shutil.rmtree(f)
			else:
				os.remove(f)

def revert(snapshot_dir, snapshot, dest):
	reversion_dir = os.path.join(snapshot_dir, snapshot)
	remove_tree(dest, '.myvcs')
	copy_tree(reversion_dir, dest, 'myvcs')


commands = [command for command in sys.argv]
command_aliases = {
	'snapshot': create_and_copy,
	'revert': revert
}

if len(commands) > 1:
	if commands[1] == 'snapshot':
		create_and_copy('.myvcs')
	elif commands[1] == 'revert':
		if not commands[2]:
			print "You need a snapshot to revert to!"
		else:
			# MUST be in the main project dir
			dest = os.getcwd()
			snapshot_dir = os.path.join(dest, '.myvcs')
			snapshot = commands[2]
			revert(snapshot_dir, snapshot, dest)