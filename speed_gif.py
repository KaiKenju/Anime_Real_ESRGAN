# from PIL import Image, ImageSequence

# def adjust_gif_speed(gif_path, target_duration, target_fps):
#     gif = Image.open(gif_path)
#     frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
#     num_frames = len(frames)
    
#     # Tính toán lại thời gian hiển thị mỗi khung hình
#     frame_duration = int(1000 / target_fps)  # Thời gian mỗi khung (ms) theo FPS mục tiêu
#     new_total_duration = frame_duration * num_frames
    
#     # Nếu tổng thời gian mới dài hơn hoặc ngắn hơn thời gian mục tiêu, điều chỉnh lại
#     scale_factor = target_duration / new_total_duration
#     new_frame_duration = int(frame_duration * scale_factor)
    
#     # Tạo một GIF mới với thời gian hiển thị đã được điều chỉnh
#     frames[0].save(f'adjusted_{gif_path}', save_all=True, append_images=frames[1:], duration=new_frame_duration, loop=0)

# def synchronize_gifs(gif1_path, gif2_path, target_duration, target_fps):
#     adjust_gif_speed(gif1_path, target_duration, target_fps)
#     adjust_gif_speed(gif2_path, target_duration, target_fps)
#     print(f"Đã điều chỉnh cả hai GIF về tổng thời gian {target_duration} ms và FPS {target_fps}.")

# # Đường dẫn đến các GIF
# gif1_path = 'Tesla_animation.gif'
# gif2_path = 'Tesla_animation_outx2_v1.gif'

# # Thời gian mục tiêu và FPS mục tiêu
# target_duration = 15000  # Ví dụ: 5000 ms (5 giây)
# target_fps = 300  # Ví dụ: 30 khung hình mỗi giây

# synchronize_gifs(gif1_path, gif2_path, target_duration, target_fps)

from PIL import Image, ImageSequence
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    return frames

def display_two_gifs(gif1_path, gif2_path):
    # Tải các khung hình từ cả hai GIF
    frames1 = load_gif_frames(gif1_path)
    frames2 = load_gif_frames(gif2_path)

    # Tìm số lượng khung hình lớn nhất để đồng bộ
    max_frames = max(len(frames1), len(frames2))

    # Thiết lập figure để hiển thị GIF
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.set_title('GIF 1')
    ax2.set_title('GIF 2')

    img1 = ax1.imshow(frames1[0])
    img2 = ax2.imshow(frames2[0])

    def update(frame):
        # Cập nhật từng frame cho mỗi GIF
        img1.set_data(frames1[frame % len(frames1)])
        img2.set_data(frames2[frame % len(frames2)])
        return img1, img2

    anim = FuncAnimation(fig, update, frames=max_frames, interval=100, blit=True)

    plt.show()

# Đường dẫn đến GIF đã điều chỉnh
gif1_path = 'Tesla_animation.gif'
gif2_path = 'Tesla_animation_outx2_v1.gif'

display_two_gifs(gif1_path, gif2_path)
