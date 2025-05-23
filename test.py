@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    user = request.user
    question_id = request.data.get('question_id')
    code = request.data.get('code')
    language = request.data.get('language')
    start_time = request.data.get('start_time')
    
    # Validate required fields
    if not question_id:
        return Response({'error': 'Question ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    if not code:
        return Response({'error': 'Code submission is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    if not language:
        return Response({'error': 'Programming language is required'}, status=status.HTTP_400_BAD_REQUEST)
        
    if not start_time:
        return Response({'error': 'Start time is required'}, status=status.HTTP_400_BAD_REQUEST)

    print(f"User {user.id} submitted code for question {question_id}")

    try:
        question = QuizQuestion.objects.get(id=question_id)
        level = question.expertise_level.level
    except QuizQuestion.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

    # Calculate time taken
    end_time = timezone.now()
    print(f"End time: {end_time}")
    
    # Handle timezone-aware datetime string
    try:
        # Parse the datetime string
        start_time_dt = timezone.datetime.fromisoformat(start_time)
        
        # Check if it's already timezone-aware
        if timezone.is_aware(start_time_dt):
            start_time = start_time_dt
        else:
            start_time = timezone.make_aware(start_time_dt)
    except Exception as e:
        print(f"Error parsing start_time: {e}")
        # Default to 5 minutes ago if we can't parse the time
        start_time = timezone.now() - timezone.timedelta(minutes=5)
    
    print(f"Start time: {start_time}")
    time_taken = (end_time - start_time).total_seconds()
    print(f"Time taken: {time_taken}")



    # Define headers for LLM Verification
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    if not api_key:
        return Response({'error': 'OpenAI API key not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Extract just the problem statement for cleaner prompt
    problem_statement = question.question_text
    # Try to extract just the question part if possible
    question_match = re.search(r'Question:\s*(.+?)(?=Sample Input:|$)', problem_statement, re.DOTALL)
    if question_match:
        problem_statement = question_match.group(1).strip()

    # Enhanced LLM Verification prompt
    prompt = (
        f"You are an AI code checker responsible for evaluating the correctness of submitted code. Your task is to analyze the provided code snippet, determine if it correctly implements a solution to the given problem, and provide helpful feedback. Respond only with the JSON response.\n"
        f"### Problem Description:\n{problem_statement}\n\n"
        f"### Submitted Code ({language}):\n```\n{code}\n```\n\n"
        f"### Instructions:\n"
        f"1. Determine if the code correctly solves the problem.\n"
        f"4. Include brief, constructive feedback about the solution.\n\n"
        f"Respond with a JSON object in the following format:\n"
        f"```json\n"
        f"{{\n"
        f'  "correct": true/false,\n'
        f'  "feedback": "Brief explanation of the evaluation result",\n'
        f'  "failed_test_cases": [] // List of failed test cases if any\n'
        f"}}\n"
        f"```"
    )
    
    data = {
        'model': 'gpt-4o-mini',
        'messages': [
            {'role': 'system', 'content': 'You are a code verification assistant that provides accurate and helpful feedback.'},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0,
        'max_tokens': 1500,
    }
    
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data
        )
            
        if response.status_code == 200:
            result = response.json()
            verification_result = result['choices'][0]['message']['content'].strip()
                
            # Try to parse the JSON from the response
            try:
                # Clean the response in case it contains markdown formatting
                clean_result = re.sub(r'```json|```', '', verification_result).strip()
                verification_json = json.loads(clean_result)
                
                is_correct = verification_json.get('correct', False)
                feedback = verification_json.get('feedback', '')
                failed_test_cases = verification_json.get('failed_test_cases', [])
                
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from GPT response: {verification_result}")
                # If we can't parse the JSON, extract information using regex
                is_correct = 'true' in verification_result.lower() and '"correct": true' in verification_result.lower()
                feedback_match = re.search(r'"feedback":\s*"([^"]+)"', verification_result)
                feedback = feedback_match.group(1) if feedback_match else "Feedback not available"
                failed_test_cases = verification_json.get('failed_test_cases', [])
        else:
            print(f"OpenAI API Error: {response.status_code}, {response.text}")
            return Response({
                'error': 'Failed to verify code',
                'details': response.text
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    except Exception as e:
        print(f"Error during code verification: {e}")
        import traceback
        traceback.print_exc()
        
        # Fall back to test case results if API fails
        is_correct = all_passed
        feedback = "System encountered an error during verification. Evaluation based on test cases only."
        failed_test_cases = failed_cases

    # Format feedback
    formatted_feedback = "✅ Correct Answer: " if is_correct else "❌ Incorrect Answer: "
    formatted_feedback += feedback

    # Update user progress
    user_progress, created = UserProgress.objects.get_or_create(user=user)
    user_progress.total_attempts += 1
    if is_correct:
        user_progress.correct_answers += 1
    
    # Update accuracy
    if user_progress.total_attempts > 0:
        user_progress.accuracy = (user_progress.correct_answers / user_progress.total_attempts) * 100
    
    # Update average time
    if user_progress.average_time_per_question == 0:
        user_progress.average_time_per_question = time_taken
    else:
        user_progress.average_time_per_question = (user_progress.average_time_per_question + time_taken) / 2
    
    user_progress.save()

    # Save submission
    submission = UserSubmission.objects.create(
        user=user, 
        question=question, 
        code=code, 
        is_correct=is_correct, 
        time_taken=time_taken
    )

    return Response({
        'submission_id': submission.id,
        'is_correct': is_correct,
        'feedback': formatted_feedback,
        'time_taken': time_taken,
        'failed_test_cases': failed_test_cases,
    }, status=status.HTTP_200_OK)
    