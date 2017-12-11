import cgi
import datetime

now = datetime.datetime.now()
now = str(now)
now = now.replace(".","")
now = now.replace(" ","")
#print now
a="filename=\"p1.c\" Content-Type: text/x-csrc #include #include #include #include void main() { key_t key = 1234; int *value; int shmid = shmget(key, sizeof(int), IPC_CREAT | 0666); value = shmat(shmid, NULL, 0); *value = 10; printf(\"Program 1 : %d\n\", *value); sleep(5); printf(\"Program 1: %d\n\", *value); shmdt(value); shmctl(shmid, IPC_RMID, NULL); }"
a=a.split("Content-Typex: text/x-python")
#a=a.split("Content-Typex: text/x-python")
print a
flnm=a[0].split("filename=\"")
flnm=flnm=flnm[1].split("\"")
flnm=now+flnm[0]
print flnm
#print a[1]
#file = open("testfile.txt","w")
#file.write(a[1])
#formData = cgi.FieldStorage()
#print formData
