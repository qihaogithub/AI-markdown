# ComfyUI's ControlNet Auxiliary Preprocessors
Plug-and-play [ComfyUI](https://github.com/comfyanonymous/ComfyUI) node sets for making [ControlNet](https://github.com/lllyasviel/ControlNet/) hint images

"anime style, a protest in the street, cyberpunk city, a woman with pink hair and golden eyes (looking at the viewer) is holding a sign with the text "ComfyUI ControlNet Aux" in bold, neon pink" on Flux.1 Dev

![](./examples/CNAuxBanner.jpg)

The code is copy-pasted from the respective folders in https://github.com/lllyasviel/ControlNet/tree/main/annotator and connected to [the 🤗 Hub](https://huggingface.co/lllyasviel/Annotators).

All credit & copyright goes to https://github.com/lllyasviel.

# Updates
Go to [Update page](./UPDATES.md) to follow updates

# Installation:
## Using ComfyUI Manager (recommended):
Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) and do steps introduced there to install this repo.

## Alternative:
If you're running on Linux, or non-admin account on windows you'll want to ensure `/ComfyUI/custom_nodes` and `comfyui_controlnet_aux` has write permissions.

There is now a **install.bat** you can run to install to portable if detected. Otherwise it will default to system and assume you followed ConfyUI's manual installation steps. 

If you can't run **install.bat** (e.g. you are a Linux user). Open the CMD/Shell and do the following:
  - Navigate to your `/ComfyUI/custom_nodes/` folder
  - Run `git clone https://github.com/Fannovel16/comfyui_controlnet_aux/`
  - Navigate to your `comfyui_controlnet_aux` folder
    - Portable/venv:
       - Run `path/to/ComfUI/python_embeded/python.exe -s -m pip install -r requirements.txt`
	- With system python
	   - Run `pip install -r requirements.txt`
  - Start ComfyUI

# Nodes
Please note that this repo only supports preprocessors making hint images (e.g. stickman, canny edge, etc).
All preprocessors except Inpaint are intergrated into `AIO Aux Preprocessor` node. 
This node allow you to quickly get the preprocessor but a preprocessor's own threshold parameters won't be able to set.
You need to use its node directly to set thresholds.

# Nodes (sections are categories in Comfy menu)
## Line Extractors
| Preprocessor Node           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| Binary Lines                | binary                    | control_scribble                          |
| Canny Edge                  | canny                     | control_v11p_sd15_canny <br> control_canny <br> t2iadapter_canny |
| HED Soft-Edge Lines         | hed                       | control_v11p_sd15_softedge <br> control_hed |
| Standard Lineart            | standard_lineart          | control_v11p_sd15_lineart                 |
| Realistic Lineart           | lineart (or `lineart_coarse` if `coarse` is enabled) | control_v11p_sd15_lineart |
| Anime Lineart               | lineart_anime             | control_v11p_sd15s2_lineart_anime         |
| Manga Lineart               | lineart_anime_denoise     | control_v11p_sd15s2_lineart_anime         |
| M-LSD Lines                 | mlsd                      | control_v11p_sd15_mlsd <br> control_mlsd  |
| PiDiNet Soft-Edge Lines     | pidinet                   | control_v11p_sd15_softedge <br> control_scribble |
| Scribble Lines              | scribble                  | control_v11p_sd15_scribble <br> control_scribble |
| Scribble XDoG Lines         | scribble_xdog             | control_v11p_sd15_scribble <br> control_scribble |
| Fake Scribble Lines         | scribble_hed              | control_v11p_sd15_scribble <br> control_scribble |
| TEED Soft-Edge Lines        | teed                      | [controlnet-sd-xl-1.0-softedge-dexined](https://huggingface.co/SargeZT/controlnet-sd-xl-1.0-softedge-dexined/blob/main/controlnet-sd-xl-1.0-softedge-dexined.safetensors) <br> control_v11p_sd15_softedge (Theoretically)
| Scribble PiDiNet Lines      | scribble_pidinet          | control_v11p_sd15_scribble <br> control_scribble |
| AnyLine Lineart             |                           | mistoLine_fp16.safetensors <br> mistoLine_rank256 <br> control_v11p_sd15s2_lineart_anime <br> control_v11p_sd15_lineart |

## Normal and Depth Estimators
| Preprocessor Node           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| MiDaS Depth Map           | (normal) depth            | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| LeReS Depth Map           | depth_leres               | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| Zoe Depth Map             | depth_zoe                 | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| MiDaS Normal Map          | normal_map                | control_normal                            |
| BAE Normal Map            | normal_bae                | control_v11p_sd15_normalbae               |
| MeshGraphormer Hand Refiner ([HandRefinder](https://github.com/wenquanlu/HandRefiner))  | depth_hand_refiner | [control_sd15_inpaint_depth_hand_fp16](https://huggingface.co/hr16/ControlNet-HandRefiner-pruned/blob/main/control_sd15_inpaint_depth_hand_fp16.safetensors) |
| Depth Anything            |  depth_anything           | [Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/blob/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors) |
| Zoe Depth Anything <br> (Basically Zoe but the encoder is replaced with DepthAnything)       | depth_anything | [Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/blob/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors) |
| Normal DSINE              |                           | control_normal/control_v11p_sd15_normalbae |
| Metric3D Depth            |                           | control_v11f1p_sd15_depth <br> control_depth <br> t2iadapter_depth |
| Metric3D Normal           |                           | control_v11p_sd15_normalbae |
| Depth Anything V2         |                           | [Depth-Anything](https://huggingface.co/spaces/LiheYoung/Depth-Anything/blob/main/checkpoints_controlnet/diffusion_pytorch_model.safetensors) |

## Faces and Poses Estimators
| Preprocessor Node           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| DWPose Estimator                 | dw_openpose_full          | control_v11p_sd15_openpose <br> control_openpose <br> t2iadapter_openpose |
| OpenPose Estimator               | openpose (detect_body) <br> openpose_hand (detect_body + detect_hand) <br> openpose_faceonly (detect_face) <br> openpose_full (detect_hand + detect_body + detect_face)    | control_v11p_sd15_openpose <br> control_openpose <br> t2iadapter_openpose |
| MediaPipe Face Mesh         | mediapipe_face            | controlnet_sd21_laion_face_v2             | 
| Animal Estimator                 | animal_openpose           | [control_sd15_animal_openpose_fp16](https://huggingface.co/huchenlei/animal_openpose/blob/main/control_sd15_animal_openpose_fp16.pth) |

## Optical Flow Estimators
| Preprocessor Node           | sd-webui-controlnet/other |          ControlNet/T2I-Adapter           |
|-----------------------------|---------------------------|-------------------------------------------|
| Unimatch Optical Flow       |                           | [DragNUWA](https://github.com/ProjectNUWA/DragNUWA) |

### How to get OpenPose-format JSON?
#### User-side
This workflow will save images to ComfyUI's output folder (the same location as output images). If you haven't found `Save Pose Keypoints` node, update this extension
![](./examples/example_save_kps.png)

#### Dev-side
An array of [OpenPose-format JSON](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/02_output.md#json-output-format) corresponsding to each frame in an IMAGE batch can be gotten from DWPose and OpenPose using `app.nodeOutputs` on the UI or `/history` API endpoint. JSON output from AnimalPose uses a kinda similar format to OpenPose JSON:
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
