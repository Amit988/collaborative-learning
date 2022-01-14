from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path("", views.index, name="index"),

    path("members/", views.allMem, name="members"),

    path("addmem/<int:mem_id>/<int:club_id>/", views.addmem, name="addmem"),

    path("Your-club-members/<int:id>/", views.clubMembers, name="Your-club-members"),
    path("Your-club_members/<int:id>/", views.club_Members, name="Your-club_members"),
    path("tasks/", views.tasks, name="tasks"),

    path("tasks/taskmsg/<str:tag_name>/", views.taskmsg, name="taskmsg"),

    path("member-info/<int:member_id>/", views.memberinfo, name="member-info"),

    path("remove/<int:mem_id>/<int:club_id>/", views.removemem, name="remove"),

    path("taskform/", views.taskform, name="taskform"),
   # path("taskstatus/<int:task_id>/", views.taskstatus, name="taskstatus"),

    path("password_reset/", views.emailtesting, name="password_reset"),

    path("recent-tasks/", views.recentTasks,  name="recent-tasks"),
    path("update-task/<slug:pk>/<int:club_id>/", views.TaskUpdate, name="update-task"),
    path("delete-task/<slug:pk>/<int:club_id>/", views.TaskDelete, name="delete-task"),
    path("task-chat/<int:task_id>/<int:club_id>/", views.taskChat, name = "task-chat"),

    path("task-details/<int:task_id>/", views.taskDetails, name="task-details" ),
    path("your-club/<int:club_id>/", views.club, name="your-club"),
    path("we-love-your-feedbacks/", views.feedbackForm, name="feedback"),
    path("club-registration/", views.clubRegistration, name="club-registration"),
    path("info/<str:username>/", views.info, name="info"),
    path("club-by-tag/<str:tag>/", views.clubTag, name="club-tag"),

    path("leave-club/<int:club_id>/", views.leaveclub, name="leave-club"),

    path("club-discussion/<int:club_id>/", views.club_discussion, name = "club-discussion"),
    path("view-club/<int:club_id>/", views.view_club, name = "view-club"),
    path("join-club/<int:club_id>/", views.join_club, name = "join-club"),
    path("Waiting-Area/<int:club_id>/", views.view_waitingarea, name = "view-waitingarea"),

    path("jsecs/<int:club_id>/<int:mem_id>/", views.make_jsec, name = "make-jsec"),
    path("teach-on-cosb/", views.content_creators, name = "teach-on-cosb"),
    path("report-club/<int:club_id>/", views.report_club, name = "report-club"),
    path("stories/", views.stories, name = "stories"),
    path("add-story/", views.add_story, name = "add-story"),
    path("view-story/<int:story_id>/", views.view_story, name = "view-story"),
    path("delete-story/<int:story_id>/", views.delete_story, name = "delete-story"),
    path("update-story/<int:story_id>/", views.update_story, name = "update-story"),

    path("edit-club/<int:pk>/", views.EditClub, name = "edit-club"),

]