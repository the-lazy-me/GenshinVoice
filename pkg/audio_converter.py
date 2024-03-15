# # import os
# # import logging
# # from pydub import AudioSegment
# # import pilk
# #
# #
# # def audio_to_pcm(audio_path: str, temp_folder: str) -> tuple[str, int]:
# #     try:
# #         audio = AudioSegment.from_file(audio_path)
# #         sample_rate = audio.frame_rate
# #         pcm_data = audio.raw_data
# #         pcm_path = os.path.join(temp_folder, os.path.splitext(os.path.basename(audio_path))[0] + '.pcm')
# #         with open(pcm_path, 'wb') as pcm_file:
# #             pcm_file.write(pcm_data)
# #         return pcm_path, sample_rate
# #     except Exception as e:
# #         logging.error(f"Error converting audio to PCM: {e}")
# #         raise
# #
# #
# # def convert_audio_to_silk(audio_path: str, temp_folder: str) -> str:
# #     try:
# #         pcm_path, sample_rate = audio_to_pcm(audio_path, temp_folder)
# #
# #         silk_path = os.path.join(temp_folder, os.path.splitext(os.path.basename(pcm_path))[0] + '.silk')
# #         pilk.encode(pcm_path, silk_path, pcm_rate=sample_rate, tencent=True)
# #
# #         # 删除临时文件
# #         # os.remove(pcm_path)
# #
# #         return silk_path
# #     except Exception as e:
# #         logging.error(f"Error converting audio to SILK: {e}")
# #         raise
# #
# #
# # if __name__ == "__main__":
# #     # 示例用法
# #     mp3_file_path = "audio.mp3"
# #     wav_file_path = "audio.wav"
# #     temp_folder_path = "../audio_temp"
# #
# #     if not os.path.exists(temp_folder_path):
# #         os.makedirs(temp_folder_path)
# #
# #     # 转换MP3文件为SILK
# #     silk_path_mp3 = convert_audio_to_silk(mp3_file_path, temp_folder_path)
# #     print(f"SILK file from MP3: {silk_path_mp3}")
# #
# #     # 转换WAV文件为SILK
# #     silk_path_wav = convert_audio_to_silk(wav_file_path, temp_folder_path)
# #     print(f"SILK file from WAV: {silk_path_wav}")
#
#
# import os
# import logging
# import av
# import pilk
#
#
# def to_pcm(in_path: str) -> tuple[str, int]:
#     out_path = os.path.splitext(in_path)[0] + '.pcm'
#     with av.open(in_path) as in_container:
#         in_stream = in_container.streams.audio[0]
#         sample_rate = 24000
#         with av.open(out_path, 'w', 's16le') as out_container:
#             out_stream = out_container.add_stream(
#                 'pcm_s16le',
#                 rate=sample_rate,
#                 layout='mono'
#             )
#             try:
#                 for frame in in_container.decode(in_stream):
#                     frame.pts = None
#                     for packet in out_stream.encode(frame):
#                         out_container.mux(packet)
#             except:
#                 pass
#     return out_path, sample_rate
#
#
# def convert_to_silk(media_path: str,temp_folder: str) -> str:
#     pcm_path, sample_rate = to_pcm(media_path)
#     # silk_path = os.path.splitext(pcm_path)[0] + '.silk'
#     # 将silk保存在temp临时文件夹
#     silk_path = os.path.join(temp_folder, os.path.splitext(os.path.basename(pcm_path))[0] + '.amr')
#     print(pcm_path, silk_path)
#     pilk.encode(pcm_path, silk_path, pcm_rate=24000, tencent=True)
#     logging.debug('silk生成成功')
#     return silk_path


import os
import logging

from io import BytesIO
from pathlib import Path
from graiax import silkcoder


def convert_to_silk(wav_path: str, temp_folder: str) -> str:
    # 读取 WAV 文件的二进制数据
    wav_data = Path(wav_path).read_bytes()

    # 对 WAV 数据进行 SILK 编码
    silk_data = silkcoder.encode(BytesIO(wav_data))

    # 将silk保存在temp临时文件夹
    silk_path = os.path.join(temp_folder, os.path.splitext(os.path.basename(wav_path))[0] + '.silk')

    # 将 SILK 数据写入 SILK 文件
    with open(silk_path, "wb") as silk_file:
        silk_file.write(silk_data)

    logging.debug(f"已将 WAV 文件 {wav_path} 转换为 SILK 文件 {silk_path}")
    return silk_path
