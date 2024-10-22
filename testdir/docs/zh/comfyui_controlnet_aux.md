# ComfyUI 的辅助预处理器插件
轻松使用的ComfyUI节点集来制作[ControlNet](https://github.com/lllyasviel/ControlNet/)提示图像，用于实现“anime风格、街头抗议、赛博朋克城市”，一名拥有粉色头发和金色眼睛的女子（正看着观众）高举着带有"ComfyUI ControlNet Aux"字样在霓虹粉红色背景上的标语。

![CNAuxBanner](./examples/CNAuxBanner.jpg)

代码从https://github.com/lllyasviel/ControlNet/tree/main/annotator中的相应文件夹复制粘贴而来，并连接至[🤗 Hub](https://huggingface.co/lllyasviel/Annotators)。

所有版权和信用都归属于https://github.com/lllyasviel。

# 更新
请前往[更新页面](./UPDATES.md)查看最新动态

# 安装
## 使用ComfyUI Manager（推荐）：
安装[ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)，按照其中介绍的步骤来安装此仓库。

## 替代方案：
如果你在Linux系统上运行或者Windows非管理员账户上运行，需要确保 `/ComfyUI/custom_nodes` 和 `comfyui_controlnet_aux` 有写权限。

现在有一个**install.bat**脚本可以运行以实现便携式安装。否则，默认会进行系统安装并假设你遵循了ConfyUI的自定义安装步骤。

如果你无法运行 **install.bat**（例如你是Linux用户）。打开CMD/Shell，按照以下步骤操作：
1. 导航到你的 `/ComfyUI/custom_nodes/` 文件夹
2. 运行 `git clone https://github.com/Fannovel16/comfyui_controlnet_aux/`
3. 导航至你所在的 `comfyui_controlnet_aux` 文件夹：
   - 对于便携式/虚拟环境：
     - 运行 `path/to/ComfUI/python_embeded/python.exe -s -m pip install -r requirements.txt`
   - 使用系统Python
     - 运行 `pip install -r requirements.txt`
4. 启动ComfyUI

# 节点
请注意，此仓库仅支持制作提示图像（例如：粘木人、边缘检测等）的预处理器。
除了Inpaint之外的所有预处理器都集成到了`AIO Aux Preprocessor`节点中。该节点允许你快速获取预处理器功能，但其自身的阈值参数无法设置。你需要直接使用节点来调整这些阈值。

# 节点（Comfy 菜单中的章节相当于类别）
## 线提取器
| 前处理节点           | sd-webui-controlnet/other  |          ControlNet/T2I-Adapter          |
|-----------------------------|---------------------------|-------------------------------------------|
| 二值线条                | binary                    | control_scribble                              |
| Canny 边缘               | canny                     | control_v11p_sd15_canny <br> control_canny <br> t2iadapter_canny |
| HED 软边缘线条         | hed                       | control_v11p_sd15_softedge <br> control_hed |
| 标准线稿               | standard_lineart          | control_v11p_sd15_lineart                       |
| 真实线稿               | lineart (或 `lineart_coarse` 如果启用了 `coarse`)  | control_v11p_sd15_lineart                         |
| 动画线稿               | lineart_anime             | control_v11p_sd15s2_lineart_anime                 |
| 静态漫画线稿           | lineart_anime_denoise     | control_v11p_sd15s2_lineart_anime                 |
| M-LSD 线条               | mlsd                      | control_v11p_sd15_mlsd <br> control_mlsd         |
| PiDiNet 软边缘线条       | pidinet                   | control_v11p_sd15_softedge <br> control_scribble  |
| 笔刷线稿               | scribble                  | control_v11p_sd15_screble <br> control_scribble    |
| 笔刷XDoG线稿           | scribble_xdog             | control_v11p_sd15_screble <br> control_scribble   |
| 虚假笔刷线稿           | scribble_hed              | control_v11p_sd15_screble <br> control_scribble    |
| TEED 软边缘线条         | teed                      | [controlnet-sd-xl-1.0-softedge-dexined](https://huggingface.co/SargeZT/controlnet-sd-xl-1.0-softedge-dexined/blob/main/controlnet-sd-xl-1.0-softedge-dexined.safetensors) <br> control_v11p_sd15_softedge (理论上)
| 笔刷PiDiNet线稿         | scribble_pidinet          | control_v11p_sd15_screble <br> control_scribble       |
| 任何线条线稿           |                           | mistoLine_fp16.safetensors <br> mistoLine_rank256 <br> control_v11p_sd15s2_lineart_anime <br> control_v11p_sd15_lineart |

（注：某些节点在 Comfy 菜单中可能没有对应的选项，具体需要根据实际情况选择合适的替代方案。）

## 正常和深度估计器
| 预处理器节点           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| MiDaS 深度图           | (正常) 深度            | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| LeReS 深度图           | depth_leres               | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| Zoe 深度图             | depth_zoe                 | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| MiDaS 正常图           | normal_map                | control_normal                            |
| BAE 正常图           | normal_bae                | control_v11p_sd15_normalbae               |
| MeshGraphormer 手部增强器 (HandRefinder [https://github.com/wenquanlu/HandRefiner](https://github.com/wenquanlu/HandRefiner))  | depth_hand_refiner | [control_sd15_inpaint_depth_hand_fp16](https://huggingface.co/hr16/ControlNet-HandRefiner-pruned/blob/main/control_sd15_inpaint_depth_hand_fp16.safetensors) |
| Depth Anything           |  depth_anything           | [Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/blob/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors) |
| Zoe 深度 Anything <br> (基本上是Zoe，但编码器被替换为DepthAnything)       | depth_anything | [Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/blob/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors) |
| Normal DSINE              |                           | control_normal/control_v11p_sd15_normalbae |
| Metric3D 深度            |                           | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| Metric3D 正常            |                           | control_v11p_sd15_normalbae |
| Depth Anything V2         |                           | [Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/blob/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors) |

（注：ControlNet 替换的文本未提供，因此保持不变。）

## 面部和姿态估测器
| 前处理节点           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| DWPose 估测器                 | dw_openpose_full          | control_v11p_sd15_openpose <br> control_openpose <br> t2iadapter_openpose |
| OpenPose 估测器               | openpose (检测身体) <br> openpose_hand (检测身体和手) <br> openpose_faceonly (检测面部) <br> openpose_full (检测手、身体和面部)    | control_v11p_sd15_openpose <br> control_openpose <br> t2iadapter_openpose |
| MediaPipe 面部网格         | mediapipe_face            | controlnet_sd21_laion_face_v2             | 
| 动物估测器                 | animal_openpose           | [control_sd15_animal_openpose_fp16](https://huggingface.co/huchenlei/animal_openpose/blob/main/control_sd15_animal_openpose_fp16.pth) |

## 光学流估测器
| 前处理节点           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| Unimatch 光学流       |                           | [DragNUWA](https://github.com/ProjectNUWA/DragNUWA) |

### 如何获取 OpenPose 格式 JSON？
#### 用户侧
此工作流程将图像保存到 ComfyUI 输出文件夹（与输出图像在同一位置）。如果尚未找到 `Save Pose Keypoints` 节点，请更新该扩展。
![](./examples/example_save_kps.png)

#### 开发侧
从 DWPose 和 OpenPose 使用 `app.nodeOutputs` 在 UI 或 `/history` API 端点，可以获取与每帧 IMAGE 批次相对应的一组 [OpenPose 格式 JSON](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/02_output.md#json-output-format)。AnimalPose 的 JSON 输出格式类似于 OpenPose JSON：
```
[
    {
        "version": "ap10k",
        "animals": [
            [[x1, y1, 1], [x2, y2, 1],..., [x17, y17, 1]],
            [[x1, y1, 1], [x2, y2, 1],..., [x17, y17, 1]],
            ...
        ],
        "canvas_height": 512,
        "canvas_width": 768
    },
    ...
]
```

### 延伸开发者的扩展：
```js
const poseNodes = app.graph._nodes.filter(node => ["OpenposePreprocessor", "DWPreprocessor", "AnimalPosePreprocessor"].includes(node.type))
for (const poseNode of poseNodes) {
    const openposeResults = JSON.parse(app.nodeOutputs[poseNode.id].openpose_json[0])
    console.log(openposeResults) //一个数组，包含每一帧的Openpose JSON
}
```

### API用户的API：
Javascript
```js
import fetch from "node-fetch" //记得在 "package.json" 中添加 "type": "module"
async function main() {
    const promptId = '792c1905-ecfe-41f4-8114-83e6a4a09a9f' //懒得去 POST /queue
    let history = await fetch(`http://127.0.0.1:8188/history/${promptId}`).then(re => re.json())
    history = history[promptId]
    const nodeOutputs = Object.values(history.outputs).filter(output => output.openpose_json)
    for (const nodeOutput of nodeOutputs) {
        const openposeResults = JSON.parse(nodeOutput.openpose_json[0])
        console.log(openposeResults) //一个数组，包含每一帧的Openpose JSON
    }
}
main()
```

Python
```py
import json, urllib.request

server_address = "127.0.0.1:8188"
prompt_id = '' #懒得去 POST /queue

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

history = get_history(prompt_id)[prompt_id]
for o in history['outputs']:
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'openpose_json' in node_output:
            print(json.loads(node_output['openpose_json'][0])) #一个列表，包含每一帧的Openpose JSON
```

### 图像分割：
| 预处理器节点           | sd-webui-controlnet/other  |
|-----------------------------|---------------------------|
| OneFormer ADE20K 分割器   | oneformer_ade20k       |
| OneFormer COCO 分割器     | oneformer_coco         |
| UniFormer 分割器         | segmentation           |

| 预处理器节点           | T2I-Adapter  |
|-----------------------------|---------------------------|
| OneFormer ADE20K 分割器   | ControlNet/T2I-Adapter   |
| OneFormer COCO 分割器     | ControlNet/T2I-Adapter   |
| UniFormer 分割器         | ControlNet/T2I-Adapter  |

（注意：上述表格中的 "ControlNet" 应替换为正确的节点名称。）

## T2IAdapter-only
| 预处理器节点           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| 颜色配色表               | color                     | t2iadapter_color                          |
| 内容打乱               | shuffle                   | t2iadapter_style                          |

## 重着色
| 预处理器节点           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| 图像亮度               | recolor_luminance         | [ioclab_sd15_recolor](https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/ioclab_sd15_recolor.safetensors) <br> [sai_xl_recolor_256lora](https://huggingface.co/lllyasviel/sd_control_collection/resolve/main/sai_xl_recolor_256lora.safetensors) <br> [bdsqlsz_controlllite_xl_recolor_luminance](https://huggingface.co/bdsqlsz/qinglong_controlnet-lllite/resolve/main/bdsqlsz_controlllite_xl_recolor_luminance.safetensors) |
| 图像强度               | recolor_intensity         | 我不确定，可能是上述节点。 |

# 示例
> 一图胜千言

![](./examples/ExecuteAll1.jpg)
![](./examples/ExecuteAll2.jpg)

# 测试工作流
https://github.com/Fannovel16/comfyui_controlnet_aux/blob/main/examples/ExecuteAll.png
输入图片: https://github.com/Fannovel16/comfyui_controlnet_aux/blob/main/examples/comfyui-controlnet-aux-logo.png

# 问答:
## 为什么安装了这个仓库后，有些节点不见了？

该仓库采用了新的机制，会跳过无法导入的自定义节点。如果您遇到这种情况，请在 [Issues 标签页](https://github.com/Fannovel16/comfyui_controlnet_aux/issues) 中创建一个新 issue，并附上命令行中的日志。

## DWPose/AnimalPose 只使用 CPU 所以运行非常慢，如何让它使用 GPU？
有两条路线可以提高 DWPose 的速度：一是使用 TorchScript 检查点（.torchscript.pt）进行加速；二是使用 ONNXRuntime (.onnx) 进行加速。TorchScript 方式比 ONNXRuntime 稍稍慢一点，但不需要额外的库，并且依然远快于 CPU。
  
1. 使用 TorchScript 检查点:
   - 将模型导出为 .torchscript.pt 格式，在 ComfyUI 中启用 TorchScript 模型。
2. 使用 ONNXRuntime:
   - 安装 ONNXRuntime 库 (pip install onnxruntime)
   - 使用 ONNXRuntime 进行推理时，可以将 ONNX 转换后的模型加载到 ComfyUI 中。

### TorchScript
根据下图设置 `bbox_detector` 和 `pose_estimator`。如果输入的图像质量理想，您可以尝试使用其他以 `.torchscript.pt` 结尾的 bbox detector 来减少 bbox 检测时间。
![](./examples/example_torchscript.png)
### ONNXRuntime
如果您已成功安装 onnxruntime 并且使用的 checkpoint 以 `.onnx` 结尾，则它将替代默认的 cv2 后端，利用 GPU。请注意，如果使用的是 NVIDIA 卡片，除非您自行编译了 onnxruntime，否则目前这一方法仅能在 CUDA 11.8 (ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z) 上运行。

1. 知道您的 onnxruntime 构建：
* * NVidia CUDA 11.x 或更低版本/AMD GPU: `onnxruntime-gpu`
* * NVidia CUDA 12.x: `onnxruntime-gpu --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/`
* * DirectML: `onnxruntime-directml`
* * OpenVINO: `onnxruntime-openvino`

请注意，如果您是第一次使用 ComfyUI，请在进行下一步操作前先测试一下它是否可以在您的设备上运行。

2. 将其添加到 `requirements.txt` 文件中。

3. 运行安装脚本 `install.bat` 或 pip 命令，具体请参阅 安装指南。

It looks like you've provided a list of pre-trained models and their corresponding links for various tasks, including face detection, hand pose estimation, facial recognition, segmentation, depth estimation, edge detection, diffusion modeling, motion flow estimation, and more. These models are often used in image and video processing pipelines.

Here's a breakdown of what each model is used for:

- **hand_pose_model.pth**: Hand pose estimation
- **facenet.pth**: Facial recognition (assuming this might be referring to FaceNet)
- **table5_pidinet.pth**: PID inference (possibly related to hand gesture detection or other control-related tasks, not sure based on the name alone)
- **mobile_sam.pt**: Mobile version of Semantic segmentation with Attention (SAM) model
- **upernet_global_small.pth**: Universal Perceptual Units Small for general-purpose image processing
- **ZoeD_M12_N.pt**: Zoe Depth Estimation Network for depth estimation
- **qinglong_controlnet-lllite/7_model.pth**: ControlNet model likely used with Qilingong framework (not sure of the exact details, but it's associated with a control-based model)
- **depth_anything_vitl14.pth**, **depth_anything_vitb14.pth**, **depth_anything_vits14.pth**: Depth estimation models using different architectures
- **diffusion_edge.pt**: Diffusion model for edge detection or denoising (indoor, urban, natural settings)
- **gmflow-scale2-regrefine6-mixdata.pth**, **gmflow-scale2-mixdata.pth**, **gmflow-scale1-mixdata.pth**: Flow and motion estimation models

These models can be particularly useful in various applications such as robotics, autonomous vehicles, interactive AI systems, and more. The availability of these pre-trained models through Hugging Face allows for easier integration into existing projects.

If you need further details on any specific model or task, feel free to ask!

### TorchScript
根据这张图设置 `bbox_detector` 和 `pose_estimator`。如果你的输入图片质量很好，可以尝试使用其他带有 `.torchscript.pt` 结尾的 bbox 检测器来减少 bbox 检测的时间。
![](./examples/example_torchscript.png)
### ONNXRuntime
如果已成功安装 onnxruntime，并且所使用的 checkpoint 结束为 `.onnx`，它将替换默认的 cv2 后端以利用 GPU。请注意，如果你使用的是 NVIDIA 显卡，除非你自己编译 onnxruntime，否则当前方法仅能在 CUDA 11.8（ComfyUI_windows_portable_nvidia_cu118_or_cpu.7z）上运行。

1. 知道你的 onnxruntime 构建：
* * NVIDIA CUDA 11.x 或更低版本/AMD GPU：`onnxruntime-gpu`
* * NVIDIA CUDA 12.x：`onnxruntime-gpu --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/`
* * DirectML：`onnxruntime-directml`
* * OpenVINO：`onnxruntime-openvino`

请注意，如果你是第一次使用 ComfyUI，请在继续下一步之前先测试一下它是否能在你的设备上运行。

2. 将其添加到 `requirements.txt` 文件中。

3. 运行安装 bat 脚本或 pip 命令，如安装说明所示。
![](./examples/example_onnx.png)

感谢你们的支持。我从没想到星星图谱会是线性的呢。