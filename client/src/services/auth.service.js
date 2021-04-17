import axios from 'axios';
import authenticationHeaders from './auth-header';
const API_URL = 'http://localhost:8000/api/';

class AuthenticationService {

    login(user) {
        return axios.post(API_URL + 'log_in/', {
            email: user.email,
            password: user.password
        })
        .then(response => {
            if (response.data.access) {
                // Use localStorage to save JWT - TODO: Remove / explore alternate options due to security concerns
                console.log(JSON.stringify(response.data))
                localStorage.setItem('user', JSON.stringify(response.data));
            }
            return response.data;
        });
    }

    logout() {
        localStorage.removeItem('user')
    }

    register(user) {
        return axios.post(API_URL + 'sign_up/', {
            email: user.email,
            username: user.username,
            password1: user.password,
            password2: user.verifyPassword
        });
    }

    verifyUser() {
        // console.log(user.access)
        return axios.get(API_URL + 'current_user/', {
            headers: authenticationHeaders()
        })
        .then(response => {
            console.log('Service -', response)
            localStorage.setItem('user', JSON.stringify(response.data));
        })
    }

    refreshToken(user) {
        return axios.post(API_URL + 'token/refresh/', {
            refresh: user.refresh
        })
        .then(
            response => {
                user.access = response.data.access
                localStorage.setItem('user', JSON.stringify(user));
            }
        )
    }    
}

export default new AuthenticationService();
