import json
import csv
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Comment

@csrf_exempt
@api_view(['POST'])
def store_comments_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            comments = data.get('data', [])
            for comment_data in comments:
                Comment.objects.create(
                    work_platform_id=comment_data['work_platform']['id'],
                    content_url=comment_data['content_url'],
                    text=comment_data['text'],
                    commenter_username=comment_data['commenter_username'],
                    commenter_display_name=comment_data['commenter_display_name'],
                    like_count=comment_data['like_count'],
                    reply_count=comment_data['reply_count'],
                    published_at=comment_data['published_at']
                )
            return JsonResponse({'message': 'Data stored successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@api_view(['GET'])
def get_comments_view(request):
    if request.method == 'GET':
        comments = Comment.objects.all().values()
        return JsonResponse({'comments': list(comments)}, status=200)
    return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

@api_view(['GET'])
def export_comments_csv(request):
    content_url = request.GET.get('content_url', None)
    if not content_url:
        return JsonResponse({'error': 'content_url parameter is required'}, status=400)

    comments = Comment.objects.filter(content_url=content_url)
    if not comments.exists():
        return JsonResponse({'error': 'No comments found for the specified content_url'}, status=404)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="comments_{content_url.split("/")[-2]}.csv"'

    writer = csv.writer(response)
    writer.writerow(['work_platform_id', 'content_url', 'text', 'commenter_username', 'commenter_display_name', 'like_count', 'reply_count', 'published_at'])

    for comment in comments:
        writer.writerow([
            comment.work_platform_id,
            comment.content_url,
            comment.text,
            comment.commenter_username,
            comment.commenter_display_name,
            comment.like_count,
            comment.reply_count,
            comment.published_at,
        ])

    return response
