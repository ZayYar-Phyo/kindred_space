# KindredSpace - Community Sharing Platform

## Overview
KindredSpace is a Django-based web application designed as a Japanese community sharing platform. Its core purpose is to facilitate the giving and requesting of items or skills among users without monetary exchange. The platform incorporates location-based functionalities using Japanese postal codes and geocoding, aiming to foster local community engagement and resource sharing. It includes robust user profiles with dynamic reputation scores, peer-to-peer rating systems, and a focus on intuitive Japanese-language UI.

## Recent Changes (January 2026)
- Simplified post creation location system:
  - Prefecture dropdown with all 47 Japanese prefectures
  - Location autocomplete using OpenStreetMap Nominatim API (free, no API key)
  - Removed map display and "Use current location" button for cleaner form
  - Lat/lng coordinates captured automatically from autocomplete selection
- Added real-time notification system with bell icon in header
- Notification model with automatic triggers for follow and review events
- Bell icon shows unread count badge (polls every 30 seconds)
- Notifications page displays avatars, messages, and relative timestamps in Japanese
- Type-specific colored badges (follow/review/post/system)
- Mark-as-read functionality on page visit

## Previous Changes (December 2024)
- Streamlined location filtering to one-click operation (removed modal for seamless UX)
- Implemented mobile-responsive location button (icon-only beside logo with unified green styling)
- Fixed header button layout shift using min-width and x-cloak for Alpine.js initialization
- Made post creation form's display_area field user-editable for customization
- Unified green button styling across mobile and desktop (bg-primary, hover:bg-primary-dark)
- Enhanced debugging infrastructure with comprehensive frontend and backend logging

## User Preferences
I prefer iterative development with clear, concise explanations for each step. Please ensure that all new features and modifications are well-documented. I value clean code and maintainable solutions. Before making any major architectural changes or introducing new external dependencies, please ask for my approval. Ensure all user-facing text is in Japanese where appropriate. I prefer detailed explanations for complex features.

## System Architecture

