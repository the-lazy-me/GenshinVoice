import os
import requests
import logging
import yaml
from uuid import uuid4
from plugins.GenshinVoice.pkg.audio_converter import convert_to_silk


class AudioGenerator:
    def __init__(self, config, character=None):
        self.config = config

        # If character is provided by the user, use it; otherwise, use the one from the config file
        if character:
            self.config["character"] = character

    def get_audio_url(self, text: str, session_hash):
        api = https://bv2.firefly.matce.cn/"
        data = {
            "data": [
                text,
                self.config["character"],  # Use self.config here
                self.config["sdp_radio"],
                self.config["ns"],
                self.config["nsw"],
                self.config["audio_speed"],
                self.config["character"].split("_")[1],
                True,
                self.config["para_stop"],
                self.config["sen_stop"],
                None,
                self.config["emotion"],
                "",
                self.config["weight"]
            ],
            "event_data": 'null',
            "fn_index": 0,
            "session_hash": session_hash
        }
        # print(data)
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }

        try:
            resp = requests.post(api + "/run/predict", json=data, headers=headers)
            response_data = resp.json()["data"]
            if response_data[0] == "Success":
                file_name = response_data[1]["name"]
                # print(api + f"/file={file_name}")
                return api + f"/file={file_name}"
        except Exception as e:
            logging.error(f"Error generating audio: {str(e)}")

        return None

    def download_audio(self, url, save_path):
        try:
            audio_content = requests.get(url)
            if audio_content.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(audio_content.content)
                logging.debug(f"Audio downloaded successfully to {save_path}")
                return True
        except Exception as e:
            logging.error(f"Error downloading audio: {str(e)}")
        return False

    def generate_audio(self, text):
        session_hash = str(uuid4()).lower().split("-")[0]
        audio_url = self.get_audio_url(text, session_hash)

        if not os.path.exists("../audio_temp"):
            os.makedirs("../audio_temp")

        if audio_url:
            save_path = os.path.join(os.getcwd(), "../audio_temp", f"{session_hash}.mp3")
            # print(save_path)
            success = self.download_audio(audio_url, save_path)

            if success:
                silk_path = convert_to_silk(save_path, "../audio_temp")
                os.remove(save_path)
                # print(silk_path)
                return silk_path
            else:
                logging.error("Failed to download audio.")
        else:
            # print(audio_url)
            logging.error("Failed to generate audio.")
        return None


if __name__ == "__main__":
    with open("../config/config.yml", "r", encoding='UTF-8') as config_file:
        config = yaml.safe_load(config_file)
        logging.info(config)

    # Check if the user has specified a character
    user_character = input("Enter the character (press Enter to use default): ").strip()

    # 读取角色列表txt
    with open("../config/角色列表.txt", "r", encoding='UTF-8') as file:
        characters = file.read().splitlines()

    # 如果不是角色列表中的角色，提示错误并退出
    if user_character and user_character not in characters:
        print("Invalid character.")
        exit()

    # Pass the "character" parameter as an argument when creating AudioGenerator
    audio_generator = AudioGenerator(config, character=user_character or None)

    result = audio_generator.generate_audio("你好，世界！")

    if result:
        print(result)
        # base64 encode the silk and return the base64 encoded string
        with open(result, 'rb') as f:
            result = f.read()
        print(result)
