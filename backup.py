#!/usr/bin/env python
import settings
import tarfile
import subprocess
import os
import boto
import tempfile
import mimetypes

from datetime import datetime
from datetime import timedelta

database_name = settings.DATABASES[ 'default' ][ 'NAME' ]
username = settings.DATABASES[ 'default' ][ 'USER' ]
password = settings.DATABASES[ 'default' ][ 'PASSWORD' ]

access_key = settings.AWS_ACCESS_KEY_ID
secret_key = settings.AWS_SECRET_ACCESS_KEY
bucket = settings.AWS_BACKUP_BUCKET_NAME

print "----- Start."
print "----- Dumping the " + database_name + " database at " + datetime.now().strftime( '%Y.%m.%d.%H.%M' )

# create structure file
backup_time = datetime.now().strftime( '%Y.%m.%d.%H.%M' )
mysqldumpCmd = "mysqldump --single-transaction -u %s -p%s --databases %s" % ( username, password, database_name )
dumpProc = subprocess.Popen( mysqldumpCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )

#create temp files
tf = tempfile.NamedTemporaryFile()
tf.write( dumpProc.communicate()[ 0 ] )

# write the last few kbs to the buffer
tf.flush()

#create tar.gz for the above two files
tar = tarfile.open( os.path.join( os.curdir, "%s_%s.tar.gz" % ( database_name, backup_time ) ), "w|gz" )
tar.add( tf.name, database_name + ".sql" )
#delete temp files
tf.close()
tar.close()

#upload the temp.tar.gz which is in the present direcotry to amazon S3
print "----- Connecting to Amazon S3"
s3 = boto.connect_s3( access_key, secret_key )

keyName = "MySql/%s/%s_%s.tar.gz" % ( database_name, database_name, backup_time )
print "----- Uploading the " + database_name + " database backup file to " + keyName + " on Amazon S3."
bucket = s3.get_bucket( bucket )
key = bucket.new_key( keyName )
key.set_contents_from_filename( os.path.join( os.curdir, "%s_%s.tar.gz" % ( database_name, backup_time ) ) )
key.set_acl( 'private' )

print "----- Cleaning up files used. "
rmProc = subprocess.Popen("rm %s_%s.tar.gz" % (database_name, backup_time,), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print "----- Finished."
