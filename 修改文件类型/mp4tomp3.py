
#import sys
#print("当前Python路径：", sys.executable)
#print("当前Python版本：", sys.version)

from moviepy import VideoFileClip

# def extract_audio(video_path, output_path):
#
#     video_clip = VideoFileClip(video_path)
#
#     audio_clip = video_clip.audio
#
      audio_clip.write_audiofile(output_path, codec='mp3')
#
#     audio_clip.close()
#     video_clip.close()
#
# extract_audio('C:/Users/ass/Music/晴天.mp4', 'C:/Users/ass/Music/晴天.mp3')

#with写法：
# def extract_audio(video_path, output_path):
#     try:
#         with VideoFileClip(video_path) as video_clip:
#             if video_clip.audio is None:
#                 raise ValueError("该视频文件没有音频轨道！")
#             video_clip.audio.write_audiofile(output_path, codec='mp3')
#         print(f"音频提取成功。保存路径：{output_path}")
#     except Exception as e:
#         print(f"提取音频失败：{str(e)}")

#批量写法：
# import os
# def extract_batch_audios(video_dir, output_dir):
#     for i in os.listdir(video_dir):
#         video_path = os.path.join(video_dir, i)
#         output_path = os.path.join(output_dir, i.rsplit('.', 1)[0] + '.mp3')
#         try:
#             with VideoFileClip(video_path) as video:
#                 video.audio.write_audiofile(output_path, codec='mp3')
#             print(f"✅ 完成: {i}")
#         except Exception as e:
#             print(f"❌ 失败: {i} - {str(e)}")
#
# extract_batch_audios('C:/Users/ass/Music/', "C:/Users/ass/Desktop/temp/")
# print("\n🎉 批量提取任务完成。")






        
