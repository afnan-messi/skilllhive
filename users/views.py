from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Activity
from skills.models import UserSkill
from reviews.models import UserReview
from django.db.models import Avg

def home(request):
    return render(request, "home.html")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Skill Exchange, {user.username}!")
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

@login_required
def dashboard_view(request):
    profile = request.user.profile
    
    # Mock data for demonstration - in a real app, these would come from the database
    matches = [
        {'username': 'Sarah_Tech', 'offer': 'Python', 'want': 'UI Design', 'img': 'https://i.pravatar.cc/150?u=sarah'},
        {'username': 'Mike_Dev', 'offer': 'React', 'want': 'Music Production', 'img': 'https://i.pravatar.cc/150?u=mike'},
        {'username': 'Elena_Art', 'offer': 'Figma', 'want': 'React', 'img': 'https://i.pravatar.cc/150?u=elena'},
    ]
    
    sessions = [
        {'skill': 'Python Basics', 'teacher': 'Sarah_Tech', 'date': 'Today, 2:00 PM'},
        {'skill': 'React Hooks', 'teacher': 'Mike_Dev', 'date': 'Tomorrow, 10:30 AM'},
    ]
    
    leaderboard = [
        {'rank': 1, 'username': 'CodeMaster', 'points': 2450},
        {'rank': 2, 'username': 'DesignPro', 'points': 2120},
        {'rank': 3, 'username': 'LearnFast', 'points': 1890},
        {'rank': 4, 'username': 'TechGuru', 'points': 1750},
        {'rank': 5, 'username': 'PyWiz', 'points': 1620},
    ]
    
    feed = [
        {'user': 'Sarah_Tech', 'action': 'completed a Python session', 'time': '5 mins ago'},
        {'user': request.user.username, 'action': 'unlocked Level ' + str(profile.level), 'time': '1 hour ago'},
        {'user': 'Mike_Dev', 'action': 'joined the platform', 'time': '2 hours ago'},
    ]
    
    from research.models import ResearchPaper, PaperReview
    papers_uploaded = ResearchPaper.objects.filter(author=request.user).count()
    reviews_given = PaperReview.objects.filter(reviewer=request.user).count()
    research_points = papers_uploaded * 20 + reviews_given * 10

    context = {
        'user': request.user,
        'profile': profile,
        'skills_offered': profile.skills_offered.split(',') if profile.skills_offered else [],
        'skills_to_learn': profile.skills_to_learn.split(',') if profile.skills_to_learn else [],
        'matches': matches,
        'sessions': sessions,
        'leaderboard': leaderboard,
        'feed': feed,
        'papers_uploaded': papers_uploaded,
        'reviews_given': reviews_given,
        'research_points': research_points,
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile_view(request):
    profile = request.user.profile
    teach_skills = UserSkill.objects.filter(user=request.user, skill_type='Teach')
    learn_skills = UserSkill.objects.filter(user=request.user, skill_type='Learn')
    
    activities = Activity.objects.filter(user=request.user)[:10]
    reviews = UserReview.objects.filter(reviewed_user=request.user)
    
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Gamification stats
    next_level_xp = profile.level * 100
    xp_progress = (profile.points % 100) if profile.points < next_level_xp else 100
    
    context = {
        'profile': profile,
        'teach_skills': teach_skills,
        'learn_skills': learn_skills,
        'activities': activities,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'total_skills': teach_skills.count(),
        'xp_progress': xp_progress,
        'next_level_xp': next_level_xp,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def matches_view(request):
    user = request.user
    
    # Get what I want to learn and what I can teach
    skills_i_want = UserSkill.objects.filter(user=user, skill_type='Learn').values_list('skill_name', flat=True)
    skills_i_want_lower = [s.lower() for s in skills_i_want]
    
    skills_i_teach = UserSkill.objects.filter(user=user, skill_type='Teach').values_list('skill_name', flat=True)
    skills_i_teach_lower = [s.lower() for s in skills_i_teach]
    
    from django.contrib.auth.models import User
    
    other_users = User.objects.exclude(id=user.id).prefetch_related('user_skills')
    matches_list = []
    
    for other_user in other_users:
        their_teach_skills = other_user.user_skills.filter(skill_type='Teach')
        their_learn_skills = other_user.user_skills.filter(skill_type='Learn')
        
        match_teach = []
        for my_want in skills_i_want_lower:
            for their_teach in their_teach_skills:
                if my_want in their_teach.skill_name.lower() or their_teach.skill_name.lower() in my_want:
                    if their_teach not in match_teach:
                        match_teach.append(their_teach)
                        
        if match_teach:
            perfect_match = False
            for my_teach in skills_i_teach_lower:
                for their_learn in their_learn_skills:
                    if my_teach in their_learn.skill_name.lower() or their_learn.skill_name.lower() in my_teach:
                        perfect_match = True
                        break
                if perfect_match:
                    break
                    
            # Calculate a basic score and get rating
            score = 100 if perfect_match else 85
            avg_rating = getattr(other_user, 'userreview_set', None) 
            if avg_rating:
                avg = avg_rating.aggregate(Avg('rating'))['rating__avg']
            else:
                avg = UserReview.objects.filter(reviewed_user=other_user).aggregate(Avg('rating'))['rating__avg']
                
            rating = round(avg, 1) if avg else 0.0

            # Safe profile picture extraction
            profile_pic_url = None
            if hasattr(other_user, 'profile') and other_user.profile and other_user.profile.profile_picture:
                profile_pic_url = other_user.profile.profile_picture.url

            matches_list.append({
                'user': other_user,
                'teach_skills': match_teach,
                'learn_skills': their_learn_skills,
                'perfect_match': perfect_match,
                'score': score,
                'rating': rating,
                'profile_pic_url': profile_pic_url
            })
            
    # Sort matches by score descending
    matches_list.sort(key=lambda x: x['score'], reverse=True)
    
    return render(request, 'matches.html', {'matches': matches_list})

from django.http import JsonResponse
import json
from .models import NQueensProgress

@login_required
def game_view(request):
    progress, created = NQueensProgress.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            if action == 'level_complete':
                level = data.get('level')
                xp_gained = data.get('xp_gained', 0)
                
                # Update progress
                progress.xp += xp_gained
                if level >= progress.level:
                    progress.level = level + 1
                progress.save()
                
                # Update global profile points too
                profile = request.user.profile
                profile.points += xp_gained
                profile.save()
                
                return JsonResponse({'status': 'success', 'new_level': progress.level, 'total_xp': progress.xp})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    context = {
        'game_level': progress.level,
        'game_xp': progress.xp,
        'profile': request.user.profile
    }
    return render(request, 'game.html', context)

@login_required
def leaderboard_view(request):
    from django.contrib.auth.models import User
    from research.models import ResearchPaper, PaperReview
    
    users = User.objects.all().select_related('profile')
    leaderboard_data = []
    
    for u in users:
        # Game XP
        try:
            game_xp = u.nqueens_progress.xp
        except:
            game_xp = 0
            
        # Research Points
        papers_uploaded = ResearchPaper.objects.filter(author=u).count()
        reviews_given = PaperReview.objects.filter(reviewer=u).count()
        research_points = papers_uploaded * 20 + reviews_given * 10
        
        # Session Points 
        session_points = getattr(u.profile, 'sessions_completed', 0) * 50
        
        total_points = game_xp + research_points + session_points
        
        profile_pic = None
        if hasattr(u, 'profile') and u.profile.profile_picture:
            profile_pic = u.profile.profile_picture.url
            
        leaderboard_data.append({
            'username': u.username,
            'profile_pic_url': profile_pic,
            'level': getattr(u.profile, 'level', 1),
            'game_xp': game_xp,
            'research_points': research_points,
            'session_points': session_points,
            'total_points': total_points,
            'is_current': u.id == request.user.id
        })
        
    total_system_points = sum(item['total_points'] for item in leaderboard_data)
    
    # Demo Data Fallback
    if total_system_points < 1000 or len(leaderboard_data) < 4:
        demo_data = [
            {'username': 'Alex_Einstein', 'profile_pic_url': 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex', 'level': 8, 'game_xp': 800, 'research_points': 500, 'session_points': 600, 'total_points': 1900, 'is_current': False},
            {'username': 'Maria_Curie', 'profile_pic_url': 'https://api.dicebear.com/7.x/avataaars/svg?seed=Maria', 'level': 7, 'game_xp': 600, 'research_points': 800, 'session_points': 400, 'total_points': 1800, 'is_current': False},
            {'username': 'David_Turing', 'profile_pic_url': 'https://api.dicebear.com/7.x/avataaars/svg?seed=David', 'level': 6, 'game_xp': 900, 'research_points': 200, 'session_points': 500, 'total_points': 1600, 'is_current': False},
            {'username': 'Sarah_Tech', 'profile_pic_url': 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah', 'level': 5, 'game_xp': 300, 'research_points': 300, 'session_points': 800, 'total_points': 1400, 'is_current': False},
            {'username': 'Mike_Dev', 'profile_pic_url': 'https://api.dicebear.com/7.x/avataaars/svg?seed=Mike', 'level': 4, 'game_xp': 400, 'research_points': 100, 'session_points': 700, 'total_points': 1200, 'is_current': False},
        ]
        existing_usernames = {item['username'] for item in leaderboard_data}
        for demo in demo_data:
            if demo['username'] not in existing_usernames:
                leaderboard_data.append(demo)
                
    # Sort leaderboard
    overall_leaderboard = sorted(leaderboard_data, key=lambda x: x['total_points'], reverse=True)
    
    # Assign ranks
    for i, item in enumerate(overall_leaderboard):
        item['rank'] = i + 1
        item['is_top3'] = i < 3
        
    game_leaderboard = sorted(leaderboard_data, key=lambda x: x['game_xp'], reverse=True)
    research_leaderboard = sorted(leaderboard_data, key=lambda x: x['research_points'], reverse=True)
    session_leaderboard = sorted(leaderboard_data, key=lambda x: x['session_points'], reverse=True)
    
    user_data = next((item for item in overall_leaderboard if item.get('is_current')), None)
    
    # Calculate points for next rank
    if user_data and user_data['rank'] > 1:
        rank_above = overall_leaderboard[user_data['rank'] - 2]
        user_data['points_needed'] = rank_above['total_points'] - user_data['total_points'] + 1
    else:
        if user_data:
            user_data['points_needed'] = 0

    context = {
        'overall_leaderboard': overall_leaderboard,
        'game_leaderboard': game_leaderboard,
        'research_leaderboard': research_leaderboard,
        'session_leaderboard': session_leaderboard,
        'user_data': user_data,
        'top_3': overall_leaderboard[:3],
    }
    return render(request, 'leaderboard.html', context)

def how_it_works_view(request):
    return render(request, "how_it_works.html")

def about_view(request):
    return render(request, "about.html")

def privacy_view(request):
    return render(request, "privacy.html")

def terms_view(request):
    return render(request, "terms.html")

def careers_view(request):
    return render(request, "careers.html")

@login_required
def skills_view(request):
    return redirect('skills_page')

@login_required
def matching_view(request):
    return redirect('matches')

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            from .models import NewsletterSubscriber
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, "Successfully joined our newsletter!")
        else:
            messages.error(request, "Invalid email address.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


