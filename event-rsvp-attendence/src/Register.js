import React, { Component } from 'react';
import { Button, FormGroup, Input, Label, Form } from 'reactstrap';

class Register extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            email: '',
            password: '',
            confirmPassword: ''
        };
    }

    handleSubmit = (e) => {
        e.preventDefault();
        const { name, email, password, confirmPassword } = this.state;

        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        fetch(`http://localhost:5000/api/users`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.message === 'User registered successfully') {
                    alert('User registered successfully')
                    this.props.onRegister();
                } else {
                    alert(data.message);
                }
            })
            .catch((error) => console.error('Error registering user:', error));
    };

    handleChange = (e) => {
        const { name, value } = e.target;
        this.setState({ [name]: value });
    }

    render() {
        const { name, email, password, confirmPassword } = this.state;

        return (
            <Form onSubmit={this.handleSubmit}>
                <FormGroup>
                    <Label for='name'>Name</Label>
                    <Input
                        type='text'
                        name='name'
                        id='name'
                        value={name}
                        onChange={this.handleChange}
                        required
                    />
                </FormGroup>
                <FormGroup>
                    <Label for='email'>Email</Label>
                    <Input
                        type='email'
                        name='email'
                        id='email'
                        value={email}
                        onChange={this.handleChange}
                        required
                    />
                </FormGroup>
                <FormGroup>
                    <Label for='password'>Password</Label>
                    <Input
                        type='password'
                        name='password'
                        id='password'
                        value={password}
                        onChange={this.handleChange}
                        required
                    />
                </FormGroup>
                <FormGroup>
                    <Label for='confirmPassword'>Confirm Password</Label>
                    <Input
                        type='password'
                        name='confirmPassword'
                        id='confirmPassword'
                        value={confirmPassword}
                        onChange={this.handleChange}
                        required
                    />
                </FormGroup>
                <Button type='submit' color='primary'>Register</Button>
            </Form>
        );
    }
}

export default Register;