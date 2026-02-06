# KindredSpace - Community Sharing Platform

## Overview
KindredSpace is a Django-based web application designed as a Japanese community sharing platform. Its core purpose is to facilitate the giving and requesting of items or skills among users without monetary exchange. The platform incorporates location-based functionalities using Japanese postal codes and geocoding, aiming to foster local community engagement and resource sharing. It includes robust user profiles with dynamic reputation scores, peer-to-peer rating systems, and a focus on intuitive Japanese-language UI.

## Recent Changes (February 2026)
- Request vs Give mode differentiation in post creation:
  - Dynamic placeholders for title/body based on post type (GIVE vs REQUEST)
  - Request-only fields: acceptable_condition (multi-select chips), urgency dropdown, deadline_date picker
  - Conditional image requirements: 2-4 required for GIVE, 0-4 optional for REQUEST
  - Alpine.js postTypeManager component with data-attribute hydration for form state persistence
  - clearRequestFields() prevents data leakage when switching from REQUEST to GIVE mode
  - Post model updated with acceptable_condition, urgency, deadline_date fields
- Improved image upload UI in post creation form:
  - Custom drag-and-drop upload zone with modern styling
  - Thumbnail previews with individual delete buttons
  - Image count display with validation status
  - Uses DataTransfer API to manage file list for individual removal

## Previous Changes (January 2026)
- Redesigned post detail page (post_page.html) with Swiper.js image gallery, owner info section, chat/edit buttons
- Real-time chat system: ChatRoom and Message models, polling-based updates (2-second interval), message bubbles UI
- Multi-image upload system: PostImage model with order field, 2-4 images per GIVE post, Swiper.js gallery
- Simplified post creation location: Prefecture dropdown, Nominatim autocomplete, auto lat/lng capture
- Real-time notification system: bell icon with unread count badge (polls every 30 seconds), type-specific badges

## Previous Changes (December 2024)
- Streamlined location filtering to one-click operation
- Mobile-responsive location button with unified green styling
- Fixed header button layout shift using min-width and x-cloak
- User-editable display_area field in post creation

## User Preferences
I prefer iterative development with clear, concise explanations for each step. Please ensure that all new features and modifications are well-documented. I value clean code and maintainable solutions. Before making any major architectural changes or introducing new external dependencies, please ask for my approval. Ensure all user-facing text is in Japanese where appropriate. I prefer detailed explanations for complex features.

## System Architecture

