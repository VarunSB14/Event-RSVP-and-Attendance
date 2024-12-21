import React, { Component } from 'react';
import { Button, Form, Input } from 'reactstrap';

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = { email: '', password: '' };
    }

    handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.state)
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.id) {
                    localStorage.setItem('user', JSON.stringify(data));
                    this.props.onLogin(data);
                } else {
                    alert(data.message);
                }
            })
            .catch((error) => console.error('Error logging in:', error));
    };

    render() {
        return (
            <Form onSubmit={this.handleSubmit}>
                <Input type='email' placeholder='Email' onChange={(e) => this.setState({ email: e.target.value })}/>
                <Input type='password' placeholder='Password' onChange={(e) => this.setState({ password: e.target.value })}/>
                <Button type='submit'>Login</Button>
            </Form>
        );
    }
}

export default Login;
