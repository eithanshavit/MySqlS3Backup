MySQL S3 Backup Utility
=============

Simply utility developed in Python to backup MySQL databases and log and archive of backups on Amazon S3.

Requirements
--------------

Requires boto. Install by:

	pip install boto
	
Configuration
--------------

Open settings.py and insert your database settings along with your S3 credentials.

Usage
--------------

To run one-time, simply:

	python backup.py
	
Alternatively, you can set it up as a CRON. For example:

	0 * * * * (cd /location/to/script/; python backup.py)