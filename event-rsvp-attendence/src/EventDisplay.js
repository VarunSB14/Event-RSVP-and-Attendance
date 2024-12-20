import React, { Component } from 'react';
import { Card, CardBody, CardTitle, Button } from 'reactstrap';

class EventDisplay extends Component {
    handleViewAttendees = () => {
        fetch(`http://localhost:5000/api/events/${this.props.event.id}/rsvp`)
            .then(response => response.json())
            .then(data => alert(`Attendees: ${data.map(rsvp => rsvp.name).join(', ')}`))
            .catch(error => console.error('Error fetching RSVPs:', error));
    };
    
    render()  {
        const { event, toggleModal, onRSVP, onDelete } = this.props;
        const { title, date, time, location, capacity, available_spots } = event;

        return (
            <Card className='text-center'>
                <CardBody>
                    <CardTitle tag='h5'>{title}</CardTitle>
                    <p>Date: {date}</p>
                    <p>Time: {time}</p>
                    <p>Location: {location}</p>
                    <p>Available Spots {available_spots}/{capacity}</p>
                    <div>
                        <Button color='primary' onClick={onRSVP}>RSVP</Button>
                        <Button color='info' onClick={toggleModal}>Edit</Button>
                        <Button color='warning' onClick={this.handleViewAttendees}>View Attendees</Button>{' '}
                        <Button color='danger' onClick={onDelete}>Delete Event</Button>
                    </div>
                </CardBody>
            </Card>
        );
    }
}

export default EventDisplay;