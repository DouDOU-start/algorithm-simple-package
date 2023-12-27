import time
import SimpleITK as sitk
import numpy as np
from minio_util import init_client, load_stk_image

LabelOrganDict = {

    1000: "Marker",

    2000: "AllTumor",
    2001: "TumorStart",
    2999: "TumorEnd",

    3000: "Liver",
    4000: "Spleen",

    5000: "Kidney",
    5001: "LeftKidney",
    5002: "RightKidney",
    
    6000: "Gallbladder",
    7000: "Esophagus",
    8000: "Stomach",
    9000: "Aorta",
    10000: "InferiorVenaCava",
    11000: "PortalVeinAndSplenicVein",
    12000: "Pancreas",

    13000:"AdrenalGland",
    13001: "LeftAdrenalGland",
    13002: "RightAdrenalGland",

    14000: "HepaticVessel",
    15000: "Bone",
    16000: "Skin",

    17000: "Lung",
    17001: "LeftLung",
    17002: "RightLung",
    18000: "Airway",
}

OrganLabelDict = {value:key for key,value in LabelOrganDict.items()}

def merge_img(model): 

    start_time = time.time()

    length = len(model["input"])
    merge_array = None
    merge_img = None

    # 遍历 algo
    for index, algo in enumerate(model["input"]):
        client = init_client()
        algo_img = load_stk_image(client, "algorithm", algo["object_name"])
        # algo_img = readImageFromMinio(algo["object_name"])
        algo_array = sitk.GetArrayFromImage(algo_img)

        # 初始化merge_array
        if merge_array is None:
            merge_array = np.zeros(algo_array.shape)
        
        # 融合label
        for label in algo["label"]:
            for organ, label_value in label.items():
                merge_array[algo_array==label_value]=OrganLabelDict[organ]

        if index == length - 1:
            # 从融合array中获取新的img数据
            merge_img = sitk.GetImageFromArray(merge_array)
            # 复制原图信息
            merge_img.CopyInformation(algo_img)

    # 保存到本地
    sitk.WriteImage(merge_img, f'/tmp/{model["task_id"]}-out/{model["output"]}', True)

    print(f'unique: {np.unique(merge_array)}')

    print(f"fusion Execution time: {time.time() - start_time} seconds")