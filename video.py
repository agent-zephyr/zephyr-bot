from moviepy import TextClip, concatenate_videoclips, VideoFileClip, CompositeVideoClip

def create_title_screen(text, output_file='output_video.mp4', duration=5, resolution=(1920, 1080)):
    # Create a TextClip with the desired text
    title_clip = TextClip(
        font='Arial',                   # Font type
        text=text,                         # The text to display
        font_size=70,                   # Font size
        color='white',                 # Text color
        size=resolution,               # Video resolution (width, height)
    )

    # Set the duration for the title screen
    title_clip = title_clip.with_duration(duration)

    # Optionally set a background color (black)
    # title_clip = title_clip.on_color(color=(0, 0, 0), col_opacity=1)

    # Write the final video file
    title_clip.write_videofile(output_file, fps=24)