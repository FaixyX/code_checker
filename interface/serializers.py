from rest_framework import serializers
from .models import MyUser, ProgrammingLanguage, ExpertiseLevel, QuizQuestion, TheoryQuestion, AssignmentResponse, Assignment


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('email' , 'password')


class UserProfileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        exclude = ('password', )


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = '__all__'


class ExpertiseLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseLevel
        fields = '__all__'


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = ['id', 'question_text', 'programming_language', 'expertise_level', 'created_at']


class TheoryQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheoryQuestion
        fields = ['id', 'question_text', 'programming_language', 'expertise_level', 'created_at']


class AssignmentResponseSerializer(serializers.ModelSerializer):
    """Serializer for individual responses within an assignment."""
    class Meta:
        model = AssignmentResponse
        fields = ['id', 'question_type', 'question_id', 'user_response', 'is_correct', 'created_at']


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for the Assignment model, including nested details."""
    # Use nested serializers for related fields to provide more context
    user = UserProfileRetrieveSerializer(read_only=True) # Use existing user serializer
    programming_language = ProgrammingLanguageSerializer(read_only=True)
    expertise_level = ExpertiseLevelSerializer(read_only=True)
    # Nest responses when retrieving a specific assignment detail
    responses = AssignmentResponseSerializer(many=True, read_only=True, source='assignmentresponse_set')

    class Meta:
        model = Assignment
        fields = [
            'id', 'user', 'programming_language', 'expertise_level', 
            'created_at', 'completed_at', 'score', 'total_questions',
            'responses' # Include the nested responses
        ]
        read_only_fields = ['created_at', 'completed_at', 'score', 'total_questions', 'responses']
