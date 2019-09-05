###
# 
# 1. Download the manifest xml from the url passed in ([Example Manifest](https://raw.githubusercontent.com/couchbase/sync_gateway/master/manifest/default.xml))
# 1. Get the contents of every repo listed in the manifest at the revision (SHA or branch) specified by the 'revision' attribute, or the master branch if no revision is specified
# 1. Add the contents of every repo into the target archive file (zip or .tar.gz)
# 1. Add the manifest itself into the target archive file
###
import os
import sys, getopt
import subprocess
import xml.etree.ElementTree as ET
import shutil
from git import Repo
import zipfile
import time
import wget

# get working path/folder
# 
def get_cwd():
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    print("Directory name is : " + foldername)
    return dirpath


# create a new place holdrer folder for all the repos
#
def create_folder(path, foldername):
    new_path = path + '/' + foldername
    try:
        shutil.rmtree(new_path) # delete the folder tree if it's not empty
        os.mkdir(new_path)
    except OSError:
        print ("Creation of the directory failed: " + new_path)
    else:
        print ("Successfully created the directory: " + new_path)
    return new_path


# Download xml with giving url
def download_file(url):
    try:
        filename = wget.download(url)
    except:
        print(Exception)
    else:
        print ("download file location: " + filename)
        return filename


# Get root object from xml
def get_xml_root(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root


# Create dictionary with repo NAME as 'key' and FETCH as 'value'
def get_repo_dict(filename):
    root = get_xml_root(filename)
    remote_repo = {}   
    for fetch_tag in root.findall('remote'):
        repo_name = fetch_tag.get('name') 
        try:
            repo_url = fetch_tag.get('fetch')
            #print(repo_name)
        except:
            print(Exception)        
        remote_repo[repo_name] = repo_url
    return remote_repo


# Create revision dictionary using REVISION as 'key' and REMOTE as 'value'
def get_revision_dict(filename):
    root = get_xml_root(filename)
    revision = {}
    for revision_tag in root.findall('project'):
        remote_name = revision_tag.get('remote')
        try:
            revi = revision_tag.get('revision')
        except:
            print(Exception)
            print("No revision tag exist")       
        revision[revi] = remote_name
    return revision


# Archive entire folder
def zip_folder(foldername, output_filename):
    # zip repo folder
    try:
        shutil.make_archive(output_filename, 'zip', foldername)
        print(output_filename)
        print(foldername)
    except:
        print(Exception)
        print("Failed to create zip file")
    else:
        print("Created zipped file: " + output_filename)
        return output_filename +'.zip'


# Get contents from Clonetarged repos with commit id
def clone_repos_commits(rr, rev, folder):
    for url, repof in zip(rr.values(), rr.keys()):
        # test it
        # print(folder)
        # temp = folder + '/' + repof
        # Repo.clone_from("https://github.com/glhome2/python-code/", temp)
        # test it
        for commit, remote in zip(rev.keys(), rev.values()):
            print(commit, remote)
            if not commit:
                try:
                    os.rmdir(folder + '/' + repof)
                    Repo.clone_from(url, folder + '/' + repof)
                except:
                    print(Exception)
                    print("Failed to access or downalod the git repo master branch" )
            else:
                try:
                    os.rmdir(folder + '/' + repof)
                    Repo.clone_from(url, folder + '/' + repof)
                    Repo.clone(commit)
                except:
                    print(Exception)
                    print("Failed to access or downalod the git repo" )


# Attache manifext xml to archived file
def add_in_zip(file_attach, zipfile_path):
    try:
        m_zip = zipfile.ZipFile(zipfile_path,'a')
        m_zip.write(os.path.basename(file_attach))
        m_zip.close()
    except:
        print(Exception)

###
# manifest_url = "https://raw.githubusercontent.com/couchbase/sync_gateway/master/manifest/default.xml"
# target_zip = "repos_zip"
###

def main(argv):
    # user input argv from cmd
    if len(sys.argv) < 3:
        print("You failed to provide xml url and zip file name as input on the command line!")
        print("eg. code_couchbase.py xmlURL zipfileName ")
        sys.exit(1)  # abort because of error
    else:
        manifest_url = sys.argv[1]
        print(manifest_url)
        target_zip = sys.argv[2]
        print(target_zip)
        
        dirpath = get_cwd()
        new_folder = create_folder(dirpath, 'repos')

        xml_filename = download_file(manifest_url)

        # Get all contentents from the repo with listed commits
        remote_repo = get_repo_dict(xml_filename)
        revision = get_revision_dict(xml_filename)
        clone_repos_commits(remote_repo, remote_repo, new_folder)

        # Add local repos contents to zip file
        output_filename = zip_folder(new_folder, target_zip)

        # Add manifest to the target zip file
        add_in_zip(xml_filename, output_filename)


if __name__ == "__main__":
    main(sys.argv[1:])



