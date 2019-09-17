# using GIT-REPO

1. install "git-repo" "wget"and "zip/unzip" on client machine
2. run following bash script: with bash:
  
  #!/bin/bash
    xmlurl=$1
    zipfile=$2
    
    wget "$xmlurl"
    mkdir project
    cd project
    repo init -u $xmlurl
    repo sync
    # zip project
    cd ..
    cp *.xml project/
    zip -r $zipfile project
    


## Usage example

```
python code_couchbase.py url target-zipfile
```

## Expected output

A .zip file that contains:

1. The manifest xml
1. The contents of every repo listed in the manifest, on the commit or branch specified in the manifest

## Packaging and dependencies

this script is tested under:
Linux george-Swift-SF314-51 5.0.0-27-generic #28~18.04.1-Ubuntu SMP Thu Aug 22 03:00:32 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
