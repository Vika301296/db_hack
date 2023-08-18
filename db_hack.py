import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)

CHASTIMENTS = [
    'Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!'
]


def remove_chastisements(schoolkid):
    vanya_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in vanya_chastisements:
        chastisement.delete()
    return vanya_chastisements


def fix_marks(schoolkid):
    vanya_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in vanya_marks:
        mark.points = 5
        mark.save()
    return vanya_marks


def create_commendation(full_name, subject):
    schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject).first()
    if lesson:
        new_commendation = Commendation.objects.create(
            text=random.choice(CHASTIMENTS),
            created=lesson.date,
            schoolkid=schoolkid,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
        return new_commendation
    else:
        print(f"No lesson found for {subject}"
              "in {year_of_study}{group_letter}")
        return None
