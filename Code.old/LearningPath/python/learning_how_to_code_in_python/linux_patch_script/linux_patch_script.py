"""_summary_

Raises:
    Exception: _description_

Returns:
    _type_: _description_
"""

import fcntl
import logging as lg
import os
import time
from datetime import datetime

import boto3
import pandas as pd
from botocore.exceptions import ClientError

lock_file_path = "/tmp/my_lock_file.lock"
# Try to create a lock file and acquire an exclusive lock
lock_file = open(lock_file_path, "w")
try:
    fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    # Another instance is running
    print("Another instance is already running")
    exit()


class Patching:
    def __init__(
        self,
        instanceId,
        accountId,
        rebootIfNeeded=False,
        patchOnly=False,
        rebootOnly=False,
    ) -> None:
        self.instanceId = instanceId
        self.accountId = accountId
        self.rebootIfNeeded = rebootIfNeeded
        self.patchOnly = patchOnly
        self.rebootOnly = rebootOnly
        self.showPatches = True
        self.patchStatus = "Not started"
        self.patchOutput = ""
        self.patchError = ""
        self.response = ""
        self.output = ""
        self.commandId = ""
        self.isStatus = ""
        self.isRebootReqOutput = ""
        self.lst = []
        self.rebootStatus = "Not Started"
        self.rebootOutput = ""
        self.rebootError = ""
        self.status = ""
        # setting up default session for aws account using aws profile name
        # Get the access to ssm and ec2
        try:
            boto3.setup_default_session(profile_name=accountId)
        except ClientError as e:
            print("Authentication Failed", e)
        self.ssm = boto3.client("ssm")
        self.ec2 = boto3.client("ec2")
        self.region = self.region_Instn()

    # Method for finding region of the instance
    def region_Instn(self):
        response = self.ec2.describe_instances(InstanceIds=[self.instanceId])
        instance = response["Reservations"][0]["Instances"][0]
        region = instance["Placement"]["AvailabilityZone"]
        return region

    # status of the instance
    def statusOfInstance(self):
        response = self.ec2.describe_instances(InstanceIds=[self.instanceId])
        status = response["Reservations"][0]["Instances"][0]["State"]["Name"]
        self.status = status

    # Method for patching of the instance
    def patchInstance(self):
        command = """
            #!/bin/bash
            #Check the type of system
            system=$(cat /etc/os-release | grep ^ID= | sed -e 's/ID=//' | tr -d '"')
            # Update the system based on the type
            echo $system
            if [ $system = "amzn" ]; then
                sudo yum update -y && sudo yum -y install kernel
            elif [ $system = "ubuntu" ]; then
                sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install linux-generic
            elif [ $system = "centos" ]; then
                sudo yum update -y && sudo yum -y install kernel
            elif [ $system = "redhat" ]; then
                sudo yum update -y && sudo yum -y install kernel
            elif [ $system = "debian" ]; then
                sudo apt-get update && sudo apt-get upgrade -y && sudo yum -y install kernel
            elif [ $system = "fedora" ]; then
                sudo dnf install yum
                sudo dnf update -y && sudo yum -y install kernel
            elif [ $system = "suse" ]; then
                sudo zypper update -y && sudo yum -y install kernel
            else
                echo "Unsupported system: $system"
                exit 1
            fi
            """
        self.response = self.getoutput(command)
        self.patchStatus = self.response["Status"]
        self.patchOutput = self.response["StandardOutputContent"]
        self.patchError = self.response["StandardErrorContent"]

    # output of the each command is invoked here
    def getoutput(self, command):
        response = self.ssm.send_command(
            InstanceIds=[self.instanceId],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": [command]},
        )
        commandid = response["Command"]["CommandId"]
        while True:
            response = self.ssm.get_command_invocation(
                CommandId=commandid, InstanceId=self.instanceId
            )
            if response["Status"] in ["Success", "Failed"]:
                break
            time.sleep(5)
        return response

    # checks weather a instance needs reboot or not
    def isRebootNeeded(self):
        command = """
            #!/bin/bash
            #Check the type of system
            if [ -n "$(which yum)" ]; then
                if ! rpm -q yum-utils; then
                    yum update -y
                    yum install -y yum-utils
                fi 
            fi
            system=$(cat /etc/os-release | grep ^ID= | sed -e 's/ID=//' | tr -d '"')
            # Update the system based on the type
            if [ $system = "amzn" ]; then
                sudo needs-restarting -r
                RESULT=$?
                echo ""
                if [ $RESULT -eq 1 ]; then
                    echo "reboot-required"
                else
                echo "No-action-required"
                fi
            elif [ $system = "ubuntu" ]; then
                if [ -f /var/run/reboot-required ]; then
                    echo "reboot-required"
                else
                    echo "No-action-required"
                fi
                
            elif [ $system = "centos" ]; then
                sudo needs-restarting -r
                RESULT=$?
                    echo ""
                if [ $RESULT -eq 1 ]; then
                    echo "reboot-required"
                else
                    echo "No-action-required"
                fi
            elif [ $system = "redhat" ]; then
                sudo needs-restarting -r
                RESULT=$?
                echo ""
                if [ $RESULT -eq 1 ]; then
                    echo "reboot-required"
                else
                    echo "No-action-required"
                fi
            elif [ $system = "debian" ]; then
                if [ -f /var/run/reboot-required ]; then
                    echo "reboot-required"
                else
                    echo "No-action-required"
                fi
            elif [ $system = "fedora" ]; then
                if [ -f /var/run/reboot-required ]; then
                    echo "reboot-required"
                else
                    echo"No-action-required"
                fi
            elif [ $system = "susu" ]; then
                if [ -f /var/run/reboot-required ]; then
                    echo "reboot-required"
                else
                    echo "No-action-required"
                fi
            else
                echo "Unsupported system: $system"
                exit 1
            fi
            """
        self.response = self.getoutput(command)
        self.isStatus = self.response["Status"]
        self.isRebootReqOutput = self.response["StandardOutputContent"]

    # commands for rebooting the instance
    def RebootInstance(self):
        self.rebootOutput = "Rebooting"
        command = "reboot"
        self.response = self.getoutput(command)
        self.rebootStatus = self.response["Status"]
        self.rebootOutput = self.response["StandardOutputContent"]
        self.rebootError = self.response["StandardErrorContent"]

    # The Status of each patch and reboot if done
    def StatusOfPatch(self):
        self.lst.append(self.instanceId)
        self.lst.append(self.region)
        self.lst.append(self.accountId)
        self.lst.append(self.patchStatus)
        self.lst.append("yes" if self.rebootIfNeeded else "no")
        rebootNeed = "yes" if "reboot-required" in self.isRebootReqOutput else "no"
        self.lst.append(rebootNeed)
        self.lst.append(self.rebootStatus)
        self.statusOfInstance()
        self.lst.append(self.status)
        return self.lst

    def rebootingInstance(self):
        try:
            self.ec2.reboot_instances(InstanceIds=[self.instanceId], DryRun=True)
        except ClientError as e:
            if "DryRunOperation" not in str(e):
                print("You don't have permission to reboot instances.")
                lg.error("You don't have permission to reboot instances.")
                raise

        try:
            response = self.ec2.reboot_instances(
                InstanceIds=[self.InstanceId], DryRun=False
            )
            print("Success", response)
        except ClientError as e:
            print("Error", e)


