import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)

CHASTIMENTS = [
    'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!'
]


def check_schoolkid(full_name):
    schoolkid = get_object_or_404(
        Schoolkid, full_name__contains=full_name)
    return schoolkid


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid).delete()
    return chastisements


def fix_marks(schoolkid):
    marks = (
        Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)
        )
    return marks


def create_commendation(full_name, subject):
    schoolkid = check_schoolkid(full_name)
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject).first()
    if not lesson:
        print(f"No lesson found for {subject}"
              "in {year_of_study}{group_letter}")
        return None
    new_commendation = Commendation.objects.create(
        text=random.choice(CHASTIMENTS),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
        )
    return new_commendation
