###
# 1. Download the manifest xml from the url passed in ([Example Manifest](https://raw.githubusercontent.com/couchbase/sync_gateway/master/manifest/default.xml))
# 1. Get the contents of every repo listed in the manifest at the revision (SHA or branch) specified by the 'revision' attribute, or the master branch if no revision is specified
# 1. Add the contents of every repo into the target archive file (zip or .tar.gz)
# 1. Add the manifest itself into the target archive file
###
import os
import wget
import subprocess
import xml.etree.ElementTree as ET
import shutil
from git import Repo
import zipfile
import time

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
        #os.rmdir(new_folder) # delete if the folder already exist
        #os.system("rm -rf new_folder")
        #subprocess.run(["rm", "-rf", new_folder])
        os.mkdir(new_path)
    except OSError:
        print ("Creation of the directory failed: " + new_path)
    else:
        print ("Successfully created the directory: " + new_path)
    return new_path


# manifest url
#
def download_file(url):
    try:
        filename = wget.download(url)
    except:
        print(Exception)
    else:
        print ("download file location: " + filename)
        return filename


def get_xml_root(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root


# get xml root tree
#root = get_xml_root(xml_filename)

# create dictionary with repo name as key and url as value
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


# revision dictionary
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


def zip_folder(foldername):
    # zip repo folder
    timestr = time.strftime("%Y%m%d%H%M%S")
    output_filename = "ziped_repo_" + timestr
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


# clone repos with commit id
def clone_repos_commits(rr, rev, folder):
    for url, repof in zip(rr.values(), rr.keys()):
        # test it
        print(folder)
        temp = folder + '/' + repof
        Repo.clone_from("https://github.com/glhome/python/", temp)
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


def add_in_zip(file_attach, zipfile_path):
    try:
        m_zip = zipfile.ZipFile(zipfile_path,'a')
        m_zip.write(os.path.basename(file_attach))
        m_zip.close()
    except:
        print(Exception)


# Prep local folder in current directory
dirpath = get_cwd()
new_folder = create_folder(dirpath, 'repos')

# Download manifest xml file
manifest_url = "https://raw.githubusercontent.com/couchbase/sync_gateway/master/manifest/default.xml"
xml_filename = download_file(manifest_url)

# Get all contentents from the repo with listed commits
remote_repo = get_repo_dict(xml_filename)
revision = get_revision_dict(xml_filename)
clone_repos_commits(remote_repo, remote_repo, new_folder)

# Add local repos contents to zip file
output_filename = zip_folder(new_folder)

# Add manifest to the target zip file
add_in_zip(xml_filename, output_filename)
