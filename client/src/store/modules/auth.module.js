import router from '../../router';
import AuthenticationService from '../../services/auth.service';
import { isValidJwt } from '../../utils/validJWT';

export const authentication = {
    namespaced: true,
    state: {
        user: localStorage.getItem('user'),
        isAuthenticated: false,
    },
    actions: {
        login({ commit }, user) {
            return AuthenticationService.login(user).then(
                user => {
                    commit('loginSuccess', user);
                    return Promise.resolve(user);
                },
                error => {
                    commit('loginFailure');
                    return Promise.reject(error);
                });
        },
        logout({ commit }) {
            AuthenticationService.logout();
            commit('logout');
        },
        register({ commit }, user) {
            return AuthenticationService.register(user).then(
                response => {
                    commit('registerSuccess');
                    return Promise.resolve(response.data);
                },
                error => {
                    commit('registerFailure');
                    return Promise.reject(error);
                });
        },
        initializeAuthAction({ commit, dispatch }) {
            // Check for user object in local storage
            const user = JSON.parse(localStorage.getItem('user'));
            // If there is no user object - set Auth to false
            if (!user) {
                commit('setAuthStatus', false);
                router.replace('/login');
                return
            }
            // If there is a user object - examine the token
            const expirationCheck = isValidJwt(user.access);
            console.log('valid token? - ', expirationCheck)
            // If the token fails to validate dispatch action that attempts to verify user:
            if (!expirationCheck) {
                dispatch('verifyUserToken', user);
                return
            }
            // Otherwise set the data once more in localstorage and update auth status
            commit('setAuthStatus', true);
            localStorage.setItem('user', JSON.stringify(user));
        },
        verifyUserToken({ commit, dispatch }, user) {
            // Called on app load / page load from initialize auth action
            // Attempts to verify a user when a token is discovered, but is invalid (expired)
            return AuthenticationService.verifyUser(user).then(
                response => {
                    // If the user is returned from the API as a valid user - update state / local storage
                    console.log('User Token Valid...Response:', response);
                    localStorage.setItem('user', JSON.stringify(user));
                    commit('setAuthStatus', true);
                },
                error => {
                    // If the user is not validated by the API - dispatch a token refresh command
                    console.log('Error:', error);
                    dispatch('refreshUserToken', user);
                    
                    // localStorage.removeItem('user');
                    // commit('setAuthStatus', false);
                }
            )
        },
        refreshUserToken({ commit }, user) {
            // Called when verifyUserToken's Authentication services recieves an error response from backend 
            return AuthenticationService.refreshToken(user).then(
                response => {
                    // if no error is detected - set auth status and local storage
                    console.log('Checking refreshToken', response);
                    commit('setAuthStatus', true);
                    localStorage.setItem('user', JSON.stringify(user))
                },
                error => {
                    // on error, clear data and set state(s)
                    // Send user to login page
                    console.log(error) 
                    localStorage.removeItem('user');
                    commit('setAuthStatus', false);
                    router.replace('/login');
                }
            )
        }
    },
    mutations: {
        loginSuccess(state, user) {
            state.isAuthenticated = true;
            state.user = user;
        },
        loginFailure(state) {
            state.isAuthenticated = false;
            state.user = null;
        },
        logout(state) {
            state.isAuthenticated = false;
            state.user = null;
        },
        registerSuccess(state) {
            state.isAuthenticated = false;
        },
        registerFailure(state) {
            state.isAuthenticated = false;
        },
        setAuthStatus(state, payload) {
            console.log('setAuthStatus', payload)
            state.isAuthenticated = payload;
        }
    },
    getters: {
        user(state) {
            return state.user
        },
        isAuthenticated(state) {
            return state.isAuthenticated
        }
    }
}