from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserSkillForm
from .models import UserSkill
from users.models import Activity

@login_required
def skills_page(request):
    categories = [
        {'name': 'Programming', 'icon': 'fas fa-code', 'count': 120},
        {'name': 'Design', 'icon': 'fas fa-palette', 'count': 85},
        {'name': 'Languages', 'icon': 'fas fa-language', 'count': 64},
        {'name': 'Music', 'icon': 'fas fa-music', 'count': 42},
        {'name': 'Cooking', 'icon': 'fas fa-utensils', 'count': 38},
        {'name': 'Marketing', 'icon': 'fas fa-bullhorn', 'count': 56},
        {'name': 'Photography', 'icon': 'fas fa-camera', 'count': 29},
        {'name': 'Business', 'icon': 'fas fa-briefcase', 'count': 72},
    ]

    marketplace_skills = [
        {'name': 'Advanced Python', 'user': 'John Doe', 'level': 'Advanced', 'rating': 4.9},
        {'name': 'UI/UX Fundamentals', 'user': 'Jane Smith', 'level': 'Intermediate', 'rating': 4.7},
        {'name': 'Public Speaking 101', 'user': 'Mike Ross', 'level': 'Beginner', 'rating': 4.5},
        {'name': 'Digital Marketing', 'user': 'Sarah Connor', 'level': 'Intermediate', 'rating': 4.8},
        {'name': 'React Development', 'user': 'David Webb', 'level': 'Advanced', 'rating': 5.0},
        {'name': 'Piano for Beginners', 'user': 'Alice Cooper', 'level': 'Beginner', 'rating': 4.6},
        {'name': 'Data Visualization', 'user': 'Bob Vance', 'level': 'Intermediate', 'rating': 4.7},
        {'name': 'French Conversation', 'user': 'Amelie Poulain', 'level': 'Advanced', 'rating': 4.9},
    ]

    matches = [
        {
            'user': 'Alex Johnson',
            'role': 'Senior Designer',
            'offer': 'Graphic Design',
            'want': 'Python',
            'score': 92,
            'color': '00d2ff'
        },
        {
            'user': 'Sarah Lee',
            'role': 'Data Scientist',
            'offer': 'Machine Learning',
            'want': 'Web Development',
            'score': 88,
            'color': '9d50bb'
        }
    ]

    trending_skills = [
        {'name': 'AI / Machine Learning', 'count': '1.2k+', 'icon': 'fas fa-fire', 'class': 'text-danger'},
        {'name': 'UI/UX Design', 'count': '850', 'icon': 'fas fa-chart-line', 'class': 'text-success'},
        {'name': 'Public Speaking', 'count': '420', 'icon': 'fas fa-microphone', 'class': 'text-info'},
        {'name': 'Video Editing', 'count': '630', 'icon': 'fas fa-video', 'class': 'text-warning'},
    ]

    context = {
        'categories': categories,
        'marketplace_skills': marketplace_skills,
        'matches': matches,
        'trending_skills': trending_skills,
    }
    return render(request, 'skills.html', context)

@login_required
def add_skill_view(request):
    if request.method == 'POST':
        form = UserSkillForm(request.POST, request.FILES)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            
            # Update user points
            profile = request.user.profile
            profile.points += 10
            profile.save()
            
            # Log activity
            Activity.objects.create(
                user=request.user,
                action=f"Added {skill.skill_name} as a {skill.skill_type} skill"
            )
            
            return redirect('profile')
    else:
        form = UserSkillForm()
    
    return render(request, 'add_skill.html', {'form': form})
