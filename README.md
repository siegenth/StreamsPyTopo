# StreamsPyTopo
Streams Python topology CI Template development.

Build and submit a Streams application in the IBM Clould.

Simple application that works with the StreamsProxy

** Notes
 - Push the tar up of the toolkits not the toolkit. 
 - Need to pull down the toolkit from github todo this right.
 - Use Maven, not shell.

I've bound the script to the job of a stage using the ${IDS_JOB_NAME}. 
The concept is to have the scripts checked in, 
look for the scripts in the ${HOME}/scripts directory. 

In the situations where we need credentials. Before this code starts,
the credential.py is unzipped from credential.pyz. 
This is the 'Build script' for the buildDeploy job of BuildDeployTopo 
pipline. 
```bash
#!/bin/bash
zip --password encCredential credenital.pyz credential.py
source scripts/${IDS_JOB_NAME}
```
When you generate a new credentials file use following command 
to encode it on your local system and checkin the new .pyz file. 
Updating to a new credential file  

```bash
zip --password <password> -e credential.pyz credential.py
```
Verify that the the credential.py is in .gitignore. 
