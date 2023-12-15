import SimpleITK as sitk
import numpy as np

from minio_client import upload_file

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

def merge_img(task_id): 

    # 获取原图 img
    lungsegmentation_img = sitk.ReadImage(f'/tmp/{task_id}/lungsegmentation.nii.gz')
    airwaysegmentation_img = sitk.ReadImage(f'/tmp/{task_id}/airwaysegmentation.nii.gz')
    bodyinference_img = sitk.ReadImage(f'/tmp/{task_id}/body_inference.nii.gz')

    # 获取 array
    lungsegmentation_array = sitk.GetArrayFromImage(lungsegmentation_img)
    airwaysegmentation_array = sitk.GetArrayFromImage(airwaysegmentation_img)
    bodyinference_array = sitk.GetArrayFromImage(bodyinference_img)

    # 开始融合
    merge_array = np.zeros_like(lungsegmentation_array)
    merge_array[bodyinference_array==3]=OrganLabelDict["Skin"]
    merge_array[bodyinference_array==2]=OrganLabelDict["Bone"]
    merge_array[lungsegmentation_array==True]=OrganLabelDict["Lung"]
    merge_array[airwaysegmentation_array==1]=OrganLabelDict["Airway"]
    merge_img = sitk.GetImageFromArray(merge_array)

    # 复制原图信息
    merge_img.CopyInformation(lungsegmentation_img)

    # 保存到本地
    sitk.WriteImage(merge_img, f'/tmp/{task_id}/merge.mha')

    # 上传到 minio
    upload_file(f'output/{task_id}/result/merge.mha', f'/tmp/{task_id}/merge.mha')


