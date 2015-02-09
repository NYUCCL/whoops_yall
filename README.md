whoops_yall
===========

Whoops ya'll is a psiTurk compatible experiment for paying people when an experiment goes badly for some reason.  You enter the workerIds of people who you owe money to and can reject all others.  Payment is handled quickly and easily via psiTurk's command line features.  When you make a whoops, use "whoops ya'll" 

** THIS IS BETA SOFTWARE.  IT HAS NOT BEEN TESTED MUCH AT ALL.  CONTRIBUTIONS WELCOME **

How to use
----------

Breifly, assuming you have psiturk installed, working, have the AWS credentials and an
account on psiturk.org.

**Get the repo**  

1. `git clone git@github.com:NYUCCL/whoops_yall.git`  

**Make it yours**  

1. `cd whoops_yall` - change to the project folder  
1. edit `config.txt` to your liking (particular setting `host` to 0.0.0.0 if you plan to run on the public internet, also fill in the `contact_email_on_error`, your university/organization name, etc...) 
1. edit the `templates/ad.html` file to reflect your university/organization and to identify yourself to workers 
1. `pip install shortuuid` as a dependency

**Update the database** 

1. `psiturk` - launch psiturk  
1. `[psiTurk server:off mode:sdbx #HITs:0]$ server on` - start server  
1. visit http://SERVER/dashboard (e.g., http://localhost:22362/dashboard)
1. login with the credentials you provided in the config.txt
1. enter worker ids and bonus amounts
1. listed below is a status list of where each person got in the reimbursement task.  also listed are "completion codes"... random codes you should send to worker who had problems to identify them uniquely.

**Test the end-user code**  

1. `psiturk` - launch psiturk if it is not already running
1. `[psiTurk server:off mode:sdbx #HITs:0]$ server on` - start server if not already running
1. `[psiTurk server:on mode:sdbx #HITs:0]$ debug` - test it locally  (will pop open a browser stepping you through)
1. `[psiTurk server:on mode:sdbx #HITs:0]$ create hit` - to create the hit on the AMT sandbox
1. Test the experiment by finding your listing on the Amazon sandbox (keep in mind the workerId and completion code
must be valid)

**Run live**  

1. If all is going well and looks how you expect, `[psiTurk server:on mode:sdbx #HITs:0]$ mode` - to switch to "live" mode  
1. `[psiTurk server:on mode:live #HITs:0]$ create hit` - to create the hit on the live server, usually something like 0.01 (minium price) 
1. `[psiTurk server:on mode:live #HITs:0]$ worker approve --hit <yourhitid>` - to approve and pay everyone who has finished
1. `[psiTurk server:on mode:live #HITs:0]$ worker bonus --hit <yourhitid> --auto` - to assign bonuses to everyone who has completed
the task correctly

