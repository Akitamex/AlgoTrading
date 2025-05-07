from rest_framework import serializers
from .models import Course, Chapter, Lesson, Review, Progress


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
        

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class ProgressSerializer(serializers.ModelSerializer):
    enroled_courses = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all(), required=False)
    finished_courses = serializers.PrimaryKeyRelatedField(many=True, queryset=Course.objects.all(), required=False)
    finished_lessons = serializers.PrimaryKeyRelatedField(many=True, queryset=Lesson.objects.all(), required=False)
    
    class Meta:
        model = Progress
        fields = '__all__'
        
    def update(self, instance, validated_data):
        instance.enroled_courses.set(validated_data.get('enroled_courses', []))
        instance.finished_courses.set(validated_data.get('finished_courses', []))
        instance.finished_lessons.set(validated_data.get('finished_lessons', []))

        instance.save()
        return instance
    