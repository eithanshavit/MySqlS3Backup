MySQL S3 Backup Utility
--------------

Simple utility to store database backup (MySQL) on Amazon S3.

Requirements
=============

Requires boto. Install by:

	pip install boto

Usage
=============

To run one-time, simply:

	python backup.py
	
Alternatively, you can set it up as a CRON. For example:

0 * * * * (cd /location/to/script/; python backup.py)