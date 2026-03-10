from flask_socketio import emit
from models import db, Message, User

def init_socket_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print("Client connected to chat")
        # Load last 50 messages
        messages = Message.query.order_by(Message.timestamp.desc()).limit(50).all()
        messages.reverse()
        
        chat_history = []
        for msg in messages:
            chat_history.append({
                'id': msg.id,
                'user': msg.user.name,
                'content': msg.content,
                'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        emit('chat_history', chat_history)
        
    @socketio.on('send_message')
    def handle_message(data):
        user_id = data.get('user_id')
        content = data.get('content')
        
        user = User.query.get(user_id)
        if user and content:
            new_msg = Message(user_id=user_id, content=content)
            db.session.add(new_msg)
            db.session.commit()
            
            emit('new_message', {
                'id': new_msg.id,
                'user': user.name,
                'content': new_msg.content,
                'timestamp': new_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }, broadcast=True)
            
    @socketio.on('disconnect')
    def handle_disconnect():
        print("Client disconnected")
