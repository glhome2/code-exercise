## Task: save contents of git repositories listed in XML manifest into a zip archive

The task is to write a script that does the following:

1. Download the manifest xml from the url passed in ([Example Manifest](https://raw.githubusercontent.com/couchbase/sync_gateway/master/manifest/default.xml))
1. Get the contents of every repo listed in the manifest at the revision (SHA or branch) specified by the 'revision' attribute, or the master branch if no revision is specified
1. Add the contents of every repo into the target archive file (zip or .tar.gz)
1. Add the manifest itself into the target archive file

## Error handling

* If the script can't get the revision listed for a given repo, it should grab the master branch and print a warning
* If the whole repo doesn't exist or is inaccessible, it should skip that repo and print a warning

## Usage example

```
./backup-manifest url target-zipfile
```

## Expected output

A .tar.gz or .zip file that contains:

1. The manifest xml
1. The contents of every repo listed in the manifest, on the commit or branch specified in the manifest

## Language and environment

- Any common Unix scripting language (python, bash, perl) is acceptable
- Assume this is being run from an automation environment such as Jenkins - ie, no user interaction, no GUI, but it should produce useful debugging and tracing output

## Packaging and dependencies

- You can assume this will run on either OSX or Linux.  No windows support needed.  If it only works on a single flavor of Unix, please mention that somewhere in the docs.
- You can assume that "standard" utilities will be installed (`git`, `python`, `bash`, etc)
- You can use any 3rd party library or existing code (but if you find this exact tool, then we might have to come up with a new coding challenge!)
- If you use any non-standard tools or libraries then you should add some documentation on how to install them

## Objective

- The point of this challenge is to verify that you are able to write well structured code that performs its function well, and is easy to understand and maintain.
- Peformance needs to be "acceptable", but there is no real reason to go crazy trying to optimize it.  You can assume this runs as a 24 hour batch job and it's fairly irrelevant whether it takes 30 seconds vs 3 minutes.
- This should not be a long-term assignment. Estimated time for completion is one to three hours.

## Submission

- Please post your submission on GitHub and reply with the source URL in email.
- Your submission should at a minimum include the script file(s) as well as a brief README describing the functionality of the script and any requirements it has. Remember, the goal is to see whether you can write utilities that would be easy for others to use and maintain.