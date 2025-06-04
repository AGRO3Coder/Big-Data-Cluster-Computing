from hdfs import InsecureClient
# HDFS伪分布式地址
HDFS_URL = "http://172.16.190.131:9870"  # 修改为你的HDFS集群地址
client = InsecureClient(HDFS_URL, user="root")  # HDFS用户