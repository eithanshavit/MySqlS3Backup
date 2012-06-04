import settings
import tarfile
import subprocess
import os
import boto
import tempfile
import mimetypes

from datetime import datetime
from datetime import timedelta

database_name = settings.DATABASES['default']['NAME']
username = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']

access_key = settings.AWS_ACCESS_KEY_ID
secret_key = settings.AWS_SECRET_ACCESS_KEY
bucket = settings.AWS_BACKUP_BUCKET_NAME

print "----- start."
print "----- dumping the " + database_name + " database at " + datetime.now().strftime('%Y.%m.%d.%H.%M')

# create structure file
backup_time = datetime.now().strftime('%Y.%m.%d.%H.%M')
proc1 = subprocess.Popen("mysqldump --no-data -u %s -p%s --databases %s" % (username, password, database_name,), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
proc3 = subprocess.Popen("mysqldump --no-create-info -u %s -p%s --databases %s" % (username, password, database_name,), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

#create temp files
t1 = tempfile.NamedTemporaryFile()
t2 = tempfile.NamedTemporaryFile()	
t1.write(proc1.communicate()[0])
t2.write(proc3.communicate()[0])

# write the last few kbs to the buffer
t1.flush()
t2.flush()

#create  tar.gz for the above two files
tar = tarfile.open(os.path.join(os.curdir, "%s_%s.tar.gz" % (database_name, backup_time,)), "w|gz")
tar.add(t1.name, database_name + "_struct.sql")
tar.add(t2.name, database_name + "_data.sql")	
#delete temp files
t1.close()
t2.close()	
tar.close()

#upload the temp.tar.gz which is in the present direcotry to amazon S3
print "----- uploading the " + database_name + " database backup file Amazon S3."

s3 = boto.connect_s3(access_key, secret_key)
bucket = s3.get_bucket(bucket)
key = bucket.new_key("/%s/%s_%s.tar.gz" % (database_name, database_name, backup_time,))
key.set_contents_from_filename(os.path.join(os.curdir, "%s_%s.tar.gz" % (database_name, backup_time,)))
key.set_acl('private')

print "----- cleaning up files used. "
proc2 = subprocess.Popen("rm %s_%s.tar.gz" % (database_name, backup_time,), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print "----- finished."
print "----- "
print "----- "
print "----- "
