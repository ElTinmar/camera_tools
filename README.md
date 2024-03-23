# camera_tools

handle various camera

```
pip install git+https://github.com/ElTinmar/camera_tools.git@main
```

# Ximea

Install xiAPI

```
CONDA_BASE=`conda info --base`
cd "${CONDA_BASE}/envs/camera_tools/lib"
PYTHON_VERSION=`ls |grep ^python`

printf "\nDownloading and extracting Ximea API ---------------------------\n"
cd $HOME
wget https://www.ximea.com/downloads/recent/XIMEA_Linux_SP.tgz
tar xzf XIMEA_Linux_SP.tgz
rm XIMEA_Linux_SP.tgz

printf "\nCompile ---------------------------\n"
cd package
./install -pcie

printf "\nCopy python API to site-packages ---------------------------\n"
cp -r api/Python/v3/ximea "${CONDA_BASE}/envs/camera_tools/lib/${PYTHON_VERSION}/site-packages/"

printf "\ncleanup ---------------------------\n"
cd $HOME
rm -rf package
```
