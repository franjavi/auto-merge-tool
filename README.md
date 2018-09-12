Synopsis
========
This tool helps to merge several repositories, and create the pull requests. Be aware that is a work in progress tool, 
and many things have to be done yet (UI, other way to introduce variables, clone repos if not existing)
For every repository we choose it does:
* Switches to the base branch and updates it
* Creates a temporal branch 
* Merges the merging branch into the temporal branch
* Pushes the new branch
* Creates the pull request
* Shows the pull request, and if has been any error, the error list


How to use the Tool:
====================
1. Fill the variables in **input_parameters.py**. The variables to fill are the ones in the **# ====== Manual editable variables ==============** section. This method of introducing data will be replaced in the future.
2. The bitbucket user should be passed via argument: *merge.py -user=yourUser* 
    * If the user is not set, the tool will do all the steps but not create the pull requests
3. The bitbucket password can be passed:
    * via argument: *merge.py -user=yourUser -password=yourPassword*
    * or, if not provided via argument, can be provided when the tool starts: *Provide Bitbucket password for the user:*   
4. Run the tool with: *merge.py \[possible arguments\]*
5. When the process is finished will report the results like:
```
Repositories output:
rtaoi-sender :  \['http://bitbucketServer.com/projects/TA/repos/repo-name/pull-requests/198'\]
export-views :  \['ERROR: Merging branch jSmith/testAutoMerge not found in export-views'\]
```

Requirements:
====================
* CLIENT
    * Python 3.5 or higher
* BITBUCKET SERVER    
    * Bitbucket API v1.0
    