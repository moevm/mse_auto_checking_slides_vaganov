from os import remove
from os.path import join, exists
from bson import ObjectId
from flask_login import current_user

from app.bd_helper.bd_helper import *
from app.main.checker import check
from app.main.parser import parse
from app.server import logger
from flask import current_app

import os
from logging import getLogger
logger = getLogger('root')


DEFAULT_PRESENTATION = 'sample.odp'

def get_file_len(file):
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0, 0)
    return file_length

def upload(request, upload_folder):
    try:
        if "presentation" in request.files:
            file = request.files["presentation"]
            if get_file_len(file) + get_storage() > current_app.config['MAX_SYSTEM_STORAGE']:
                logger.critical('Storage overload has occured')
                return 'storage_overload'
            converted_id = write_pdf(file)
            filename = join(upload_folder, file.filename)
            file.save(filename)
            delete = True
        else:
            filename = join(upload_folder, DEFAULT_PRESENTATION)
            delete = False

        presentation_name = basename(filename)
        logger.info("Обработка презентации " + presentation_name + " пользователя " +
              current_user.username + " проверками " + str(current_user.criteria))
        presentation = find_presentation(current_user, presentation_name)
        if presentation is None:
            user, presentation_id = add_presentation(current_user, presentation_name)
            presentation = get_presentation(presentation_id)

        checks = create_check(current_user)
        check(parse(filename), checks, presentation_name, current_user.username, converted_id)
        presentation, checks_id = add_check(presentation, checks, filename)

        if delete and exists(filename):
            remove(filename)

        logger.info("\tОбработка завершена успешно!")
        return str(checks_id)
    except Exception as e:
        logger.error("\tПри обработке произошла ошибка: " + str(e), exc_info=True)
        return 'Not OK, error: {}'.format(e)


def remove_presentation(json):
    count = len(current_user.presentations)
    user, presentation = delete_presentation(current_user, ObjectId(json['presentation']))
    deleted = count == len(user.presentations) - 1
    logger.info("Презентация " + presentation.name + " пользователя " + user.username + " удалена со всеми проверками")
    return 'OK' if deleted else 'Not OK'
