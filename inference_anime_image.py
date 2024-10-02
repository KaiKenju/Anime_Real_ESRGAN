import argparse
import cv2
import glob
import os
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

def main():
    """Inference demo for Real-ESRGAN."""
    parser = argparse.ArgumentParser(description='Real-ESRGAN Inference Script')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input image folder or specific image path')
    parser.add_argument(
        '-n',
        '--model_name',
        type=str,
        default='RealESRGAN_x4plus',
        help=('Model name: RealESRGAN_x4plus | RealESRNet_x4plus | RealESRGAN_x4plus_anime_6B | RealESRGAN_x2plus | '
              'realesr-animevideov3 | realesr-general-x4v3'))
    parser.add_argument('-o', '--output', type=str, required=True, help='Output folder to save images')
    parser.add_argument(
        '-dn',
        '--denoise_strength',
        type=float,
        default=0.5,
        help=('Denoise strength. 0 for weak denoising (retain noise), 1 for strong denoising. '
              'Only used for realesr-general-x4v3 model'))
    parser.add_argument('-s', '--outscale', type=float, default=4, help='Final image upscaling factor')
    parser.add_argument(
        '--model_path', type=str, default=None, help='[Optional] Path to the model. Usually, you don’t need to specify it')
    parser.add_argument('--suffix', type=str, default='out', help='Suffix of the restored images')
    parser.add_argument('-t', '--tile', type=int, default=0, help='Tile size, 0 for no tiling during testing')
    parser.add_argument('--tile_pad', type=int, default=10, help='Tile padding size')
    parser.add_argument('--pre_pad', type=int, default=0, help='Pre-padding size at each border')
    parser.add_argument('--face_enhance', action='store_true', help='Use GFPGAN to enhance face')
    parser.add_argument(
        '--fp32', action='store_true', help='Use fp32 precision during inference. Default: fp16 (half precision)')
    parser.add_argument(
        '--alpha_upsampler',
        type=str,
        default='realesrgan',
        help='The upsampler for the alpha channels. Options: realesrgan | bicubic')
    parser.add_argument(
        '--ext',
        type=str,
        default='auto',
        help='Image extension. Options: auto | jpg | png, auto means using the same extension as the input')
    parser.add_argument(
        '-g', '--gpu-id', type=int, default=None, help='GPU device to use (default=None), can be 0,1,2 for multi-GPU')

    args = parser.parse_args()

    # Determine model based on model name
    args.model_name = args.model_name.split('.')[0]
    if args.model_name == 'RealESRGAN_x4plus':  # RRDBNet x4 model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth']
    elif args.model_name == 'RealESRNet_x4plus':  # RRDBNet x4 model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth']
    elif args.model_name == 'RealESRGAN_x4plus_anime_6B':  # RRDBNet x4 model with 6 blocks
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth']
    elif args.model_name == 'RealESRGAN_x2plus':  # RRDBNet x2 model
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth']
    elif args.model_name == 'realesr-animevideov3':  # VGG-style x4 model (XS size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu')
        netscale = 4
        file_url = ['https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth']
    elif args.model_name == 'realesr-general-x4v3':  # VGG-style x4 model (S size)
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
        netscale = 4
        file_url = [
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth',
            'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth'
        ]

    # Determine model path
    if args.model_path is not None:
        model_path = args.model_path
    else:
        model_dir = 'weights'
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, args.model_name + '.pth')
        if not os.path.isfile(model_path):
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            for url in file_url:
                model_path = load_file_from_url(
                    url=url, model_dir=model_dir, progress=True, file_name=None)

    # Use dni to control denoising strength
    dni_weight = None
    if args.model_name == 'realesr-general-x4v3' and args.denoise_strength != 1:
        wdn_model_path = model_path.replace('realesr-general-x4v3', 'realesr-general-wdn-x4v3')
        model_path = [model_path, wdn_model_path]
        dni_weight = [args.denoise_strength, 1 - args.denoise_strength]

    # Initialize upsampler
    upsampler = RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=args.tile,
        tile_pad=args.tile_pad,
        pre_pad=args.pre_pad,
        half=not args.fp32,
        gpu_id=args.gpu_id)

    # If face enhancement is enabled with GFPGAN
    if args.face_enhance:
        try:
            from gfpgan import GFPGANer
            face_enhancer = GFPGANer(
                model_path='https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth',
                upscale=args.outscale,
                arch='clean',
                channel_multiplier=2,
                bg_upsampler=upsampler)
        except ImportError:
            print("Error: You need to install gfpgan for face enhancement feature.")
            return

    # Create output folder if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Determine input image paths
    if os.path.isfile(args.input):
        paths = [args.input]
    else:
        # Support common image formats
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff']
        paths = []
        for ext in image_extensions:
            paths.extend(glob.glob(os.path.join(args.input, ext)))
        paths = sorted(paths)

    if not paths:
        print(f"No images found in input folder: {args.input}")
        return

    # Process each image
    for idx, path in enumerate(paths):
        imgname, extension = os.path.splitext(os.path.basename(path))
        print(f'Processing {idx + 1}/{len(paths)}: {imgname}{extension}')

        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"Error: Unable to read image {path}. Skipping.")
            continue

        if len(img.shape) == 3 and img.shape[2] == 4:
            img_mode = 'RGBA'
        else:
            img_mode = None

        try:
            if args.face_enhance:
                _, _, output = face_enhancer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
            else:
                output, _ = upsampler.enhance(img, outscale=args.outscale)
        except RuntimeError as error:
            print(f'Error processing image {path}: {error}')
            print('If you encounter CUDA out of memory, try setting --tile with a smaller value.')
            continue

        # Determine output image extension
        if args.ext == 'auto':
            out_extension = extension[1:].lower()
        else:
            out_extension = args.ext.lower()

        if img_mode == 'RGBA':  # RGBA images should be saved as png
            out_extension = 'png'

        # Determine output save path
        if args.suffix:
            save_filename = f'{imgname}_{args.suffix}.{out_extension}'
        else:
            save_filename = f'{imgname}.{out_extension}'
        save_path = os.path.join(args.output, save_filename)

        # Save processed image
        success = cv2.imwrite(save_path, output)
        if success:
            print(f'Image saved at: {save_path}')
        else:
            print(f'Error: Unable to save image at {save_path}')

if __name__ == '__main__':
    main()
