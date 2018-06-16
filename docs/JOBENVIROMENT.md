# Job Enviroment

When a job is run in dockJob it has access to the enviroment variables of the machine it is being run on. These can be seen by creating a job with the command 'env' which will output the enviroment.
DockJob adds enviroment variables to give jobs access to more information. These variables and their meanings are documented on this page.

 | Variable | Meaning |
 |----------|---------|
 | DOCKJOB_JOB_GUID | GUID of the job being executed |
 | DOCKJOB_JOB_NAME | Name of the job being executed |
 | DOCKJOB_EXECUTION_GUID | GUID of the execution |
 | DOCKJOB_EXECUTION_NAME | Name of the execution |
 | DOCKJOB_EXECUTION_METHOD | The method used to start this job execution running. [Manual,Scheduled,StateChangeToSuccess,StateChangeToFail,StateChangeToUnknown] |
 | DOCKJOB_TRIGGERJOB_GUID | If the execution method is a State Change this will contain the GUID of triggering job |
 | DOCKJOB_TRIGGERJOB_NAME | If the execution method is a State Change this will contain the Name of triggering job |
 | DOCKJOB_TRIGGEREXECUTION_GUID | If the execution method is a State Change to Success or Fail then this variable will contain the GUID of the execution that triggered it |
 | DOCKJOB_TRIGGEREXECUTION_NAME | If the execution method is a State Change to Success or Fail then this variable will contain the Name of the execution that triggered it |
 | DOCKJOB_TRIGGEREXECUTION_STDOUT | If the execution method is a State Change to Success or Fail then this variable will contain the STDOUT of the execution that triggered it |


Note: When the state changes to unknown there is no trigger execution so in this case these variables will be blank.
