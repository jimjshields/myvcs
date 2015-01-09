# My Version Control System

### Part 1 - Basic backups

1. Single backup
  * Command line tool
  * Recursively copies everything in the current directory to a directory called `.myvcs`
  	* directory should be created if it doesn't exist
  	* can overwrite if it exists (for now)
2. Snapshots
  * put first backup into myvcs/1, second into myvcs/2, etc.
3. Reversion
  * add an option to the tool to revert to an earlier snapshot
4. Latest snapshot
  * 'latest' should revert to the latest snapshot

### Part 2 - Metadata

1. Current backup
  * make a file called .myvcs/head that keeps track of which backup you're currently 'using.'