if __name__ == "__main__":

    # Reading input
    # 1st Line - List of instance-id and aws account profile name i.e. is set with access key and secret key in dev/cloud desktop
    # 2nd Line - Reboot the instance if required if yes press "y" if don't want reboot press "n"
    # 3rd Line - If only patching is required then  press "y"
    # 4th Line - If reboot only required press "y"
    # note : patchonly and rebootonly cannot be true at same time
    Instances = eval(input("Enter the list of instance id's and aws profile :"))
    if len(Instances) == 0:
        print("List cannot be empty")
    elif len(Instances[0]) < 2:
        print("Instance list should contain list of instance id and aws profile ")
        exit()
    rebootOptIn = input("Reboot if required Enter y/n : ")
    if rebootOptIn == "y":
        rebootOptIn = True
    elif rebootOptIn == "n":
        rebootOptIn = False
    else:
        print("Please Enter correct option")
        exit()
    patchOnly = input("patch only required Enter y/n :")
    if patchOnly == "y":
        patchOnly = True
    elif patchOnly == "n":
        patchOnly = False
    else:
        print("Please Enter correct option")
        exit()
    rebootOnly = input("reboot only required Enter y/n :")
    if rebootOnly == "y":
        rebootOnly = True
    elif rebootOnly == "n":
        rebootOnly = False
    else:
        print("Please Enter correct option")
        exit()
    if rebootOnly == True and patchOnly == True:
        raise Exception("RebootOnly and patchOnly cannot be used together")

    # Information of each instance is stored in the data list
    data = []
    headers = [
        "InstanceId",
        "Region",
        "AccountId",
        "PatchStatus",
        "RebootOptIn",
        "RebootNeeded",
        "RebootComplete",
        "Status",
    ]

    ts = datetime.now()

    timeStamp = str(ts.date()) + "_" + str(ts.time()) + "_patchScript"
    # logging
    lg.basicConfig(filename=timeStamp, level=lg.INFO)

    # For each Instance do
    for i in Instances:
        lg.info("Patching Instance Id -->" + i[0])
        print("Patching Instance Id -->", i[0])
        ins = Patching(i[0], i[1], rebootOptIn, patchOnly, rebootOnly)
        if ins.rebootOnly:
            ins.RebootInstance()
            if ins.rebootStatus == "Success":
                print("Rebooted successfully ", ins.rebootOutput)
                lg.info("Rebooted successfully " + ins.rebootOutput)
            else:
                print("Reboot failed due to :", ins.rebootOutput)
                lg.error("Reboot failed due to :" + ins.rebootOutput)
        else:
            ins.patchInstance()
            print(ins.patchStatus)
            if ins.patchStatus == "Success":
                print(ins.patchOutput)
                lg.info("patching " + ins.patchOutput)
                ins.isRebootNeeded()
                print(ins.isStatus + " " + ins.isRebootReqOutput)
                lg.info(ins.isStatus + " " + ins.isRebootReqOutput)
                if ins.rebootIfNeeded and "reboot-required" in ins.isRebootReqOutput:
                    ins.RebootInstance()
                    if ins.rebootStatus == "Success":
                        print("Rebooted successfully ", ins.rebootOutput)
                        lg.info("Rebooted successfully " + ins.rebootOutput)
                    else:
                        print("Reboot failed due to :", ins.rebootOutput)
                        lg.error("Reboot failed due to :" + ins.rebootOutput)
                else:
                    if "reboot-required" in ins.isRebootReqOutput:
                        print(
                            "Reboot is Required for this instance id ->", ins.instanceId
                        )
                        lg.critical(
                            "Reboot is Required for this instance id ->"
                            + ins.instanceId
                        )

            else:
                print("Patching failed due to :", ins.patchOutput)
                print("Error", ins.patchError)
                lg.error("Patching failed due to :" + ins.patchOutput)
                lg.error(ins.patchError)

        temp = ins.StatusOfPatch()
        data.append(temp)
    df = pd.DataFrame(data, columns=headers)
    print(df)
    lg.info(df)

# Release the lock and delete the lock file
fcntl.lockf(lock_file, fcntl.LOCK_UN)
lock_file.close()
os.unlink(lock_file_path)
