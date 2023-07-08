#! /bin/bash
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

CUR_SCRIPT_FOLDER=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCENARIO_HOMEDIR=$( cd -- "${CUR_SCRIPT_FOLDER}/.." &> /dev/null && pwd )

source "${SCENARIO_HOMEDIR}/_bash/utilities.sh"
# DEBUG=true

# Check if python3 is installed
checkPython3() {
    local exists=0
    if command -v python3 &>/dev/null; then
        # Get the version number
        python_version=$(python3 -V 2>&1)

        # Extract the major version number
        major_version=$(echo "$python_version" | awk -F'[ .]' '{print $2}')

        # Check if the major version is 3
        if [ "$major_version" -eq 3 ]; then
            exists=1
        fi
    fi

    echo ${exists}
}


python3Exists=$(checkPython3)
if [[ $python3Exists -eq 0 ]]; then
    echo "Python3 is not installed. Please install python3 and try again."
    errExit 10
fi

# Check if pip3 is installed
if not command -v pip3 &>/dev/null; then
    echo "pip3 is not installed. Please install pip3 and try again."
    errExit 20
fi

# Install the required python packages
pythonPkgReqFile="${SCENARIO_HOMEDIR}/python-scenarios/_python/requirements.txt"
if [[ -f "${pythonPkgReqFile}" ]]; then
    pip3 install -r "${SCENARIO_HOMEDIR}/python-scenarios/_python/requirements.txt"  
fi