import os
from hdf5filewriter import HDF5FileWriter

def main():
    config = {
        "record_name":"20250530045629",
        "record_dir":r"E:\project\DobotRX\临时的不上传\test1209\collect_data\20250530045629", # 表示任务所在的绝对路径
        "save_dir":r"E:\project\DobotRX\临时的不上传\test1209\train_data",
        "annotation_file":r"E:\project\DobotRX\临时的不上传\test1209\collect_data\20250530045629\annotationcfg\config.json",
        "name":"test",
        "jpeg_quality":50, # 图像转换质量，范围 1~100
        "img_width": 640, # 压缩后的图片像素宽，默认 640
        "img_height": 480, # 压缩后的图片像素高 默认 480
        "camera_names": [ # 录制回合的几个图片目录，有几个就填几个，但一定是这4个中的某几个
                "top_left", 
                "top_right",
                "wrist_left",
                "wrist_right"],
        "crop_img":{ #表示图片裁剪的比例值,对应上面录制回合目录，每一个都是2维数组
                "top_left": [
                    [5 / 12, 12 / 12], # 表示“宽度从左边5/12开始裁剪，到右边12/12结束”
                    [1 / 4, 3 / 4]     # 表示“高度从上边的1/4开始裁剪，到下边3/4结束”
                ],
                "top_right": [[5 / 12, 12 / 12], [1 / 4, 3 / 4]],
                "wrist_left": [[1 / 4, 3/4], [2 / 8, 8 / 8]],
                "wrist_right": [[0 / 3, 1.0], [0 / 8, 8 / 8]]
        }
    }

    hdf5 = HDF5FileWriter()
    hdf5.process_dataset(config)

if __name__ == '__main__':
    main()