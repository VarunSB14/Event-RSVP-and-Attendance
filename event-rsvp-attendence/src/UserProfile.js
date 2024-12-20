import React, { Component } from 'react';

class UserProfile extends Component {
    constructor(props) {
        super(props);
        this.state = { user: null, rsvps: [] };
    }

    componentDidMount() {
        this.fetchDetails();
        this.fetchRSVPs();
    }

    fetchDetails = () => {
        fetch(`http://localhost:5000/api/users/${this.props.userId}`)
            .then(response => response.json())
            .then(data => this.setState({ user: data }))
            .catch(error => console.error('Error fetching user details:', error));
    };

    fetchRSVPs = () => {
        fetch(`http://localhost:5000/api/users/${this.props.userId}/rsvps`)
            .then(response => response.json())
            .then(data => this.setState({ rsvps: data }))
            .catch(error => console.error('Error fetching user RSVPs:', error));
    };

    render() {
        const { user, rsvps } = this.state;
        if (!user) return <p>Loading user profile...</p>;
        
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