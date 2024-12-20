import React, { Component } from 'react';
import { Container, Row, Col, Button, Input, FormGroup, Label } from 'reactstrap';
import EventDisplay from './EventDisplay';
import EventModal from './EventModal';
import UserProfile from './UserProfile';
import './styles.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = { events: [], selectedEvent: null, showModal: false, filter: '', userId: 1 };
  }

  fetchData = () => {
    fetch(`http://localhost:5000/api/events`)
      .then((response) => response.json())
      .then((data) => this.setState({ events: data }))
      .catch((error) => console.error('Error fetching events:', error));
  }

  componentDidMount() {
    this.fetchData();
  }

  toggleModal = (eventId = null) => {
    if (eventId) {
      fetch(`http://localhost:5000/api/events/${eventId}`)
        .then(response => response.json())
        .then(data => this.setState({ selectedEvent: data, showModal: true }))
        .catch(error => console.error('Error fetching event details:', error));
    } else {
      this.setState({ selectedEvent: null, showModal: true}); // New event
    }
  };

  handleFilter = (e) => {
    this.setState({ filter: e.target.value });
  };

  sortEventsByDate = () => {
    const sorted = [...this.state.events].sort((a, b) => new Date(a.date) - new Date(b.date));
    this.setState({ events: sorted });
  };

  filterByCategory = (category) => {
    const filtered = this.state.events.filter(event => event.category === category);
    this.setState({ events: filtered });
  };

  onRSVP = (eventId) => {
    fetch(`http://localhost:5000/api/events/${eventId}/rsvp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: this.state.userId })
    })
      .then((response) => response.json())
      .then(() => this.fetchData())
      .catch((error) => console.error('Error RSVPing:', error));
  };

  deleteEvent = (eventId) => {
    fetch(`http://localhost:5000/api/events/${eventId}`, { method: 'DELETE' })
      .then(() => {
        console.log('Event deleted successfully!');
        this.fetchData();
      })
      .catch((error) => console.error('Error deleting event:', error));
  };

  updateEvent = () => {
    this.fetchData(); // Refresh event list
  };

  render() {
    const { events, showModal, selectedEvent, filter } = this.state;
    const filteredEvents = events.filter(event =>
      event.location && event.location.toLowerCase().includes(filter.toLowerCase())
    );

    return (
      <Container>
        <h1 className='text-center my-4'>Event RSVP and Attendance Tracker</h1>
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
          <Button color='secondary' onClick={() => this.filterByCategory('Workshops')}>Filter: Workshops</Button>{' '}
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
        <UserProfile userId={this.state.userId}/>
      </Container>
    );
  }
}

export default App;