### UI/UX Decisions
The platform features an eco-friendly green color scheme (#4CAF50) as the primary brand color, used for buttons, forms, and accents, while the header is a clean off-white (bg-gray-50) for a professional look. The header implements a unified green button aesthetic with clear visual hierarchy: the "検索" (Search) button features green background with white text and rounded-r-lg corners, "Create Post" is styled as a primary CTA button with green background and white text, and "Home" is a secondary green text link with bold font-weight. All navigation elements use proper spacing with gap-6 utilities for consistent layout. The search bar uses a flex container layout creating a seamless, unified component where the input field and "検索" button share a single border with inset shadow styling. The button integrates perfectly into the right side of the search container using rounded-r-lg, while the input uses transparent background to blend seamlessly. The entire search component displays a focus ring when active using focus-within.

The home page uses a JMTY-inspired responsive grid layout displaying posts as minimal cards. The grid adapts from 3 columns on desktop (lg), 2 columns on tablet (md), to 1 column on mobile. Each post card features a 4:3 aspect ratio image with an overlaid post type badge (提供/依頼), clickable title with line-clamp truncation, and prominent location display using the `display_area` field (e.g., "大阪市 淀川区"). Cards maintain uniform heights and provide a clean, scannable interface focused on essential information - full details appear when users click through to individual post pages.

It includes responsive design for all components, an auto-hiding header on scroll, and dynamic hero background carousels with pagination using Swiper.js. User profiles are professionally redesigned with enlarged photos, prominent names, enhanced statistics, and gradient trust metric bars.

**Mobile-Responsive Location Button:**
- Desktop: Full text button "現在地を使用" with location icon, unified green styling (bg-primary hover:bg-primary-dark)
- Mobile: Icon-only button beside logo (md:hidden), same green styling for visual consistency
- Both use x-cloak to prevent layout shifts during Alpine.js initialization
- Clear filter button (✕) appears when location filter is active

### Technical Implementations
- **Backend**: Django 5.2.6 (Python 3.12)
- **Frontend**: HTML templates with Tailwind CSS
- **Database**: SQLite (development)
- **Image Handling**: Pillow for image uploads.
- **Authentication**: Custom authentication system with Japanese-language login/signup pages, secure logout, and `next` parameter handling for redirects.
- **User Profiles**: Comprehensive `UserProfile` model with fields for profile picture, bio, dynamic `reputation_score`, `total_contributions`, `success_rate`, `location_display`, `is_verified`, and `followers_count`. Includes a bulletproof profile safety system using context processors and template filters to prevent `RelatedObjectDoesNotExist` errors.
- **Peer-to-Peer Rating**: `Review` model for 1-5 star ratings and comments, automatically calculating user reputation scores.
- **Follow System**: `Follow` model implementing follower/following relationships with dynamic count calculation and a toggle follow/unfollow view.
- **Posts**: Users can create GIVE (offering) or REQUEST (seeking) posts with image uploads, location data (Japanese postal codes), and a tag/category system. Posts display visual badges for type and link to user profiles. The display_area field is user-editable for custom location descriptions.
- **Search**: Functionality to search by title, body, artist, and tags.
- **Location-Based Filtering**: Browser geolocation API integration with Haversine distance calculation to filter posts within a 10km radius. Features include:
  - One-click "現在地を使用" button (no modal, direct activation)
  - Mobile icon-only button beside logo with unified green styling
  - SessionStorage persistence for location preferences across sessions
  - Dynamic UI indicator showing active filter with clear button (✕)
  - Backend filtering using Haversine formula with Decimal-to-float conversion
  - Resilient error handling (per-post validation, graceful fallbacks)
  - Posts sorted by distance (closest first) with distance badges
  - Supports valid 0.0 coordinates (equator/prime meridian)

### Feature Specifications
- User authentication with Japanese UI.
- User profiles with community metrics, trust scores, and activity tabs.
- Peer-to-peer rating system with dynamic reputation scores.
- Post creation with image uploads, location, and privacy options.
- Search functionality.
- Follow/unfollow system for users.
- Custom authentication pages (`/login/`, `/signup/`, `/logout/`).
- One-click location filtering with mobile-responsive design.
- Real-time notification system with automatic triggers for follows and reviews.

### System Design Choices
- Configured for Replit compatibility with `0.0.0.0:5000` for the development server and `ALLOWED_HOSTS = ['*']`.
- Deployment configured for Autoscale with Gunicorn.
- Uses `LOGIN_URL` and `LOGIN_REDIRECT_URL` for custom authentication flow.
- Context processors and template filters ensure safe access to user profiles and post owners, preventing errors.
- Uses x-cloak and min-width utilities to prevent layout shifts during Alpine.js initialization.

## External Dependencies
- **ZipCloud API**: Used for Japanese postal code lookup.
- **Nominatim/OpenStreetMap**: Used for geocoding services.
- **Swiper.js**: Integrated for hero background carousels.
- **Alpine.js**: Used for dynamic UI behaviors like the auto-hiding header and location filtering.
- **Python Packages**:
    - Django 5.2.6
    - Pillow 11.1.0
    - beautifulsoup4 4.12.3
    - requests 2.32.3
    - gunicorn 23.0.0

## Key Files
- `templates/includes/header.html` - Main header with location button, search, navigation, notification bell
- `templates/a_posts/home.html` - Home page with hero carousel and post grid
- `templates/a_posts/post_grid_item.html` - Individual post card component
- `templates/a_posts/post_create.html` - Post creation form with Nominatim autocomplete
- `templates/a_posts/notifications.html` - Notifications list page
- `a_posts/views.py` - Post views including location filtering and notifications logic
- `a_posts/models.py` - Post, Notification, and related models
- `a_posts/forms.py` - Post creation/edit forms
- `a_posts/prefectures.py` - Japanese prefecture constants (47 prefectures)
