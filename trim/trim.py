import subprocess

def trim_and_reencode(input_file, start_time, duration, output_file):
    """
    Trim a video file and re-encode it using ffmpeg.
    input_file: Path to the input file.
    start_time: Start time in seconds.
    duration: Duration in seconds.
    output_file: Path to the output file.
    """
    command = [
        "ffmpeg",
        "-ss", str(start_time),  # Start time
        "-i", input_file,        # Input file
        "-t", str(duration),     # Duration
        "-c:v", "libx264",       # Re-encode video to H.264
        "-crf", "23",            # Quality factor for x264
        "-preset", "fast",       # Encoding speed/quality tradeoff
        "-c:a", "aac",           # Re-encode audio
        "-b:a", "128k",          # Audio bitrate
        "-keyint_min", "30",     # Minimum keyframe interval
        "-g", "60",              # Maximum keyframe interval (frames)
        "-sc_threshold", "0",    # Disable scene change detection for consistent keyframes
        output_file
    ]
    subprocess.run(command, check=True)

    
    
def concat_clips(segments, output_file):
    with open("file_list.txt", "w") as f:
        for segment in segments:
            f.write(f"file '{segment}'\n")    
    command = [
        "ffmpeg",
        "-f", "concat",       # Use concat demuxer
        "-safe", "0",         # Allow potentially unsafe file paths
        "-i", "file_list.txt",# Input file list
        "-c:v", "libx264",    # Re-encode during concatenation
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "128k",
        output_file
    ]

    # Run the command
    try:
        subprocess.run(command, check=True)
        print("FFmpeg command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")