import React, { Component } from 'react';

class UserProfile extends Component {
    constructor(props) {
        super(props);
        this.state = { user: null, rsvps: [] };
    }

    componentDidMount() {
        fetch(`http://localhost:5000/api/users/${this.props.userId}`)
            .then(response => response.json())
            .then(data => this.setState({ user: data, rsvps: data.rsvps || [] }))
            .catch(error => console.error('Error fetching user profile:', error));
    }

    render() {
        const { user, rsvps } = this.state;
        if (!user) {
            return (
                <div>
                    <p>Error loading user profile.</p>
                    <button onClick={this.componentDidMount}>Retry</button>
                </div>

            );
        }
        
        return (
            <div className='user-profile'>
                <h2>{user.name}'s Profile</h2>
                <h4>Email: {user.email}</h4>
                <h4>RSVP'd Events:</h4>
                {rsvps.length > 0 ? (
                    <ul>
                        {rsvps.map(event => (
                            <li key={event.id}>
                                <strong>{event.title}</strong> on {event.date} at {event.time}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No events RSVP'd yet.</p>
                )}
            </div>
        );
    }
}

export default UserProfile;