# Alumni Networking Platform

A comprehensive platform built to connect students with alumni for inspiration, mentorship, and professional opportunities.

## Why This Platform Exists

As a student at BITS, I noticed there was no easy way to communicate with alumni, resulting in missed opportunities for job updates, career guidance, and motivation. This platform bridges that gap that many colleges don't address, helping students get inspired, find internships, and participate in alumni-led events.

## Features

### User Registration & Profiles
- Smooth signup process with proper validation
- Automatic profile picture resizing for consistency
- Detailed profile information to highlight skills and experience

### Job & Event Modules
- Alumni can post job opportunities and events
- Students can apply for jobs or register for events with a simple interface
- Filter and search functionality for finding relevant opportunities

### Connection System
- Send and approve connection requests to build your network
- View mutual connections and expand your professional circle
- Recommendation algorithm to suggest relevant connections

### Real-Time Messaging
- Instant chat between alumni and students
- Implemented using Django Channels and Daphne
- No page reloads required for message updates

## Tech Stack

- **Django**: Core framework chosen for its security features (CSRF tokens) and organized structure (templates for HTML, views for logic, models for database queries)
- **Python**: Primary programming language
- **HTML, Bootstrap, JavaScript**: Frontend technologies
- **Django Channels & Daphne**: Added to enable real-time messaging via WebSockets



