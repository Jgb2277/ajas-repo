import React, { useState, useEffect, useContext, useRef } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { io } from 'socket.io-client';

export default function LiveChat() {
    const { user } = useContext(AuthContext);
    const [socket, setSocket] = useState(null);
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Initializing socket connection
        const newSocket = io('http://localhost:5000');
        setSocket(newSocket);

        // Initial load history
        newSocket.on('chat_history', (history) => {
            setMessages(history);
        });

        // Real-time listener
        newSocket.on('new_message', (message) => {
            setMessages((prev) => [...prev, message]);
        });

        return () => newSocket.close();
    }, []);

    // Auto-scroll to bottom of chat list
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    const sendMessage = (e) => {
        e.preventDefault();
        if (inputMessage.trim() && socket) {
            socket.emit('send_message', {
                user_id: user.id,
                content: inputMessage
            });
            setInputMessage('');
        }
    };

    return (
        <div style={{ height: 'calc(100vh - 180px)', display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ marginBottom: '1rem', color: 'var(--text-dark)' }}>Live Student Chat Room</h3>
            <div className="chat-container">
                <div className="chat-messages">
                    {messages.map((msg, index) => {
                        const isMine = msg.user === user.name;
                        return (
                            <div key={index} className={`message ${isMine ? 'message-mine' : 'message-other'}`}>
                                <div className="message-sender">{msg.user} • {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                                <div>{msg.content}</div>
                            </div>
                        );
                    })}
                    <div ref={messagesEndRef} />
                </div>
                <form className="chat-input" onSubmit={sendMessage}>
                    <input
                        type="text"
                        placeholder="Type your message to the class..."
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                    />
                    <button type="submit">Send</button>
                </form>
            </div>
        </div>
    );
}
