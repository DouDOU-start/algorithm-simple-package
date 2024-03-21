import time
import SimpleITK as sitk
import numpy as np
import pymysql

# LabelOrganDict = {

#     1000: "Marker",

#     2000: "AllTumor",
#     2001: "TumorStart",
#     2999: "TumorEnd",

#     3000: "Liver",
#     4000: "Spleen",

#     5000: "Kidney",
#     5001: "LeftKidney",
#     5002: "RightKidney",
    
#     6000: "Gallbladder",
#     7000: "Esophagus",
#     8000: "Stomach",
#     9000: "Aorta",
#     10000: "InferiorVenaCava",
#     11000: "PortalVeinAndSplenicVein",
#     12000: "Pancreas",

#     13000:"AdrenalGland",
#     13001: "LeftAdrenalGland",
#     13002: "RightAdrenalGland",

#     14000: "HepaticVessel",
#     15000: "Bone",
#     16000: "Skin",

#     17000: "Lung",
#     17001: "LeftLung",
#     17002: "RightLung",
#     18000: "Airway",
# }

db_config = {
    "host": "10.8.6.34",
    "port": 3366,
    "user": "root",
    "password": "hanglok8888",
    "database": "algorithm_scheduling_dev",
    "charset": "utf8mb4"
}

connection = pymysql.connect(**db_config)

print("database connection successful")

try:
    with connection.cursor() as cursor:
        sql = "SELECT label, name FROM organ"
        cursor.execute(sql)

        organ_data = [{"label": row[0], "name": row[1]} for row in cursor.fetchall()]
finally:
    connection.close()

LabelOrganDict = {item["label"]: item["name"] for item in organ_data}

OrganLabelDict = {value:key for key,value in LabelOrganDict.items()}

def merge_img(model): 

    start_time = time.time()

    length = len(model["args"]["label"])
    merge_array = None
    merge_img = None

    for index, item in enumerate(model["args"]["label"]):
        # 遍历字典中的文件名和标签值
        for filename, attributes in item.items():
            algo_img = sitk.ReadImage(f'/tmp/{model["task_id"]}/{filename}')
            algo_array = sitk.GetArrayFromImage(algo_img)

            # 初始化merge_array
            if merge_array is None:
                merge_array = np.zeros(algo_array.shape)

            print(f"index{index + 1}: {filename}")
            
            # 判断属性是否为字典
            if isinstance(attributes, dict):
                # 融合label
                for label_value, organ in attributes.items():
                    merge_array[algo_array==int(label_value)]=OrganLabelDict[organ]
            else:
                # 如果不是字典，直接打印值
                print(f"Error Value: {attributes}")
        
        if index == length - 1:            
            # 从融合array中获取新的img数据
            merge_img = sitk.GetImageFromArray(merge_array)
            # 复制原图信息
            merge_img.CopyInformation(algo_img)

    # 保存到本地
    sitk.WriteImage(merge_img, f'/tmp/{model["task_id"]}-out/{model["outputFile"]["output"]}', True)

    print(f'unique: {np.unique(merge_array)}')

    print(f"fusion Execution time: {time.time() - start_time} seconds")