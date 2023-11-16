# External trigger

There are a number of types of External triggers I plan to support:

 - googleDriveRawClass
 - googleDriveNewFileWatchClass

I will add others in future.

Each job will have the following fields:
 - Accept external triggers True/False
 - Trigger passwords generated when trigger setup
   - There are TWO passwords. one in the URI and one not.
 - External Trigger Type - String of the type (above)
 - External Trigger Variables - Dictionary of trigger variables

Notificaitons are received at https://host:port/triggerapi/${URISTRING}
URISTRING can be anything depending on the trigger type. It is not used to select the type

There will be a system passwoerd "DOCKJOB_EXTERNAL_TRIGGER_SYS_PASSWORD".
When a trigger is received the engine asks each type 'is this yours'. The type will take the message and if it is return
the Job GUID that the trigger corrosponds to. The system checks that that Job is accepting external triggers and the type
matches. 

It is NOT possible that the message belongs to a type and should be ignored. This is because the same message may be acceptable 
by google raw and google drive, but the job itself knows which one it needs.

If the type matches then the External trigger provides a stdin for the process and the process is kicked off.
Failures here are logged to stdout.

Raw trigger types will just forward the message as json to the stdin of the process.
Others like the Google Drive New File Watch will do further processing to find the actual file that was added to the drive
and pass data bout it to the process.




To build this I must:
Implement a drive change list watcher - https://developers.google.com/drive/api/reference/rest/v3/changes/list
I can on a call watch changes from a drive

Implement a notification handler that starts a process with the input being the drive notification

Add secrets into the mix for google credentials

