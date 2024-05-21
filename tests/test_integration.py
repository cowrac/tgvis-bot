import unittest
from unittest.mock import patch, MagicMock
import os
from aiogram import types, Dispatcher, Bot
from aiogram.types import ContentType
from main import dp, bot, process_audio, create_visualization, compress_video

class TestTelegramBotIntegration(unittest.TestCase):

    @patch('main.create_visualization')
    @patch('main.compress_video')
    @patch('aiogram.types.Message.reply_video')
    @patch('aiogram.types.Message.reply')
    @patch('aiogram.types.Message.audio.download')
    @patch('os.remove')
    async def test_process_audio(self, mock_remove, mock_download, mock_reply, mock_reply_video, mock_create_visualization, mock_compress_video):
        # Создаем мок-объект для сообщения
        message = MagicMock(spec=types.Message)
        message.audio.mime_type = 'audio/mpeg'
        message.audio.file_unique_id = '12345'
        message.audio.download.return_value = 'path/to/downloaded/file.mp3'

        audio_file_path = os.path.join('visualization_videos', '12345.mp3')
        visualization_file = os.path.join('visualization_videos', '12345.mp4')
        compressed_video_path = os.path.join('visualization_videos', '12345_compressed.mp4')

        # Вызываем функцию обработки аудио
        await process_audio(message)

        # Проверяем, что функции были вызваны с правильными аргументами
        mock_download.assert_called_once_with(destination=audio_file_path)
        mock_create_visualization.assert_called_once_with(audio_file_path, visualization_file)
        mock_compress_video.assert_called_once_with(visualization_file, compressed_video_path)
        mock_reply_video.assert_called_once()
        mock_remove.assert_any_call(audio_file_path)
        mock_remove.assert_any_call(compressed_video_path)

    @patch('aiogram.types.Message.reply')
    async def test_process_audio_invalid_mime_type(self, mock_reply):
        # Создаем мок-объект для сообщения с неверным MIME-типом
        message = MagicMock(spec=types.Message)
        message.audio.mime_type = 'audio/wav'

        with self.assertRaises(Exception):  # замените CancelHandler на Exception
            await process_audio(message)

        # Проверяем, что бот отправил сообщение с ошибкой
        mock_reply.assert_called_once_with('Извините, я могу обрабатывать только аудиофайлы в формате MP3.')

if __name__ == '__main__':
    unittest.main()
