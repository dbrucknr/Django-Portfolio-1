export default function authenticationHeaders() {
    let userData = JSON.parse(localStorage.getItem('user'));

    if (userData && userData.access) {
        return { Authorization: 'Bearer' + userData.access }
    } else {
        return {}
    }
}