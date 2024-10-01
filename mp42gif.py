from moviepy.editor import VideoFileClip

# Đường dẫn file video MP4
input_video = "results\Tesla_animation_outx2.mp4"
# Đường dẫn lưu file GIF
output_gif = "assets/gif/Tesla_animation_outx2.gif"

# Đọc video MP4
clip = VideoFileClip(input_video)

# Cắt video để lấy đoạn ngắn (ví dụ từ giây thứ 0 đến giây thứ 5)
clip = clip.subclip(5, 20)

# Tăng tốc độ khung hình (fps)
increased_fps = 60

# Chuyển đổi và lưu dưới dạng GIF
clip.write_gif(output_gif, fps=increased_fps)

print(f"GIF đã được lưu tại {output_gif}")
