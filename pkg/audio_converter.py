import os
import logging
from pydub import AudioSegment
import pilk

def audio_to_pcm(audio_path: str, temp_folder: str) -> tuple[str, int]:
    try:
        audio = AudioSegment.from_file(audio_path)
        sample_rate = audio.frame_rate
        pcm_data = audio.raw_data
        pcm_path = os.path.join(temp_folder, os.path.splitext(os.path.basename(audio_path))[0] + '.pcm')
        with open(pcm_path, 'wb') as pcm_file:
            pcm_file.write(pcm_data)
        return pcm_path, sample_rate
    except Exception as e:
        logging.error(f"Error converting audio to PCM: {e}")
        raise

def convert_audio_to_silk(audio_path: str, temp_folder: str) -> str:
    try:
        pcm_path, sample_rate = audio_to_pcm(audio_path, temp_folder)
        silk_path = os.path.join(temp_folder, os.path.splitext(os.path.basename(pcm_path))[0] + '.silk')
        pilk.encode(pcm_path, silk_path, pcm_rate=sample_rate, tencent=True)

        # 删除临时文件
        os.remove(pcm_path)

        return silk_path
    except Exception as e:
        logging.error(f"Error converting audio to SILK: {e}")
        raise

if __name__ == "__main__":
    # 示例用法
    mp3_file_path = "sample.mp3"
    wav_file_path = "sample.wav"
    temp_folder_path = "../audio_temp"

    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)

    # 转换MP3文件为SILK
    silk_path_mp3 = convert_audio_to_silk(mp3_file_path, temp_folder_path)
    print(f"SILK file from MP3: {silk_path_mp3}")

    # 转换WAV文件为SILK
    silk_path_wav = convert_audio_to_silk(wav_file_path, temp_folder_path)
    print(f"SILK file from WAV: {silk_path_wav}")
