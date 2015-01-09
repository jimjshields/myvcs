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
def copy(src, dest, name):
	"""recursively copy all of the files and directories from src to dest"""
	if os.path.exists(dest):
		shutil.rmtree(dest)

	os.mkdir(dest)
	print "Created %s" % (dest)

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

def create_and_copy(name):
	src = os.getcwd()
	dest = src + "/%s" % (name)
	copy(src, dest, name)

# 2 - snapshots
def create_snapshot(name):
	cwd = os.getcwd()
	snapshot_dir = "%s/%s" % (cwd, name)
	if not os.path.exists(name):
		os.mkdir(name)
	snapshots = []
	for item in os.listdir(snapshot_dir):
		snapshots.append(item)
	if not snapshots:
		create_and_copy('.myvcs/%s' % (1))
	else:
		create_and_copy('.myvcs/%s' % (max(snapshots) + 1))

# commands = {
# 	'dir': create_and_copy,
# 	'snapshot': create_snapshot
# }


first_command = sys.argv[1]
if first_command == 'dir':
	print 'cool'
	# create_and_copy('.myvcs')
elif first_command == 'snapshot':
	create_snapshot('.myvcs')