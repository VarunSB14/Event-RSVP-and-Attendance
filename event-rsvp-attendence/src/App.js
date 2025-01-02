import React, { Component } from 'react';
import { Container, Row, Col, Button, Input, FormGroup, Label } from 'reactstrap';
import EventDisplay from './EventDisplay';
import EventModal from './EventModal';
import UserProfile from './UserProfile';
import Register from './Register';
import Login from './Login';
import './styles.css';

class App extends Component {
  /**
  * Main application component that manages state and renders the app's main functionality.
  * Handles user login, logout, event management, and RSVP actions.
  */
  constructor(props) {
    super(props);
    this.state = { 
      events: [],             // List of all events
      selectedEvent: null,    // Event selected for editing
      showModal: false,       // Whether the event modal is visible
      filter: '',             // Filter for event locations
      userId: null,           // Logged-in user's ID
      user: null              // Logged-in user's details
    };
  }

  // Fetches all events from the backend
  fetchData = () => {
    fetch(`http://localhost:5000/api/events`)
      .then((response) => response.json())
      .then((data) => this.setState({ events: data }))
      .catch((error) => console.error('Error fetching events:', error));
  }

  // Lifecycle method to initialize the app's state after mounting
  componentDidMount() {
    const storedUser = JSON.parse(localStorage.getItem('user'));
    if (storedUser) {
      this.setState({ user: storedUser, userId: storedUser.id }, this.fetchData);
    }
  }

  // Handles user login by updating state and fetching events
  handleLogin = (user) => {
    this.setState({ user, userId: user.id });
    this.fetchData();
  };

  // Handles user logout by clearing state and local storage
  handleLogout = () => {
    this.setState({ user: null, userId: null });
    localStorage.removeItem('user');
  };

  // Toggles the visibility of the event modal
  toggleModal = (eventId = null) => {
    if (eventId) {
      // Fetch the event details if an event ID is provided
      fetch(`http://localhost:5000/api/events/${eventId}`)
        .then(response => response.json())
        .then(data => this.setState({ selectedEvent: data, showModal: true }))
        .catch(error => console.error('Error fetching event details:', error));
    } else {
      this.setState({ selectedEvent: null, showModal: true});
    }
  };

  // Updates the filter value for event locations
  handleFilter = (e) => {
    this.setState({ filter: e.target.value });
  };

  // Sorts events by date in ascending order
  sortEventsByDate = () => {
    const sorted = [...this.state.events].sort((a, b) => new Date(a.date) - new Date(b.date));
    this.setState({ events: sorted });
  };

  // Handles RSVP action for a specific event
  onRSVP = (eventId) => {
    fetch(`http://localhost:5000/api/events/${eventId}/rsvp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: this.state.userId })
    })
      .then((response) => response.json())
      .then(() => {
        this.fetchData();
      })
      .catch((error) => console.error('Error RSVPing:', error));
  };

  // Deletes a specific event
  deleteEvent = (eventId) => {
    fetch(`http://localhost:5000/api/events/${eventId}`, { method: 'DELETE' })
      .then(() => {
        console.log('Event deleted successfully!');
        this.fetchData();
      })
      .catch((error) => console.error('Error deleting event:', error));
  };

  // Updates events list after saving changes
  updateEvent = () => {
    this.fetchData();
  };

  render() {
    const { events, showModal, selectedEvent, filter, user } = this.state;
    
    // If user is not logged in, show the login/register page
    if (!user) {
      return (
        <Container>
          <Row>
            <Col>
              <Button onClick={() => this.setState({ showRegister: true })}>Register</Button>
            </Col>
          </Row>
          {this.state.showRegister ? (
            <Register onRegister={() => this.setState({ showRegister: false })}/>
          ) : (
            <Login onLogin={this.handleLogin}/>
          )}
        </Container>
      );
    }
    
    // Filter events based on location
    const filteredEvents = events.filter(event =>
      event.location && event.location.toLowerCase().includes(filter.toLowerCase())
    );

    return (
      <Container>
        <h1 className='text-center my-4'>Event RSVP and Attendance Tracker</h1>
        <Button color='secondary' onClick={this.handleLogout}>Logout</Button>
        <FormGroup className='mb-4 text-center'>
          <Label for='filter'>Filter by Location:</Label>
          <Input
            id='filter'
            type='text'
            placeholder='Enter location'
            value={filter}
            onChange={this.handleFilter}
            className='mb-3'
          />
          <Button color='secondary' onClick={this.sortEventsByDate}>Sort by Date</Button>{' '}
          <Button color='primary' onClick={() => this.toggleModal()}>Add New Event</Button>
        </FormGroup>
        <Row>
          {filteredEvents.map(event => (
            <Col xs='12' sm='6' lg='4' key={event.id} className='mb-4'>
              <EventDisplay 
                event={event} 
                toggleModal={() => this.toggleModal(event.id)}
                onRSVP={() => this.onRSVP(event.id)}
                onDelete={() => this.deleteEvent(event.id)} 
              />
            </Col>
          ))}
        </Row>
        {showModal && (
          <EventModal 
            isOpen={showModal}
            event={selectedEvent}
            toggle={() => this.setState({ showModal: false })}
            onSave={this.updateEvent}
          />
        )}
        <UserProfile userId={this.state.userId} refreshProfile={() => this.fetchData()}/>
      </Container>
    );
  }
}

export default App;