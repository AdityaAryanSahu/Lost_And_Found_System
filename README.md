# Lost & Found Inventory

A full-stack application developed for seamlessly managing and recovering lost items across the college campus. Built with **React**, **FastAPI**, and **MongoDB**, the system provides a comprehensive item catalog with secure user authentication, a smart AI-driven matching engine, claim management, and automated email notifications.

***

## Features

-  **Smart Matching Engine** - Automated background algorithm that calculates match probabilities between lost and found items.
-  **Automated Email Notifications** - Real-time, responsive HTML email alerts powered by Resend for high-confidence matches and claim updates.
-  **Comprehensive Item Catalog** - Browse, search, and filter items by category, date, and status (Lost/Found/Claimed).
-  **Secure Claim System** - Finders can review detailed justifications submitted by users attempting to claim found items (Approve/Reject workflow).
-  **In-App Messaging** - Secure direct communication between users to coordinate item handoffs without exposing private contact details.
-  **Personalized Dashboard** - Dedicated interface to manage personal uploads, review incoming claims, and track match statuses.
-  **Premium Responsive Design** - A modern, dark-themed Glassmorphism UI with gold accents and smooth CSS animations, optimized for both desktop and mobile.

***

## Tech Stack

**Frontend:**

- React (UI Library)
- React Router (Navigation)
- CSS3 (Custom Glassmorphism styling)

**Backend:**

- FastAPI (Modern Python web framework)
- MongoDB (NoSQL Database)
- Pydantic (Data validation)
- Resend API (Email notification service)
- CloudFare R2 (Image storage)

***

## How It Works

1. **Report Items**: Students securely log in and upload details (category, location, images) of items they have lost or found.
2. **Smart Matching**: The backend engine continuously scans new and existing database entries to calculate match probabilities.
3. **Automated Alerts**: When a high-confidence match (e.g., >65%) is detected, the system instantly emails both parties to review the match.
4. **Verification & Claims**: Users looking for lost items can submit formal claim justifications to the finders.
5. **Resolution**: Finders review claims on their dashboard, approve them, and coordinate the physical return via the integrated messaging system.

***

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/AdityaAryanSahu/lost_and_found_portal.git
cd lost_and_found_portal
```

### 2. Backend Setup

```bash
cd my_app
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate   # On macOS/Linux

pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in your backend directory and set up your MongoDB and Resend API keys:

```bash
DATABASE_URL="mongodb+srv://user:password@cluster.mongodb.net/lost_and_found"
RESEND_API_KEY="re_your_api_key_here"
```

### 4. Run Backend Server

```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Frontend Setup

```bash
cd ../frontend
npm install
npm run dev   # For development
# or
npm run build   # For production
```

***

## API Endpoints

**Authentication**
- `POST /auth/register` - Register a new user account
- `POST /auth/login` - Authenticate user and receive access tokens
- `POST /auth/refresh` - Refresh authentication token

**Items**
- `POST /items/` - Create a new item listing (Lost or Found)
- `GET /items/` - Retrieve and list all items
- `GET /items/{item_id}` - Retrieve details of a specific item
- `PUT /items/{item_id}` - Update a specific item's details
- `DELETE /items/{item_id}` - Delete a specific item
- `PATCH /items/{item_id}/claim` - Mark an item as claimed or recovered

**Claims**
- `POST /claims/` - Submit a formal claim for a found item
- `GET /claims/item/{item_id}` - Retrieve all claims submitted for a specific item
- `POST /claims/{claim_id}/review/{action}` - Review a claim (Approve/Reject)

**Matches**
- `POST /matches/` - Trigger or fetch all smart matches
- `GET /matches/saved/{item_id}` - Retrieve saved automated matches for a specific item

**Search**
- `POST /search/` - Advanced search endpoint for filtering items

**Messages**
- `POST /messages/send` - Send an in-app message to another user
- `GET /messages/conversations` - Retrieve all active user conversations
- `GET /messages/conversations/{conversation_id}` - Retrieve messages within a specific conversation

**System**
- `GET /health` - API health check endpoint

***

## Contributed By

**Aditya Aryan Sahu**
 [GitHub](https://github.com/AdityaAryanSahu)

**Lakshya Agarwal**
 [GitHub](https://github.com/LuckyMan22-SuperMan)

**Sheldon Rodricks**
 [GitHub](https://github.com/SheldonRodricks)

---