### UI/UX Decisions
The platform features an eco-friendly green color scheme (#4CAF50) as the primary brand color, used for buttons, forms, and accents, while the header is a clean off-white (bg-gray-50) for a professional look. The header implements a unified green button aesthetic with clear visual hierarchy: the search button features green background with white text and rounded-r-lg corners, Create Post is styled as a primary CTA button with green background and white text, and Home is a secondary green text link with bold font-weight.

The home page uses a JMTY-inspired responsive grid layout displaying posts as minimal cards. The grid adapts from 3 columns on desktop (lg), 2 columns on tablet (md), to 1 column on mobile. Each post card features a 4:3 aspect ratio image with an overlaid post type badge, clickable title with line-clamp truncation, and prominent location display using the display_area field.

It includes responsive design for all components, an auto-hiding header on scroll, and dynamic hero background carousels with pagination using Swiper.js. User profiles are professionally redesigned with enlarged photos, prominent names, enhanced statistics, and gradient trust metric bars.

Mobile-Responsive Location Button:
- Desktop: Full text button with location icon, unified green styling
- Mobile: Icon-only button beside logo, same green styling for visual consistency
- Both use x-cloak to prevent layout shifts during Alpine.js initialization
- Clear filter button appears when location filter is active

### Technical Implementations
- Backend: Django 5.2.6 (Python 3.12)
- Frontend: HTML templates with Tailwind CSS (via CDN)
- Database: SQLite (development)
- Image Handling: Pillow for image uploads and processing
- Authentication: Custom authentication system with Japanese-language login/signup pages, secure logout, and next parameter handling for redirects
- User Profiles: Comprehensive UserProfile model with fields for profile picture, bio, dynamic reputation_score, total_contributions, success_rate, location_display, is_verified, and followers_count. Includes a bulletproof profile safety system using context processors and template filters to prevent RelatedObjectDoesNotExist errors
- Peer-to-Peer Rating: Review model for 1-5 star ratings and comments, automatically calculating user reputation scores
- Follow System: Follow model implementing follower/following relationships with dynamic count calculation and a toggle follow/unfollow view
- Posts: Users can create GIVE (offering) or REQUEST (seeking) posts with image uploads, location data (Japanese postal codes), and a tag/category system. Posts display visual badges for type and link to user profiles. The display_area field is user-editable for custom location descriptions. REQUEST posts support additional fields: acceptable_condition (multi-select), urgency level, and deadline_date
- Multi-Image Upload: PostImage model stores 2-4 images per post with order field. GIVE posts require 2-4 images; REQUEST posts allow 0-4 images optionally. Swiper.js gallery on detail page
- Search: Functionality to search by title, body, artist, and tags
- Chat System: Polling-based messaging between users about specific posts via ChatRoom and Message models with 2-second polling interval and read status tracking
- Notification System: Automatic notifications for follows, reviews, and messages. Bell icon with unread count badge polling every 30 seconds. Notification types: follow, review, post, message, system
- Location-Based Filtering: Browser geolocation API integration with Haversine distance calculation to filter posts within a 10km radius. One-click activation button, SessionStorage persistence, distance badges, and resilient error handling

### Data Models
- Post: title, body, image (optional legacy), post_type (GIVE/REQUEST), user (FK), artist, url, reason, prefecture, latitude, longitude, display_area, show_general_area_only, tags (M2M to Tag), acceptable_condition, urgency (choices: asap/week/no_rush/custom), deadline_date
- PostImage: post (FK to Post), image, order, created_at
- Tag: name, slug
- UserProfile: user (OneToOne to User), profile_picture, bio, reputation_score, total_contributions, success_rate, location_display, is_verified, followers_count, created_at, updated_at
- Review: reviewer (FK User), reviewee (FK User), rating (1-5), comment, post (FK), created_at, updated_at
- Follow: follower (FK User), following (FK User), created_at (unique_together: follower+following)
- Notification: recipient (FK User), sender (FK User, nullable), notification_type (follow/review/post/message/system), message, is_read, link, created_at
- ChatRoom: post (FK), participant1 (FK User - post owner), participant2 (FK User - initiator), created_at, updated_at
- Message: chat_room (FK ChatRoom), sender (FK User), content, is_read, created_at

### URL Routes
- / -> home_view (home) - Home page with post grid and hero
- /login/ -> login_view (login) - User login page
- /signup/ -> signup_view (signup) - User registration page
- /logout/ -> logout_view (logout) - User logout
- /posts/create/ -> post_create_view (post-create) - Create new post
- /posts/<pk> -> post_page_view (post) - Post detail page
- /posts/edit/<pk> -> post_eidt_view (post-edit) - Edit post
- /posts/delete/<pk> -> post_delete_view (post-delete) - Delete post
- /users/<username>/ -> profile_view (profile) - User profile page
- /users/<username>/review/ -> submit_review_view (submit-review) - Submit user review
- /users/<username>/follow/ -> toggle_follow_view (toggle-follow) - Toggle follow/unfollow
- /notifications/ -> notifications_view (notifications) - Notifications list
- /api/notifications/unread-count/ -> notifications_unread_count_view - API: unread notification count
- /notifications/<id>/read/ -> notification_mark_read_view - Mark notification as read
- /chat/<post_id>/ -> chat_room_view (chat_room) - Open/create chat for a post
- /chat/room/<room_id>/ -> chat_messages_view (chat_messages) - View chat room messages
- /chat/room/<room_id>/api/ -> chat_messages_api (chat_messages_api) - API: poll chat messages
- /chats/ -> chat_list_view (chat_list) - All user conversations
- /api/geocode -> geocode_view (geocode) - Geocoding API endpoint
- /presentation/ -> TemplateView (presentation) - Presentation page
- /admin/ -> Django Admin

### Feature Specifications
- User authentication with Japanese UI (login, signup, logout)
- User profiles with community metrics, trust scores, and activity tabs
- Peer-to-peer rating system with dynamic reputation scores (1-5 stars)
- Post creation with GIVE/REQUEST mode differentiation, multi-image uploads, location, and privacy options
- Multi-image upload (2-4 for GIVE, 0-4 for REQUEST) with drag-and-drop UI
- Request-specific fields: acceptable condition chips, urgency level, deadline date
- Search functionality by title, body, artist, and tags
- Follow/unfollow system for users
- Polling-based chat messaging system for post inquiries (2-second interval)
- Polling-based notification system with automatic triggers for follows, reviews, and messages (30-second interval)
- One-click location filtering with mobile-responsive design (10km radius)
- Custom 404 error page

### System Design Choices
- Configured for Replit compatibility with 0.0.0.0:5000 for the development server and ALLOWED_HOSTS = ['*']
- Deployment configured for Autoscale with Gunicorn
- Uses LOGIN_URL and LOGIN_REDIRECT_URL for custom authentication flow
- Context processors (a_posts/context_processors.py) and template filters (a_posts/templatetags/profile_tags.py) ensure safe access to user profiles and post owners
- Uses x-cloak and min-width utilities to prevent layout shifts during Alpine.js initialization
- All URL routes are centralized in a_core/urls.py (no app-level urls.py)

## External Dependencies
- ZipCloud API: Used for Japanese postal code lookup
- Nominatim/OpenStreetMap: Used for geocoding services (free, no API key)
- Swiper.js: Hero background carousels and image gallery (via CDN)
- Alpine.js: Dynamic UI behaviors - auto-hiding header, location filtering, post type switching, form state management (via CDN)
- Tailwind CSS: Utility-first CSS framework (via CDN)
- Python Packages (requirements.txt):
  - Django 5.2.6
  - Pillow 11.1.0
  - beautifulsoup4 4.12.3
  - requests 2.32.3
  - gunicorn 23.0.0

## Project File Structure

### Backend (Python/Django)
- manage.py - Django management script
- create_demo_user.py - Script to create demo user data
- a_core/settings.py - Django project settings
- a_core/urls.py - All URL route definitions
- a_core/wsgi.py - WSGI application entry point
- a_core/asgi.py - ASGI application entry point
- a_posts/models.py - All data models (Post, PostImage, Tag, UserProfile, Review, Follow, Notification, ChatRoom, Message)
- a_posts/views.py - All view functions (home, auth, posts, profiles, chat, notifications, geocoding)
- a_posts/forms.py - Post creation/edit forms
- a_posts/admin.py - Django admin configuration
- a_posts/apps.py - App configuration
- a_posts/prefectures.py - Japanese prefecture constants (47 prefectures)
- a_posts/context_processors.py - Template context processors for safe profile access
- a_posts/templatetags/profile_tags.py - Custom template filters for profile safety

### Templates
- templates/base.html - Root base template
- templates/layouts/a.html - Layout variant A
- templates/layouts/b.html - Layout variant B
- templates/layouts/simple.html - Simple layout (for auth pages)
- templates/includes/header.html - Main header with location button, search, navigation, notification bell
- templates/includes/hero.html - Hero carousel section
- templates/includes/sidebar.html - Sidebar component
- templates/includes/messages.html - Django messages display
- templates/a_posts/home.html - Home page with hero carousel and post grid
- templates/a_posts/post_grid_item.html - Individual post card component
- templates/a_posts/post_page.html - Post detail page with gallery, owner info, and chat button
- templates/a_posts/post_create.html - Post creation form with GIVE/REQUEST mode and Nominatim autocomplete
- templates/a_posts/post_edit.html - Post edit form
- templates/a_posts/post_delete.html - Post deletion confirmation
- templates/a_posts/post.html - Simple post view
- templates/a_posts/profile.html - User profile page with stats, reviews, and follow
- templates/a_posts/login.html - Login page (Japanese UI)
- templates/a_posts/signup.html - Registration page (Japanese UI)
- templates/a_posts/chat_room.html - Chat messaging interface (polling-based)
- templates/a_posts/chat_list.html - Post-specific inquiry list for owners
- templates/a_posts/chat_list_all.html - All conversations list
- templates/a_posts/notifications.html - Notifications list page
- templates/presentation.html - Presentation/showcase page
- templates/404.html - Custom 404 error page
