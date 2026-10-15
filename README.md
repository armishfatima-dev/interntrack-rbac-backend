# Interntrack RBAC Backend

A secure FastAPI backend implementing **Role-Based Access Control (RBAC)** and server-side resource ownership rules for the Interntrack program.

## Features

- **JWT Authentication**: Secure registration and login tokens (`/auth/register`, `/auth/login`).
- **Role Hierarchy**: Supports `intern`, `mentor`, and `admin` roles.
- **Server-Side Ownership & Filtering**: Interns can only access and create their own submissions; mentors and admins can view all submissions.
- **Mentor/Admin Grading**: Dedicated endpoints for grading and providing feedback.
- **Admin Management**: Role management endpoint restricted strictly to administrators.
