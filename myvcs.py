# for file/directory operations
import os

# part 1 - basic backups

# 1 - single backup

# method for creating the directory (if it's not there)
def create_dir():
	"""creates a directory in the current directory
	   called .myvcs"""
	os.mkdir('.myvcs')