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

commands = [command for command in sys.argv]
command_aliases = {
	'snapshot': create_and_copy
}

if len(commands) > 1:
	command_aliases[commands[1]]('.myvcs')