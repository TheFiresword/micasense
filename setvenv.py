import platform
import subprocess
import argparse

def create_and_activate_conda_env(env_file, env_name, exiftool_version):
    # param env_file::  yaml config file attached to this directory
    # param env_name:: the conda environment name (micasense by default)
    # param exiftool_version:: Version of the package exiftool to use
    exiftool_zip, exiftool_dir = "Image-"+exiftool_version+".tar.gz", "Image-"+exiftool_version
    conda_create_cmd = f"conda env create -f {env_file}"
    current_os = platform.system().lower()
    print("Your OS name is ", current_os)
    if 'windows' in current_os:
        # For windows computer
        conda_activate_cmd = f"conda activate {env_name}"
        subprocess.run(conda_create_cmd, shell=True)
        subprocess.run(f"call {conda_activate_cmd}", shell=True)
        print("Please manually download exiftool package here : https://exiftool.org/ and follow the instructions")
    elif 'linux' in current_os :
        # For Linux computer
        try:
            subprocess.run("wget https://exiftool.org/"+exiftool_zip, check=True, shell=True)
            print("Download completed successfully.")
            subprocess.run("tar -xvzf "+exiftool_zip)
            subprocess.run("cd "+ exiftool_dir + " && perl Makefile.PL && make test && sudo make install")
            subprocess.run("sudo apt install libzbar0", shell=True)
            conda_activate_cmd = f"source activate {env_name}"        
            subprocess.run(conda_create_cmd, shell=True)
            subprocess.run(conda_activate_cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    else:
        raise EnvironmentError("Unsupported operating system")

    print(f"Conda environment '{env_name}' created and activated successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This program installs the requirements needed to run the scripts")
    parser.add_argument("-f", "--envfile", type=str, help="the name of the yaml file", default="micasense_conda_env.yml")
    parser.add_argument("-p", "--exiftoolversion", type=str, help="The version of the exiftool package to be installed",
                        default="12.89")
    args = parser.parse_args()
    env_file = args.envfile 
    conda_env = "micasense"
    exiftool_version = args.exiftoolversion
    create_and_activate_conda_env(env_file, conda_env, exiftool_version)
