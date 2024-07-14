import platform
import subprocess
import argparse
import os

def create_and_activate_conda_env(env_file, env_name, exiftool_version):
    # param env_file::  yaml config file attached to this directory
    # param env_name:: the conda environment name (micasense by default)
    # param exiftool_version:: Version of the package exiftool to use
    exiftool_zip, exiftool_dir = "Image-ExifTool-"+exiftool_version+".tar.gz", "Image-ExifTool-"+exiftool_version
    current_os = platform.system().lower()
    print("Your OS name is ", current_os)
    if 'windows' in current_os:
        # For windows computer
        try:
            subprocess.run(f"conda env create -f {env_file}", shell=True)
            print(f"Conda environment '{env_name}' created successfully!\nU can now activate your micasense \
                  environment by executing conda activate micasense")
            print("Please also manually download exiftool package here : https://exiftool.org/ and follow the instructions")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    elif 'linux' in current_os :
        # For Linux computer
        anaconda_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        try:
            # Install conda if necessary
            result = subprocess.run("conda --version", shell=True, text=True, capture_output=True)
            if result.returncode != 0:
                subprocess.run("mkdir -p ~/miniconda3 && wget "+anaconda_url +" -O ~/miniconda3/miniconda.sh", shell=True)
                subprocess.run("bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && rm -rf ~/miniconda3/miniconda.sh",shell=True)
                subprocess.run("~/miniconda3/bin/conda init bash && ~/miniconda3/bin/conda init zsh", shell=True)
                input("Veuillez redémarrer le terminal puis exécuter  à nouveau ce script...")
                os.system("exit")
            if not os.path.isdir(exiftool_dir):
                if not os.path.exists(exiftool_zip):
                    subprocess.run("wget https://exiftool.org/"+exiftool_zip, check=True, shell=True)
                    print("Download completed successfully.")
                subprocess.run("tar -xvzf "+exiftool_zip, shell=True)
            
            subprocess.run("cd "+ exiftool_dir + " && perl Makefile.PL && make test && \
                           sudo make install && cd ..", shell=True)
            # check if libzbar0 is already installed
            if subprocess.run(["dpkg", "-l", "libzbar0"], stdout=subprocess.PIPE).returncode != 0:
                subprocess.run("sudo apt install libzbar0", shell=True)
            
            subprocess.run(f"conda env create -f {env_file}", shell=True)

            print(f"Conda environment '{env_name}' created successfully!\nU can now activate your micasense
                  environment by executing conda activate micasense")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    else:
        raise EnvironmentError("Unsupported operating system")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program installs the requirements needed to run the scripts and set up a conda environment")
    parser.add_argument("-f", "--envfile", type=str, help="the name of the yaml file", default="micasense_conda_env.yml")
    parser.add_argument("-p", "--exiftoolversion", type=str, help="The version of the exiftool package to be installed",
                        default="12.89")
    args = parser.parse_args()
    env_file = args.envfile 
    conda_env = "micasense"
    exiftool_version = args.exiftoolversion
    create_and_activate_conda_env(env_file, conda_env, exiftool_version)
