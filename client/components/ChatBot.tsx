"use client"
import React, { useState } from 'react';

interface Message {
    text: string;
    sender: 'user' | 'bot';
}

const ChatBot = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState('');

    const sendMessage = () => {
        if (inputText.trim()) {
            setMessages([...messages, { text: inputText, sender: 'user' }]);
            setInputText('');
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    const addBotMessage = (text: string) => {
        setMessages([...messages, { text, sender: 'bot' }]);
    };

    return (
        <div className="w-full h-screen bg-gray-200 flex flex-col">
            <div className="flex-1 p-4 overflow-y-scroll">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`bg-white p-3 rounded-lg mb-2 ${
                            message.sender === 'user' ? 'ml-auto' : ''
                        }`}
                    >
                        {message.text}
                    </div>
                ))}
            </div>
            <div className="p-4 flex items-center">
                <input
                    className="border border-gray-300 p-2 rounded-lg flex-1"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyPress={handleKeyPress}
                />
                <button
                    className="bg-blue-500 text-white p-3 rounded-lg ml-4"
                    onClick={sendMessage}
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default ChatBot;