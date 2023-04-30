import os
import shutil
import cv2

source_folder = 'J:/Camera01'
output_folder = 'H:/Media-Upload'
max_file_size = 9663676416  # 10GB in bytes
move_files = False  # Set to True to move files instead of copying them

for filename in os.listdir(source_folder):
    if filename.endswith('.mp4') or filename.endswith('.avi'):

        filepath = os.path.join(source_folder, filename)
        file_size = os.path.getsize(filepath)
        print(f'Now doing {filename}')
        if os.path.getsize(filepath) > max_file_size:
            cap = cv2.VideoCapture(filepath)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            segment_count = int((file_size / max_file_size) + 1)
            segment_duration = int(frame_count / segment_count / fps)
            cap.release()
            for i in range(segment_count):
                start_time = i * segment_duration
                end_time = (i + 1) * segment_duration
                output_filename = os.path.join(output_folder, f"{filename.split('.')[0]}_{i+1}.mp4")
                segment_filepath = os.path.join(output_folder, f"{filename.split('.')[0]}_{i+1}.mkv")
                print(f'Now doing {filename}')
                command = f"ffmpeg -n -copyts -ss {start_time} -i {filepath} -map_metadata 0 -movflags use_metadata_tags -movflags +faststart -to {end_time} -c:v copy -c:a copy -copy_unknown -strict unofficial {segment_filepath}"
                print(command)
                os.system(command)
                if move_files:
                    os.rename(segment_filepath, output_filename)
                else:
                    pass
            continue
            if move_files:
                os.rename(filepath, os.path.join(output_folder, filename))
            else:
                shutil.copy(filepath, os.path.join(output_folder, filename))
        else:
            if move_files:
                os.rename(filepath, os.path.join(output_folder, filename))
            else:
                if not os.path.exists(os.path.join(output_folder, filename)):
                    shutil.copy(filepath, os.path.join(output_folder, filename))

#TODO Cleanup
