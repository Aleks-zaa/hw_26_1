from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import UrlValidator


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlValidator(field='video_url')]
        # video_url = CharField(validators=[url_validator])


class CourseDetailSerializer(ModelSerializer):
    lesson_in_course = SerializerMethodField()
    # lesson_list = SerializerMethodField()
    lesson_set = LessonSerializer(many=True)

    def get_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("name", "description", "lesson_in_course", "lesson_set")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
