import AuthenticationService from '../../services/auth.service';

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
                }
            );
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
                }
            )
        },
        initializeAuthAction() {
            const user = JSON.parse(localStorage.getItem('user'));
            AuthenticationService.verifyUser(user).then(
                response => {
                    console.log('Response:', response);
                },
                error => {
                    console.log('Error:', error);
                    AuthenticationService.refreshToken(user).then(
                        AuthenticationService.verifyUser(user)
                        // response => { 
                        //     console.log('Checking refreshToken', response);
                             
                        // }
                    )
                }
            )

            // if (user) {
            //     commit('setAuthStatus', true);
            // } else {
            //     AuthenticationService.verifyUser
            // }
            // if (localStorage.getItem('user')) {
            //   state.isAuthenticated = true;
            // } else {
            //     state.isAuthenticated = false;
            // }
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
            state.isAuthenticated = payload;
        },
        initializeAuth(state) {
            if (localStorage.getItem('user')) {
                // console.log(localStorage.getItem('user'))
              state.isAuthenticated = true;
            } else {
                state.isAuthenticated = false;
            }
        }
    }
}