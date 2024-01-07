# YOU DON'T NEED THIS, JUST SEE (THIS VIDEO FOR EASY SYNCING)[https://www.youtube.com/watch?v=8RYprLafFzw] or you can use an easy to use software (WinSCP)[https://winscp.net/eng/download.php]

Your files on your XNAT server is somewhere like this:

/root/xnat-docker-compose/xnat-data/archiv/PROJECT-NAME





# Aim of previous code (NO need to read it :)


In this instruction, you will download (sync) segmentations from your server into your windows folder, when any segmentations are generated. In XNAT, when segmentations are avaialble for a case, it will sotre them in a folder within each session-folder named, ASSESSORS. This code will look for existance of this subfolder, and sync it with your local. You should run this code on your XNAT terminal, after logging into your linux (you can do this using remote-ssh on visual studio).

# Step 1: Set Up Network Sharing
First, ensure that the folder E:\XNAT_BACK on your Windows machine is shared on the network and is accessible from your Linux server. This setup is done from your Windows machine. Once shared, you can mount this network share on your Linux server using smbclient or mount -t cifs.

### Step 1_A: Share the Folder in Windows
Locate the Folder: Go to E:\XNAT_BACK on your Windows machine.

Open Folder Properties: Right-click on the folder and select Properties.

Navigate to the Sharing Tab: In the Properties dialog, go to the Sharing tab.

Advanced Sharing: Click on Advanced Sharing….

Enable Sharing: Check Share this folder. This will enable sharing for the selected folder.

Assign a Share Name: In the Share name field, you can keep the default name or give a new name to the shared folder. This name will be used to access the folder from the network.

Permissions: Click on Permissions. For basic sharing, you can allow Read access for Everyone. If you need to write to the folder from your Linux server, you should also allow Change or Full Control. Be cautious with these settings to avoid unauthorized access.

Apply and OK: Click Apply and then OK to close the dialog boxes.

### Step 1_B: Note Down Network Details
Get the IP Address: On your Windows machine, open Command Prompt and type ipconfig. Note down the IPv4 Address.

Check the Workgroup: Go to Control Panel → System and Security → System and check the Workgroup. It’s important that your Linux server is on the same workgroup if you’re using an older version of Windows or SMB protocol.


# Step 2 - Solutuion A: Mount the Windows Share on Linux
On your Linux server, you’ll access this shared folder either by mounting it or using smbclient. To mount it, you’ll need the cifs-utils package installed on your Linux server. You can install it with:

    sudo apt-get install cifs-utils  # For Debian/Ubuntu
    # or
    sudo yum install cifs-utils    # For CentOS/RHEL
    # or
    sudo dnf install cifs-utils    # For Fedora

Before mounting, you should create the Mount point on your server. Open your terminal in linux server and run this:

    sudo mkdir -p /mnt/windows_share

This command creates a new directory at /mnt/windows_share that will serve as the mount point for the shared folder. The -p flag ensures that any necessary parent directories are also created.

Then, to mount the shared folder, you can use:

    sudo mount -t cifs //WINDOWS_IP_ADDRESS/XNAT_BACK /mnt/windows_share -o user=WINDOWS_USERNAME

Replace WINDOWS_IP_ADDRESS with the IP address you noted earlier and WINDOWS_USERNAME with your Windows username (IN your command terminal on windows write the prompt whoami). You will be prompted to enter your Windows user's password.

Security Note: Using shared folders over a network can expose your data. Ensure your network is secure, and consider using VPNs or other secure methods when accessing sensitive data. Also, be cautious with permissions, especially if your network includes public or untrusted devices.
Security Note: For security reasons, it's better to use a credentials file instead of typing your password directly into the terminal. You can create a credentials file with your username and password and reference it in the mount command with credentials=/path/to/your/credentials_file.


Verify the Mount:
Once the command completes, you can verify that the share has been mounted successfully by running:
    ls /mnt/windows_share

# Step 2 - Solutuion A: Mount the Windows Share on Linux

Step 1: Install smbclient
First, ensure that smbclient is installed on your Linux server. You can install it using your distribution's package manager. For Debian/Ubuntu, use:

    sudo apt-get update 
    sudo apt-get install smbclient #for Debian/Ubunto
    #or
    sudo yum install smbclient  # CentOS/RHEL 7 and below
    # or
    sudo dnf install smbclient  # Fedora and CentOS/RHEL 8+

Step 2: Connect to the Windows Share
To connect to the Windows share using smbclient, use the following command:

    smbclient //WINDOWS-IP-ADDRESS/XNAT_BACK -U WINDOWS-USERNAME

Replace WINDOWS-IP-ADDRESS with the IP address of your Windows machine and XNAT_BACK with the name of the shared folder. -U WINDOWS-USERNAME specifies the username; you will be prompted for the password.

Step 3: Transfer Files
Once connected, you can use smbclient commands to transfer files. Here are some basic commands:


Once connected, you can use smbclient commands to transfer files. Here are some basic commands:

ls: List files in the current directory of the share.
cd [directory]: Change directory.
get [filename]: Download a file from the share to your current local directory.
put [filename]: Upload a file from your local directory to the share.
mget *: Download all files from the current directory of the share.
mput *: Upload all files from your local directory to the share.
exit or quit: Close the smbclient session.
For example, to download all contents from the ASSESSORS directory:

    cd ASSESSORS
    lcd /path/to/local/directory
    mget *

Replace /path/to/local/directory with the path where you want to download the files on your Linux server.


Step 4: Check the smbclient connection with windows before running your script
Open server linux terminal and run:

    smbclient -L //WINDOWS-IP-ADdress -U LABTOB-DOMAIN\\LABTOB-USERNAME #replace WINDOWS-IP-ADdress; LABTOB-DOMAIN; and LABTOB-USERNAME wiht your own values using two command line prompts of ipconfig and whoami on windows terminal

This command lists all shares available on the Windows machine. Look for XNAT_BACK in the list. If prompted for a password, enter the password for the WINDOWS-USERNAME user.



# Step 3: Write the Sync Script - for solution 1
Now, write a bash script on your Linux server to perform the synchronization:

    #!/bin/bash

    # Source directory on the Linux server
    src_dir="/root/xnat-docker-compose/xnat-data/archive/PanCanAID/arc001"

    #you can fill in project name by using this code instead of the src_dir
    # Ask for the project name
    #read -p "Enter the project name: " project_name
    #src_dir="/root/xnat-docker-compose/xnat-data/archive/$project_name/arc001"


        #First install rsync using the following command
        sudo apt install rsync

        # Destination directory (mounted Windows share)
        dest_dir="/mnt/windows_share"

        # Iterate through each subfolder in the source directory
        for folder in "$src_dir"/*; do
            # Check if the 'ASSESSORS' subfolder exists
            if [ -d "$folder/ASSESSORS" ]; then
                # Extract the folder name
                folder_name=$(basename "$folder")

                # Create the corresponding directory in the destination
                mkdir -p "$dest_dir/$folder_name"

                # Sync the 'ASSESSORS' subfolder
                rsync -av --progress "$folder/ASSESSORS/" "$dest_dir/$folder_name/"
            fi
        done

        echo "Sync complete."

Save this script on your Linux server, make it executable with chmod +x script_name.sh, and run it with ./script_name.sh.


# Step 3: Write the Sync Script - for solution 2
Run this code for syncing cases for a example porject 'PanCanAID' if it contains folder ASSESSORS; replace the WINDOW-IP-ADDRESS wiht your windows ip address; WINDOW-USERNAME with your windows username

    #!/bin/bash

    # Source directory on the Linux server
    src_dir="/root/xnat-docker-compose/xnat-data/archive/PanCanAID/arc001"

    # Windows share details
    win_share="//WINDOW-IP-ADDRESS/XNAT_BACK"
    win_user="WINDOW-USERNAME" # replace with your Windows username

    # Ask for the Windows password
    read -sp "Enter password for $win_user: " win_pass
    echo

    # Iterate through each subfolder in the source directory
    for folder in "$src_dir"/*; do
        # Check if the 'ASSESSORS' subfolder exists
        if [ -d "$folder/ASSESSORS" ]; then
            # Extract the folder name
            folder_name=$(basename "$folder")

            # Connect to the Windows share using smbclient and transfer files
            smbclient $win_share -U $win_user%$win_pass -c "cd $folder_name; lcd $folder/ASSESSORS; prompt; recurse; mput *"
        fi
    done

    echo "Sync complete."

# Final step, for reuse
Save the script to a file on your Linux server (e.g., sync_assessors.sh).

Make the script executable:

    chmod +x sync_assessors.sh

Run the script:

    ./sync_assessors.sh


# Important Notes:
This script assumes you've successfully mounted the Windows share on your Linux server.

Ensure you have rsync installed on your Linux server.

The user executing the script needs to have read permissions on the source directories and write permissions on the mounted Windows share.

Test the script with a small amount of data first to ensure it works as expected.

The use of plain text passwords as shown here is not secure for production environments. Consider using a credentials file or other secure methods for authentication.

Regularly back up your data to prevent accidental loss during synchronization.

The script prompts for the Windows password when run. This is a basic form of security, but be aware that typing passwords in the terminal can be insecure in some environments.

The smbclient command in the script connects to the Windows share, changes to the corresponding directory, sets the local directory to the ASSESSORS subfolder, and then uses mput * to upload all files in that directory.

The prompt and recurse commands within the smbclient command disable interactive prompts and ensure recursive uploading of directories, respectively.

Ensure that the necessary directory structure exists on the Windows share, as smbclient does not create directories recursively.

This script does not perform two-way synchronization; it only uploads files from Linux to Windows. If files on the Windows side are updated, those changes will not be reflected back on the Linux server.

Ensure smbclient is installed on your Linux server (sudo apt-get install smbclient for Ubuntu/Debian systems).
Test this script with a small data set first to ensure it works as expected in your environment.