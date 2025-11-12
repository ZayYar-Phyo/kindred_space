from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Post, Tag, UserProfile, Review, Follow
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


def home_view(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.select_related('user').all()
    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(body__icontains=query)
            | Q(artist__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()
    
    for post in posts:
        if post.user:
            UserProfile.objects.get_or_create(user=post.user)
    
    return render(request, 'a_posts/home.html', {'posts' : posts, 'q': query})


# View to handle post creation
@login_required
def post_create_view(request):
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            if not post.title:
                post.title = 'Untitled'
            post.save()
            form.save_m2m()
            return redirect('home')
    return render(request, 'a_posts/post_create.html', {'form' : form})

# View to handle post deletion
@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('home')
    return render(request, 'a_posts/post_delete.html', {'post': post})

# View to handle post editing
@login_required
def post_eidt_view(request, pk):
    post = get_object_or_404(Post, id=pk)
    form = PostEditForm(instance=post)
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('home')
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'a_posts/post_edit.html', context)
    
# View to display a single post
def post_page_view(request, pk):
    post = get_object_or_404(Post.objects.select_related('user'), id=pk)
    if post.user:
        UserProfile.objects.get_or_create(user=post.user)
    return render(request, 'a_posts/post_page.html', {'post': post})


# Geocoding API endpoint for postal code lookup
def geocode_view(request):
    """
    API endpoint to geocode Japanese postal codes to coordinates and display area.
    Returns JSON with latitude, longitude, and display_area.
    """
    if request.method != 'GET':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    postal_code = request.GET.get('postal_code', '').strip().replace('-', '').replace(' ', '')
    
    # Validate postal code (7 digits)
    if not postal_code or len(postal_code) != 7 or not postal_code.isdigit():
        return JsonResponse({
            'success': False,
            'error': '郵便番号は7桁の数字で入力してください。'
        }, status=400)
    
    try:
        # Step 1: Get address from postal code using ZipCloud API
        zipcloud_url = f'https://zipcloud.ibsnet.co.jp/api/search?zipcode={postal_code}'
        zipcloud_response = requests.get(zipcloud_url, timeout=10)
        
        if zipcloud_response.status_code != 200:
            return JsonResponse({
                'success': False,
                'error': '郵便番号APIへの接続に失敗しました。'
            }, status=500)
        
        zipcloud_data = zipcloud_response.json()
        
        # Check if results found
        if zipcloud_data.get('status') != 200 or not zipcloud_data.get('results'):
            return JsonResponse({
                'success': False,
                'error': '郵便番号が見つかりませんでした。正しい郵便番号を入力してください。'
            }, status=404)
        
        result = zipcloud_data['results'][0]
        prefecture = result.get('prefecture', '')  # 都道府県
        city = result.get('address1', '')  # 市区町村
        area = result.get('address2', '')  # 町域
        address3 = result.get('address3', '')  # その他
        
        # Build display area string (Japanese format)
        display_parts = [prefecture, city, area]
        if address3:
            display_parts.append(address3)
        display_area = ' '.join(filter(None, display_parts))
        
        # Build full address for geocoding
        full_address = f'{prefecture}{city}{area}'
        if address3:
            full_address += address3
        
        # Step 2: Geocode address to coordinates using Nominatim
        nominatim_url = 'https://nominatim.openstreetmap.org/search'
        nominatim_params = {
            'q': full_address,
            'format': 'json',
            'limit': 1,
            'countrycodes': 'jp',
            'accept-language': 'ja'
        }
        nominatim_headers = {
            'User-Agent': 'KindredSpace/1.0'  # Required by Nominatim
        }
        
        nominatim_response = requests.get(nominatim_url, params=nominatim_params, headers=nominatim_headers, timeout=10)
        
        if nominatim_response.status_code != 200:
            return JsonResponse({
                'success': False,
                'error': '座標の取得に失敗しました。'
            }, status=500)
        
        nominatim_data = nominatim_response.json()
        
        if not nominatim_data or len(nominatim_data) == 0:
            return JsonResponse({
                'success': False,
                'error': '座標が見つかりませんでした。'
            }, status=404)
        
        location = nominatim_data[0]
        latitude = float(location.get('lat', 0))
        longitude = float(location.get('lon', 0))
        
        # Return success response
        return JsonResponse({
            'success': True,
            'latitude': latitude,
            'longitude': longitude,
            'display_area': display_area
        })
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'success': False,
            'error': f'ネットワークエラーが発生しました: {str(e)}'
        }, status=500)
    except (KeyError, ValueError, IndexError) as e:
        return JsonResponse({
            'success': False,
            'error': f'データの処理中にエラーが発生しました: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'予期しないエラーが発生しました: {str(e)}'
        }, status=500)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    tab = request.GET.get('tab', 'giving')
    
    if tab == 'giving':
        posts = user.posts.filter(post_type='GIVE').order_by('-created_at')
    elif tab == 'requesting':
        posts = user.posts.filter(post_type='REQUEST').order_by('-created_at')
    elif tab == 'history':
        posts = user.posts.all().order_by('-created_at')
    else:
        posts = user.posts.filter(post_type='GIVE').order_by('-created_at')
    
    all_reviews = Review.objects.filter(reviewee=user).select_related('reviewer').order_by('-created_at')
    review_count = all_reviews.count()
    reviews = all_reviews[:10]
    
    can_review = request.user.is_authenticated and request.user != user
    has_reviewed = False
    if can_review:
        has_reviewed = Review.objects.filter(reviewer=request.user, reviewee=user).exists()
    
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    
    followers_count = Follow.objects.filter(following=user).count()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'current_tab': tab,
        'reviews': reviews,
        'review_count': review_count,
        'can_review': can_review,
        'has_reviewed': has_reviewed,
        'is_following': is_following,
        'followers_count': followers_count,
    }
    
    return render(request, 'a_posts/profile.html', context)


@login_required
def submit_review_view(request, username):
    reviewee = get_object_or_404(User, username=username)
    
    if request.user == reviewee:
        messages.error(request, '自分自身をレビューすることはできません。')
        return redirect('profile', username=username)
    
    existing_review = Review.objects.filter(reviewer=request.user, reviewee=reviewee, post__isnull=True).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, 'レビューを投稿しました！')
            return redirect('profile', username=username)
    
    return redirect('profile', username=username)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    next_url = request.POST.get('next') or request.GET.get('next')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                UserProfile.objects.get_or_create(user=user)
                messages.success(request, f'{username}さん、おかえりなさい！')
                
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                    return redirect(next_url)
                return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'a_posts/login.html', {'form': form, 'next': next_url})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'{user.username}さん、KindredSpaceへようこそ！')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'a_posts/signup.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'ログアウトしました。')
        return redirect('home')
    return redirect('home')


@login_required
def toggle_follow_view(request, username):
    if request.method != 'POST':
        return redirect('profile', username=username)
    
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        messages.error(request, '自分自身をフォローすることはできません。')
        return redirect('profile', username=username)
    
    follow_relation = Follow.objects.filter(follower=request.user, following=user_to_follow).first()
    
    if follow_relation:
        follow_relation.delete()
        messages.success(request, f'{user_to_follow.username}さんのフォローを解除しました。')
    else:
        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f'{user_to_follow.username}さんをフォローしました！')
    
    return redirect('profile', username=username)