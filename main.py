import os
import subprocess
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from moviepy.editor import VideoFileClip

TOKEN = '5804494344:AAEYEObmmddT0JQxgUo9MAW_hWVFyJrNhvo'
SAVE_DIR = 'visualization_videos'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def create_visualization(audio_path, output_path):
    subprocess.run(['ffmpeg', '-i', audio_path, '-filter_complex', 'showwaves=s=1280x720:mode=cline', '-y', output_path])


def compress_video(video_path, compressed_path):
    clip = VideoFileClip(video_path)
    clip.write_videofile(compressed_path, codec="libx265", bitrate="2500k")  # bitrate
    clip.close()


@dp.message_handler(content_types=types.ContentType.AUDIO)
async def process_audio(message: types.Message):
    if message.audio.mime_type != 'audio/mpeg':
        await message.reply('Извините, я могу обрабатывать только аудиофайлы в формате MP3.')
        return

    audio_file_path = os.path.join(SAVE_DIR, f'{message.audio.file_unique_id}.mp3')
    await message.audio.download(destination=audio_file_path)

    visualization_file = os.path.join(SAVE_DIR, f'{message.audio.file_unique_id}.mp4')
    create_visualization(audio_file_path, visualization_file)

    compressed_video_path = os.path.join(SAVE_DIR, f'{message.audio.file_unique_id}_compressed.mp4')
    compress_video(visualization_file, compressed_video_path)

    with open(compressed_video_path, 'rb') as video:
        await message.reply_video(video)

    os.remove(compressed_video_path)
    os.remove(audio_file_path)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот, который может создавать визуализацию аудио в виде анимированного видео. Просто отправь мне аудиофайл в формате MP3, и я сделаю визуализацию для него!")


if __name__ == '__main__':
    os.makedirs(SAVE_DIR, exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
