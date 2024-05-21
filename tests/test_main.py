import unittest
from unittest.mock import patch, MagicMock
import os
from main import create_visualization, compress_video, process_audio


class TestCompressVideo(unittest.TestCase):

    @patch('main.VideoFileClip')
    def test_compress_video(self, mock_videofileclip):
        # Создаем мок объекта VideoFileClip
        mock_clip = MagicMock()
        mock_videofileclip.return_value = mock_clip

        video_path = 'test_video.mp4'
        compressed_path = 'test_compressed.mp4'

        # Вызываем тестируемую функцию
        compress_video(video_path, compressed_path)

        # Проверяем, что VideoFileClip был вызван с правильными аргументами
        mock_videofileclip.assert_called_once_with(video_path)

        # Проверяем, что методы write_videofile и close были вызваны на объекте mock_clip
        mock_clip.write_videofile.assert_called_once_with(compressed_path, codec="libx265", bitrate="2500k")
        mock_clip.close.assert_called_once()


class TestProcessAudioHandler(unittest.TestCase):

    @patch('os.makedirs')
    @patch('os.remove')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('aiogram.types.Message.reply')
    @patch('aiogram.types.Message.reply_video')
    @patch('aiogram.types.Message.audio.download')
    @patch('main.create_visualization')
    @patch('main.compress_video')
    async def test_process_audio(self, mock_compress_video, mock_create_visualization, mock_download, mock_reply_video, mock_reply, mock_open, mock_remove, mock_makedirs):
        message = MagicMock()
        message.audio.mime_type = 'audio/mpeg'
        message.audio.file_unique_id = '12345'
        audio_file_path = os.path.join('visualization_videos', '12345.mp3')
        visualization_file = os.path.join('visualization_videos', '12345.mp4')
        compressed_video_path = os.path.join('visualization_videos', '12345_compressed.mp4')

        await process_audio(message)

        mock_download.assert_called_once_with(destination=audio_file_path)
        mock_create_visualization.assert_called_once_with(audio_file_path, visualization_file)
        mock_compress_video.assert_called_once_with(visualization_file, compressed_video_path)
        mock_reply_video.assert_called_once()
        mock_remove.assert_any_call(audio_file_path)
        mock_remove.assert_any_call(compressed_video_path)

    @patch('aiogram.types.Message.reply')
    async def test_process_audio_invalid_mime_type(self, mock_reply):
        message = MagicMock()
        message.audio.mime_type = 'audio/wav'

        with self.assertRaises(Exception):
            await process_audio(message)

        mock_reply.assert_called_once_with('Извините, я могу обрабатывать только аудиофайлы в формате MP3.')

if __name__ == '__main__':
    unittest.main()
