// import axios from 'axios';
import { share } from 'rxjs/operators'; 
import { webSocket } from 'rxjs/webSocket'; 

// import getAccessToken from './auth.service.js';

let _socket; 
export let messages;

let accumulatedData = [];

class MessengerService { 

    connect() {
        if (!_socket || _socket.closed) {
        const user = JSON.parse(localStorage.getItem('user'));
        const token = user.access
        _socket = webSocket(`ws://localhost:8000/messenger/?token=${token}`);
        messages = _socket.pipe(share());
        messages.subscribe(message => accumulatedData.push(message));
        }
    }

    createMessage(data) {
        console.log('createMessage', data)
        this.connect();
        const message = {
            type: 'create.message',
            data: data
        };
        _socket.next(message);
    }

    messageThread() {
        return accumulatedData
    }
}

export default new MessengerService();
