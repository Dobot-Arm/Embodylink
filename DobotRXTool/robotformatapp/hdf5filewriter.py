'''
hdf5的格式转换，将采集数据转换为hdf5格式
'''

import sys
import os
import glob
import pickle
import h5py  # h5py==3.11.0
import cv2     # opencv_contrib_python==4.1.2.30
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
import json

class HDF5FileWriter:
    def __init(self):
        pass

    """
    # config的数据结构是这样的
    config = {
        "record_name":"yyyyMMddHHmmss", # 录制回合的文件夹名称，也就是那个年月日的文件名称，比如: 20250529112345
        "record_dir":"", #录制回合所在的绝对路径，也就是那个年月日的文件夹绝对路径，比如: /home/test/taskname/collect_data/20250529112345
        "annotation_file":"", #该记录回合的标注信息配置文件，只有已标注的才有
        "save_dir":"", #转换为hdf5文件后，该训练数据保存的绝对路径，比如 /home/test/savepath/train_data
        "name":"", # 表示生成hdf5文件的保存时的前缀名
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
    """

    def create_directory(self,path: str) -> bool:
        """Create directory if it doesn't exist."""
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
            return True
        return False


    # 对单个的回合数据进行处理并保存
    def process_dataset(self,config) -> None:
        """Process a single dataset episode."""
        episode = config["record_name"]
        episode_dir = config["record_dir"]
        save_dir = config["save_dir"]
        prefixName = config["name"]
        # Load data with selected cameras
        qpos, action, image_files, joint_count = self.load_dataset(config, episode_dir)

        # Load annotation info to json string
        anno_json = self.load_annotation(config)

        # Prepare data dictionary
        data_dict = {
            '/observations/qpos': qpos, # 这个其实就是集合了所有pkl文件中的obs参数，形如[[...],[...],[...]...] 这样的结构
            '/action': action, # 这个其实就是集合了所有pkl文件中的action参数，形如[[...],[...],[...]...] 这样的结构
            '/annotation': anno_json, #标注信息，为json字符串
        }

        for cam in config["camera_names"]:
            data_dict[f'/observations/images/{cam}'] = image_files[cam] #图片文件的绝对路径数组

        # Save HDF5
        self.create_directory(save_dir)
        file_full_path = os.path.join(save_dir, f"{prefixName}-{episode}.hdf5")
        self.save_hdf5(file_full_path,data_dict,config,joint_count,compress=True)

    # ******************************************************************************************************
    def save_hdf5(self,
            output_file: str,
            data_dict: Dict[str, np.ndarray],
            config,
            joint_count: int = 28,
            compress: bool = True
    ) -> None:
        """
        Save dataset to HDF5 file with optional JPEG compression.
        Args:
            output_path: Output file path without extension
            data: Dictionary containing dataset arrays
            camera_names: List of camera names to include
            compress: Enable JPEG compression
            jpeg_quality: JPEG quality (1-100)
        """
        camera_names = config["camera_names"]
        jpeg_quality: int = config["jpeg_quality"]
        crop_img = config["crop_img"]
        img_width: int = config["img_width"]
        img_height: int = config["img_height"]

        T = len(data_dict['/observations/qpos'])
        with h5py.File(output_file, "w") as hf:
            hf.attrs['sim'] = False
            hf.attrs['compress'] = compress

            # Create datasets
            obs = hf.create_group('observations')
            img_group = obs.create_group('images')

            qpos_ds = obs.create_dataset('qpos', (T, joint_count), dtype='float64')
            action_ds = hf.create_dataset('action', (T, joint_count), dtype='float64')
            anno_ds = hf.create_dataset('annotation', (1, ), dtype=h5py.string_dtype(encoding='utf-8'))

            qpos_ds[...] = data_dict['/observations/qpos'] #写入数据
            action_ds[...] = data_dict['/action'] #写入数据
            anno_ds[...] = data_dict['/annotation'] #写入数据

            # Handle image compression
            compress_len = []
            max_size = 0
            for cam in camera_names:
                image_path_all = data_dict[f'/observations/images/{cam}']
                cam_crop_dict = crop_img[cam]
                if compress:
                    # JPEG compression
                    compressed = []
                    for image_file in image_path_all:
                        frame = self.load_camera_images_from_file(cam_crop_dict, image_file, img_width, img_height)
                        if frame is None:
                            continue
                        _, buf = cv2.imencode('.jpg',frame,[int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
                        compressed.append(buf)
                        compress_len.append(len(buf))
                        max_size = max(max_size, len(buf))
                    # Pad compressed data
                    padded = np.zeros((T, max_size), dtype='uint8')
                    for i, buf in enumerate(compressed):
                        padded[i, :len(buf)] = buf.reshape(-1)
                    img_group.create_dataset(cam, data=padded)
                else:
                    frames = []
                    for image_file in image_path_all:
                        img = self.load_camera_images_from_file(cam_crop_dict, image_file, img_width, img_height)
                        if img is None:
                            continue
                        frames.append(img)
                    img_group.create_dataset(cam, data=frames)

            # Store compression metadata
            if compress:
                hf.create_dataset('compress_len', data=np.array(compress_len))

    # ******************************************************************************************************
    # 读取并返回图片数据
    def image_read(self, img_path):
        try:
            # ASCII路径，使用更快的方法
            img_path.encode('ascii') #当它包含非ascii字符时会抛异常
            return cv2.imread(img_path)
        except:
            # 非ASCII路径，使用兼容方法
            img_data = np.fromfile(img_path, dtype=np.uint8)
            return cv2.imdecode(img_data, cv2.IMREAD_COLOR) # cv2.imread第二个参数默认是cv2.IMREAD_COLOR

    # ******************************************************************************************************
    def load_camera_images_from_file(self, cam_crop_dict, img_path, img_width, img_height):
        img = self.image_read(img_path)
        if img is None:
            return None
        v_crop, h_crop = cam_crop_dict
        h, w = img.shape[:2]
        y1, y2 = int(h * v_crop[0]), int(h * v_crop[1])
        x1, x2 = int(w * h_crop[0]), int(w * h_crop[1])
        img = img[y1:y2, x1:x2]

        # Resize to target resolution
        img = cv2.resize(img, (img_width, img_height))
        return img
    
    # ******************************************************************************************************
    def load_dataset(self,
            config,
            episode_dir: str,
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, List[str]], bool]:
        """
        Load robot dataset with selected cameras.
        Args:
            episode_dir: Path to dataset record directory
            camera_names: List of cameras to include
        Returns:
            qpos: Robot joint positions (T, 28)
            action: Robot actions (T, 28)
            images: Dictionary of camera images {camera_name: (T, H, W, 3)}
            is_sim: Simulation flag (always False for real data)
        """
        # 获取当前记录回合下observation目录中的所有pkl文件的绝对路径
        pose_files = sorted(glob.glob(f"{episode_dir}/observation/*.pkl"),key=lambda x: int(Path(x).stem))
        # 分别获取当前记录回合下的top_left、top_right、wrist_left、wrist_right目录中的所有jpg文件的绝对路径
        image_files = {}
        for cam in config["camera_names"]:
            cam_files = sorted(glob.glob(f"{episode_dir}/{cam}/*.jpg"),key=lambda x: int(Path(x).stem))
            image_files[cam] = cam_files

        print(f"load_dataset-->before filter, the source pkl file count={len(pose_files)}", flush=True)
        for k,v in image_files.items():
            print(f"load_dataset-->before filter, the source {k} image file count={len(v)}", flush=True)

        # 对齐pkl文件和jpg文件，保证他们的数量和文件名称是一致的
        pose_files, image_files = self.validate_data_files(pose_files, image_files)

        print(f"load_dataset-->after filter, the source pkl file count={len(pose_files)}", flush=True)
        for k,v in image_files.items():
            print(f"load_dataset-->after filter, the source {k} image file count={len(v)}", flush=True)

        # 加载每一个pkl文件，分别获取文件中的obs和action
        qpos, actions, joint_count = [], [], 0
        for pose_file in pose_files:
            with open(pose_file, "rb") as f:
                data = pickle.load(f)
                joint_count = max(joint_count, len(data['obs']), len(data['action']))
                qpos.append(data['obs'])
                actions.append(data['action'])
        # Load and preprocess images
        print(f"load_dataset-->open and parse pkl file success count={len(qpos)}, joint_count={joint_count}", flush=True)
        return np.array(qpos), np.array(actions), image_files, joint_count
    

    # ******************************************************************************************************
    # 此函数的目的就是为了对齐数据，让pose_files中的文件名与image_files中的文件名数量和名称一致
    def validate_data_files(self,
            pose_files: List[str],
            image_files: Dict[str, List[str]]
    ) -> Tuple[List[str], Dict[str, List[str]]]:
        """
        Ensure data consistency by removing incomplete frames.
        Args:
            pose_files: List of pose pickle files
            image_files: Dictionary of {camera_name: list of image files}
        Returns:
            Validated pose_files and image_files
        """
        # Create timestamp set from pose files
        valid_ts = {Path(f).stem for f in pose_files}

        # Filter image files
        filtered_images = {}
        for cam, files in image_files.items():
            filtered = [f for f in files if Path(f).stem in valid_ts]
            filtered_images[cam] = filtered

        # Filter pose files based on image availability
        image_ts = {Path(f).stem for files in filtered_images.values() for f in files}
        filtered_poses = [f for f in pose_files if Path(f).stem in image_ts]

        return filtered_poses, filtered_images
    
    #************************************************************************************************************
    #此函数加载标注信息
    def load_annotation(self, config):
        file_path = config["annotation_file"]
        annos_js = '[]'
        try:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    annos_js = json.dumps(data["steps"], ensure_ascii=False)
        except Exception as e:
            print(f"解析标注文件出现错误: {e}", flush=True)
        return annos_js