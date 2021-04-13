import axios from 'axios';

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

}

export default new AuthenticationService();
