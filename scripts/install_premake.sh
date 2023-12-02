yum install -y wget unzip
mkdir /tmp/premake
wget https://github.com/premake/premake-core/releases/download/v5.0.0-beta2/premake-5.0.0-beta2-linux.tar.gz
tar -xzvf premake-5.0.0-beta2-linux.tar.gz -C /tmp/premake
export PATH=$PATH:/tmp/premake
ls -al /tmp/premake
ls -al .
