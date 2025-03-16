import cv2
import numpy as np
import random
from PIL import Image, ImageEnhance, ImageFilter
from moviepy.editor import VideoFileClip, AudioFileClip


# Initialize camera
cap = cv2.VideoCapture(1)

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = 20  # Frames per second
output_file = "original_video.mp4"

# Define video writer (MP4 format)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

print("Recording video... Press 'q' to stop.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break 

    out.write(frame)  # Save the frame

    cv2.imshow("Recording", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video saved as {output_file}")
input_video = "original_video.mp4"
output_video = "edited_video.mp4"

def apply_random_effect(frame):
    """Apply aggressive random effects to the video frames."""
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Pick a STRONGER effect
    effect = random.choice(["invert", "rgb_shift", "high_contrast", "high_saturation", "blur", "sharpen"])

    if effect == "invert":
        img = Image.fromarray(255 - np.array(img))  # Inverts colors
    elif effect == "rgb_shift":
        img = np.array(img)
        img = img[..., [2, 0, 1]]  # Swap RGB channels randomly
        img = Image.fromarray(img)
    elif effect == "high_contrast":
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(random.uniform(1.5, 3.0))  # Extreme contrast
    elif effect == "high_saturation":
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(random.uniform(1.5, 3.0))  # Extreme saturation
    elif effect == "blur":
        img = img.filter(ImageFilter.GaussianBlur(random.randint(2, 5)))  # Strong blur
    elif effect == "sharpen":
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(random.uniform(2.0, 5.0))  # Over-sharpening

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)



# Open the recorded video
cap = cv2.VideoCapture(input_video)

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))

# Define video writer (MP4 format)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4
out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

print("Processing video...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    edited_frame = apply_random_effect(frame)  # Apply effect

    out.write(edited_frame)  # Save the modified frame

cap.release()
out.release()

print(f"Edited video saved as {output_video}")



edited_video = "edited_video.mp4"

final_output = "final_video_with_audio.mp4"

songs = ["background.mp3", "background2.mp3", "background3.mp3"]

# 🎲 Randomly select one
background_audio = random.choice(songs)

print(f"Selected background music: {background_audio}")

try:
    video = VideoFileClip(edited_video)
    audio = AudioFileClip(background_audio).subclip(0, video.duration)  # Trim audio

    final_video = video.set_audio(audio)
    final_video.write_videofile(final_output, codec="libx264", fps=video.fps)

    print(f"Final video with audio saved as {final_output}")
except Exception as e:
    print(f"Error adding audio: {e}")