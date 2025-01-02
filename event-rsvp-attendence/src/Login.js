import React, { Component } from 'react';
import { Button, Form, Input } from 'reactstrap';

class Login extends Component {
    /**
     * Component to handle user login.
     * Allows users to log in with email and password.
     */
    constructor(props) {
        super(props);
        this.state = { email: '', password: '' };   // Initialize form state
    }

    // Handles form submission for login
    handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.state)  // Send email and password  
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.id) {
                    // Save user data and invoke login callback
                    localStorage.setItem('user', JSON.stringify(data));
                    this.props.onLogin(data);
                } else {
                    alert(data.message);    // Show error message on failure
                }
            })
            .catch((error) => console.error('Error logging in:', error));
    };

    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <Input type='email' placeholder='Email' onChange={(e) => this.setState({ email: e.target.value })}/>
                <Input type='password' placeholder='Password' onChange={(e) => this.setState({ password: e.target.value })}/>
                <Button type='submit' color='primary'>Login</Button>
            </Form>
        );
    }
}

export default Login;
