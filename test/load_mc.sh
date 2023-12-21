#!/bin/bash

mc_client="$1"

# 选取第一个非环回，非docker网卡地址作为本机地址的公共变量
INNER_IP=""
for real_ip in `ip address |grep 'inet ' | awk '{print $2}' |awk -F '/'  '{print $1}'`;
do
	if [[ $real_ip != "127.0"* && $real_ip != "172.17"* && $real_ip != "" ]]
	then
		INNER_IP=${real_ip}
		break
	fi
done

if [ "$mc_client" = "vpn" ]; then
    ./mc alias set vpn http://10.8.0.17:9000 afK2BE5BSWvayIw546b2 ZRITpJds2V3lQyDb3T3t3GyA383G7npr32p9zk9x
elif [ "$mc_client" = "local" ]; then
    ./mc alias set local http://$INNER_IP:9000 afK2BE5BSWvayIw546b2 ZRITpJds2V3lQyDb3T3t3GyA383G7npr32p9zk9x
else
    echo "Error: The mc_client parameters are only vpn or local!"
    exit 1
fi