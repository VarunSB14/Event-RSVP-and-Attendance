import React, { Component } from 'react';
import { Card, CardBody, CardTitle, Button, Modal, ModalHeader, ModalBody } from 'reactstrap';

class EventDisplay extends Component {
    /**
     * Component to display individual event details and related actions.
     * Allows users to RSVP, edit, view attendees, and delete events.
     */
    constructor(props) {
        super(props);
        this.state = { openModal: false, attendees: [] };
    }

    // Toggles the modal visibility for viewing attendees
    toggleModal = () =>  {
        this.setState({ openModal: !this.state.openModal });    // Local state for attendees and modal visibility
    };

    // Fetches and displays the list of attendees for the event
    handleViewAttendees = () => {
        fetch(`http://localhost:5000/api/events/${this.props.event.id}/rsvp`)
            .then(response => response.json())
            .then(data => this.setState({ attendees: data }, this.toggleModal))
            .catch(error => console.error('Error fetching RSVPs:', error));
    };
    
    render()    {
        const { event, toggleModal, onRSVP, onDelete } = this.props;
        const { attendees, openModal } = this.state;

        return  (
            <Card className='text-center'>
                <CardBody>
                    <CardTitle tag='h5'>{event.title}</CardTitle>
                    <p>Date: {event.date}</p>
                    <p>Time: {event.time}</p>
                    <p>Location: {event.location}</p>
                    <p>Available Spots {event.available_spots}/{event.capacity}</p>
                    <div>
                        <Button color='primary' onClick={onRSVP}>RSVP</Button>{' '}
                        <Button color='info' onClick={toggleModal}>Edit</Button>{' '}
                        <Button color='warning' onClick={this.handleViewAttendees}>View Attendees</Button>{' '}
                        <Button color='danger' onClick={onDelete}>Delete Event</Button>
                    </div>
                </CardBody>
                <Modal isOpen={openModal} toggle={this.toggleModal}>
                    <ModalHeader toggle={this.toggleModal}>Attendees</ModalHeader>
                    <ModalBody>
                        {attendees.length > 0 ? (
                            <ul>
                                {attendees.map((attendee, index) => (
                                    <li key={index}>{attendee.name}</li>
                                ))}
                            </ul>
                        ) : (
                            <p>No attendees yet.</p>
                        )}
                    </ModalBody>
                </Modal>
            </Card>
        );
    }
}

export default EventDisplay;