from django.core.exceptions import ValidationError
import os


def get_path_upload_avatar(instance, file):
    """Building a file path,format: (media)/avatar/user_id/photo.jpg
    """
    return f'avatar/user_{instance.id}/{file}'


def get_path_upload_cover_album(instance, file):
    """Building a file path,format: (media)/album/user_id/photo.jpg
    """
    return f'album/user_{instance.user.id}/{file}'


def get_path_upload_video(instance, file):
    """Building a file path,format: (media)/video/user_id/photo.jpg
    """
    return f'video/user_{instance.user.id}/{file}'


def get_path_upload_cover_playlist(instance, file):
    """Building a file path,format: (media)/playlist/user_id/photo.jpg
    """
    return f'playlist/user_{instance.user.id}/{file}'

def get_path_upload_cover_video(instance, file):
    """Building a file path,format: (media)/video/cover/user_id/photo.jpg
    """
    return f'video/cover/user_{instance.user.id}/{file}'


def validate_size_image(file_obj):
    """Check file size
    """
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {megabyte_limit} мегабайта')


def delete_old_file(path_file):
    """Removing old file
    """
    if os.path.exists(path_file):
        os.remove(path_file)
