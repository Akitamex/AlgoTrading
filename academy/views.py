from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CourseSerializer, ChapterSerializer, LessonSerializer, ReviewSerializer, ProgressSerializer
from .models import Course, Chapter, Lesson, Review, Progress

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken



class CourseAPIView(APIView):
    def get(self, request, course_id=None):
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                reviews = Review.objects.filter(course_id=course_id)
                reviews_serializer = ReviewSerializer(reviews, many=True)
                serializer = CourseSerializer(course).data
                serializer['reviews_count'] = reviews.count()
                
                review_data = reviews_serializer.data
                total_mark = sum(int(review['mark']) for review in review_data)
                
                try:
                    serializer['avg_mark'] = int(total_mark / len(review_data))
                except ZeroDivisionError:
                    pass

                
                return Response({'course': dict(serializer)})
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True).data
        
        for course in serializer:
            course['reviews_count'] = Review.objects.filter(course_id=course['id']).count()
            
            reviews = Review.objects.filter(course_id=course['id'])
            reviews_serializer = ReviewSerializer(reviews, many=True).data
            total_mark = 0
            
            if reviews_serializer:
                total_mark = sum(review['mark'] for review in reviews_serializer)
                
                try:
                    course['avg_mark'] = int(total_mark / len(reviews_serializer))
                except ZeroDivisionError:
                    pass
            else:
                course['avg_mark'] = 0
            
        
        return Response({'courses': serializer})
    

class ChapterAPIView(APIView):
    def get(self, request, course_id, chapter_id=None):
        if chapter_id:
            try:
                chapter = Chapter.objects.get(id=chapter_id)
                serializer = ChapterSerializer(chapter)
                return Response({'chapter': serializer.data})
            except Chapter.DoesNotExist:
                return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
        
        chapters = Chapter.objects.filter(course_id=course_id)
        serializer = ChapterSerializer(chapters, many=True)
        return Response({'course_id': course_id, 'chapters': serializer.data})


class LessonAPIView(APIView):
    def get(self, request, course_id, chapter_id, lesson_id=None):
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                serializer = LessonSerializer(lesson)
                return Response({'lesson': serializer.data})
            except Lesson.DoesNotExist:
                return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)
        
        lessons = Lesson.objects.filter(chapter_id=chapter_id)
        serializer = LessonSerializer(lessons, many=True)
        return Response({'course_id': course_id, 'chapter_id': chapter_id, 'lessons': serializer.data})
    
    
class ReviewAPIView(APIView):
    def get(self, request, course_id, review_id=None):
        if review_id:
            try:
                review = Review.objects.get(id=review_id)
                serializer = ReviewSerializer(review)
                return Response({'review': serializer.data})
            except Review.DoesNotExist:
                return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        reviews = Review.objects.filter(course_id=course_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response({'course_id': course_id, 'reviews': serializer.data})

    def post(self, request, course_id, format=None):
        access_token = request.data.get('access_token')
        
        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                user_id = decoded_token['user_id']
            except InvalidToken:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Access token not specified'}, status=status.HTTP_401_UNAUTHORIZED)
        
        request.data['user'] = user_id
        request.data['course'] = course_id
            
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class ProgressAPIView(APIView):
    def get(self, request, user_uuid=None):
        if user_uuid:
            progress = Progress.objects.get(user_id=user_uuid)
        
            serializer = ProgressSerializer(progress)
            return Response({'progress': serializer.data})
        
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        access_token = request.data.get('access_token')
        
        if access_token:
            try:
                decoded_token = AccessToken(access_token)
                user_id = decoded_token['user_id']
            except InvalidToken:
                return Response({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Access token not specified'}, status=status.HTTP_401_UNAUTHORIZED)
            
        try:
            progress = Progress.objects.get(user_id=user_id)
        except Progress.DoesNotExist:
            return Response({'error': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProgressSerializer(progress, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
            
    
    
    # def put(self, request, id, format=None):
    #     try:
    #         user = CustomUser.objects.get(id=id)
    #     except CustomUser.DoesNotExist:
    #         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = UserSerializer(user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
