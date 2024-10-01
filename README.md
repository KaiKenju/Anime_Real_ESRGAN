# Anime_Real_ESRGAN
this project to enhance anime video to satifys
| Input | RealESRGAN |
|--|--|
| <img src="./assets/gif/Tesla_animation.gif" alt="c2" width="650"/> | <img src="./assets/gif/Tesla_animation_outx2_v1.gif" alt="g2" width="650"/> |
<!-- | <img src="./assets/gif/tougenaki.gif" alt="c2" width="650"/> | <img src="./assets/gif/tougenaki_outx2.gif" alt="g2" width="650"/> | -->



- Compare accelester
|           |video gốc | video enhance time | upscale |
|-----------|-------------------------------|--------|
|           | 2p46s                         | 4      |
| **GPU**   | 18s                           |--------|
|           | 1:44s                         | 2      |
|-----------|-------------------------------|--------|
|           | >2h                           | 2      |
| **CPU**   | 18s                           |--------|
|           | unknown                       | 4      |



# 🔧 Dependencies 
- Python >= 3.7 (Recommend to use Anaconda or Miniconda)
- PyTorch >= 1.7
- GPU (CPU very slow)
- FFmpeg environment
   1. You need to install ffmqpeg: [here](https://www.gyan.dev/ffmpeg/builds/)
   2. You can following the guide: [Guide](https://kdata.vn/tin-tuc/huong-dan-cach-cai-dat-ffmpeg-tren-windows-cuc-ky-don-gian)
   3. After that unzip file , the file `ffmpeg.exe` in the folder `bin`
   4. Open `System Properties/Environment Variable/System variables/PATH/path of ffmpeg.exe` in Window . 
   5. For example of path ffmpeg.exe: 
     ```
     C:\Users\ffmpeg-7.0.2-essentials_build\bin
     ```
# 🛠️ Installation
- Clone the project 
```
git clone https://github.com/KaiKenju/Anime_Real_ESRGAN.git
cd Anime_Real_ESRGAN
```
- Initial enviroment with Miniconda(Default python: 3.10) and requirements
```
conda create -n <env_name> python=3.10 
conda activate <env_name>
pip install -r requirements.txt
```
- Fix torchvision problem: you need to run the [fix_torchvision.py](fix_torchvision.py) to solve the problem of basicsr
```
python fix_torchvision.py
```
# ⚡ Quick Inference
- With anime video
```bash
python inference_anime_video.py -i <input_video> -n realesr-animevideov3 -s 2 --suffix outx2 
```

```console
Usage: python inference_anime_video.py -i input/video/Tesla_animation.mp4 -n realesr-animevideov3 -s 2 --suffix outx2 

  -h                   show this help
  -i --input           Input video . Default: inputs
  -o --output          Output folder. Default: results
  -n --model_name      Model name. Default: realesr-animevideov3
  -s, --outscale       The final upsampling scale of the image (1,2,3,4). Default: 4
  --suffix             Suffix of the restored image. Default: out
  -t, --tile           Tile size, 0 for no tile during testing. Default: 0
  --face_enhance       Whether to use GFPGAN to enhance face. Default: False
  --fp32               Use fp32 precision during inference. Default: fp16 (half precision).
  --ext                Image extension. Options: auto | jpg | png, auto means using the same extension as inputs. Default: auto
```

**Tips**

I suggest need to use GPU to run the model, 
