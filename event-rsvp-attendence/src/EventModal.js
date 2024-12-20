import React, { Component } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter, Button, Form, FormGroup, Label, Input } from 'reactstrap';

class EventModal extends Component {
    constructor(props) {
        super(props);
        this.state = { ...props.event || { title: '', description: '', date: '',  time: '', location: '', capacity: 50, category: 'Workshops' } };
    }

    handleChange = (e) => {
        const { name, value } = e.target;
        this.setState({ [name]: value });
    };

    handleSave = () => {
        const { title, date, time, location } = this.state;
        if (!title || !date || !time || !location) {
            alert('Please fill in all required fields!');
            return;
        }

        const isNew = !this.props.event?.id; // Check if it's a new event
        const url = isNew ? `http://localhost:5000/api/events` : `http://localhost:5000/api/events/${this.props.event.id}`;
        const method = isNew ? 'POST' : 'PUT';

        fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.state)
        })
            .then(response => response.json())
            .then(() => {
                console.log(isNew ? 'Event created successfully!': 'Event updated successfully!');
                this.props.toggle();
                this.props.onSave(); // Refresh events
            })
            .catch(error => console.error('Error saving event:', error));
    };

    render() {
        const { isOpen, toggle } = this.props;
        const { title, description, date, time, location, capacity, category } = this.state;

        return (
            <Modal isOpen={isOpen} toggle={toggle}>
                <ModalHeader toggle={toggle}>{this.props.event?.id ? 'Edit Event': 'Add New Event'}</ModalHeader>
                <ModalBody>
                    <Form>
                        <FormGroup>
                            <Label for='title'>Title</Label>
                            <Input id='title' name='title' value={title} onChange={this.handleChange}/>
                        </FormGroup>
                        <FormGroup>
                            <Label for='description'>Description</Label>
                            <Input id='description' name='description' value={description} onChange={this.handleChange}/>
                        </FormGroup>
                        <FormGroup>
                            <Label for='category'>Category</Label>
                            <Input id='category' name='category' type='select' value={category} onChange={this.handleChange}>
                                <option>Workshops</option>
                                <option>Meetups</option>
                                <option>Conferences</option>
                            </Input>
                        </FormGroup>
                        <FormGroup>
                            <Label for='date'>Date</Label>
                            <Input id='date' name='date' type='date' value={date} onChange={this.handleChange}/>
                        </FormGroup>
                        <FormGroup>
                            <Label for='time'>Time</Label>
                            <Input id='time' name='time' type='time' value={time} onChange={this.handleChange}/>
                        </FormGroup>
                        <FormGroup>
                            <Label for='location'>Location</Label>
                            <Input id='location' name='location' value={location} onChange={this.handleChange}/>
                        </FormGroup>
                        <FormGroup>
                            <Label for='capacity'>Capacity</Label>
                            <Input id='capacity' name='capacity' type='number' value={capacity} onChange={this.handleChange}/>
                        </FormGroup>
                    </Form>
                </ModalBody>
                <ModalFooter>
                    <Button color="secondary" onClick={toggle}>Cancel</Button>
                    <Button color="primary" onClick={this.handleSave}>Save</Button>
                </ModalFooter>
            </Modal>
        );
    }
}

export default EventModal;