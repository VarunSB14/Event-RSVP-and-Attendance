# Event RSVP and Attendance App

## Description

The Event RSVP and Attendance App is a web-based application that allows users to browse, RSVP, and manage events. Organizers can create, edit, and delete events, while attendees can RSVP for events and view their RSVP'd event details.

The app uses a **React frontend** with **Flask** as the backend and **PostgreSQL** as the database.

---

## Features

### User Features

- **Registration/Login**: Users can sign up, log in, and log out securely.
- **Event Browsing**: View a list of available events with details like date, time, location, and availability.
- **RSVP**: RSVP to events and manage attendance status.
- **User Profile**: View RSVP'd events in a personalized user profile.

### Organizer Features

- **Event Management**: Create, edit, or delete events.
- **View Attendees**: View a list of attendees for each event.

---

## Technologies Used

### Frontend

- **React**: User interface and client-side functionality.
- **Reactstrap**: UI components for a modern look and feel.
- **CSS**: Styling for all pages.

### Backend

- **Flask**: RESTful API to handle server-side operations.
- **Flask-RESTful**: For structured API development.
- **PostgreSQL**: Database for event, user, and RSVP management.

---

## Installation and Setup

### Prerequisites

- Python 3.x
- Node.js
- PostgreSQL

### Backend Setup

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd backend
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    - Create a PostgreSQL database.
    - Execute the provided `data.sql` file to initialize tables and seed data:

        ```bash
        psql -U <username> -d <database_name> -f data.sql
        ```

4. Start the Flask server:

    ```bash
    python server.py
    ```

### Frontend Setup

1. Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the React development server:

    ```bash
    npm start
    ```

4. Open your browser and navigate to:

    ```
    http://localhost:3000
    ```

---

## API Endpoints

### **Authentication:**

- `POST /api/login`: Authenticate a user.

### **Users:**

- `GET /api/users/<user_id>`: Fetch user details and RSVP'd events.
- `POST /api/users`: Register a new user.

### **Events:**

- `GET /api/events`: Fetch all events.
- `POST /api/events`: Create a new event.
- `GET /api/events/<event_id>`: Fetch details of a specific event.
- `PUT /api/events/<event_id>`: Update an event.
- `DELETE /api/events/<event_id>`: Delete an event.

### **RSVP:**

- `GET /api/events/<event_id>/rsvp`: Fetch attendees for an event.
- `POST /api/events/<event_id>/rsvp`: RSVP to an event.
- `PUT /api/events/<event_id>/rsvp`: Update RSVP status.

---

## File Structure

### Backend

```plaintext
backend/
├── authentication.py  # Handles user login
├── db_utils.py        # Database utility functions
├── event.py           # Event-specific API endpoints
├── events.py          # Multiple events API endpoints
├── rsvp.py            # RSVP management
├── users.py           # User management
├── data.sql           # Database schema and seed data

frontend/
├── src/
    ├── App.js            # Main app component
    ├── EventDisplay.js   # Component to display individual events
    ├── EventModal.js     # Modal for adding/editing events
    ├── Login.js          # Login form
    ├── Register.js       # Registration form
    ├── UserProfile.js    # User profile and RSVP'd events
    ├── styles.css        # Custom styling

## Usage

### As a User:
1. Register and log in to access the app.
2. Browse events, RSVP, and view your RSVP'd events in your profile.

### As an Organizer:
1. Log in with an organizer account.
2. Create, edit, and delete events.
3. View the list of attendees for your events.

---

## Future Enhancements
- **Email Notifications**: Notify users when an event they're interested in is updated.
- **Event Categories**: Add filtering by category (e.g., Workshops, Meetups, Conferences).
- **Search Functionality**: Implement a global search for events by title or description.
- **Admin Dashboard**: Advanced tools for organizers to manage events and users.

---

## Contributors
- **Varun Bharthavarapu** - Developer

