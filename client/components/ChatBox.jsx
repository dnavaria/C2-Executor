"use client"
import React, {useState, useRef, useEffect} from 'react';
import {Button} from "@/components/ui/button"
import {Input} from "@/components/ui/input"
import supabase_client from "@/services/supabase_service";
import {useRouter} from "next/navigation";

const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const messagesEndRef = useRef(null);


    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const handleSendMessage = () => {
        if (input.trim() === '') return;

        // make a post request to the c2-api-server
        fetch('http://localhost:11999/api/v1/command/run', {
            method: 'POST',
            body: JSON.stringify({
                command_text: input
            }),
            headers: {
                'Content-Type': 'application/json'
            },
        }).then((response) => {
            if (response.status === 200) {
                setInput('');
            }
        });

        // const newMessage = {
        //     command_text: input,
        //     isUser: true,
        // };

        // Create a new array with the user's message
        // const updatedMessages = [...messages, newMessage];

        // Update the 'messages' state with the user's message
        // setMessages(updatedMessages);
        //
        // setInput('');

        // // Simulate a bot response after a delay (e.g., 2 seconds)
        // setTimeout(() => {
        //     const botMessage: Command = {
        //         id: updatedMessages.length,
        //         content: 'Hello from the bot',
        //         isUser: false,
        //     };

        // Create a new array with the bot's reply and the existing messages
        // const updatedMessagesWithBot = [...updatedMessages, botMessage];

        // Update the 'messages' state with the bot's reply
        // setMessages(updatedMessagesWithBot);

        // Scroll to the bottom of the chat window
        // if (messagesEndRef.current) {
        //     messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
        // }
        // }, 2000);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    }

    const fetchMessages = async () => {
        try {
            const {data: commands, error: postgrestError} = await supabase_client
                .from('c2_executor')
                .select('*')
                .order('created_at', {ascending: false})
                .limit(10);

            if (postgrestError) {
                console.error(postgrestError);
                return;
            }

            // sort the messages by created_at
            // const newMessages = commands.sort((a, b) => {
            //     return new Date(a.created_at) - new Date(b.created_at);
            // }).map((command) => {
            //     return {
            //         task_id: command.task_id,
            //         command_text: command.command_text,
            //         isUser: true,
            //         status: command.status,
            //         result: command.result
            //     };
            // });

            // from each message take the command_text and create a new message where isUser is true
            // and add another entry for the result where isUser is false
            // sort the messages by created_at
            const newMessages = commands.sort((a, b) => {
                return new Date(a.created_at) - new Date(b.created_at);
            }).reduce((acc, command) => {
                acc.push({
                    task_id: command.task_id,
                    command_text: command.command_text,
                    isUser: true,
                    status: command.status,
                    result: command.result
                });
                acc.push({
                    task_id: command.task_id,
                    command_text: command.command_text,
                    isUser: false,
                    status: command.status,
                    result: command.result.split("\n").map((line) => {
                        return <div>{line}</div>
                    }, [])
                });
                return acc;
            }, []);


            if (JSON.stringify(newMessages) !== JSON.stringify(messages)) {
                setMessages(newMessages);
            }
        } catch (error) {
            console.error(error);
        }
    }

    const handleUpdates = (payload) => {
        console.log(payload);
    }
    const router = useRouter();

    useEffect(() => {
        const interval = setInterval(() => {
            fetchMessages();
        }, 2000);

        return () => clearInterval(interval);
    }, [messages]); // Dependency on 'messages'


    return (
        <div className="max-w-6xl h-screen flex flex-col mx-auto mt-2">
            <div className="flex-1 p-4 overflow-y-scroll border rounded-2xl">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`${
                            message.isUser ? 'text-right' : 'text-left'
                        } mb-2`}
                    >
                        <div
                            className={`${
                                message.isUser
                                    ? 'bg-blue-500 text-white rounded-tl-lg rounded-br-lg rounded-tr-lg'
                                    : 'bg-green-300 rounded-tl-lg rounded-bl-lg rounded-br-lg'
                            } p-2 inline-block max-w-xs`}
                        >
                            {message.isUser ? message.command_text : message.result}
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef}/>
            </div>

            <div className="p-4 flex items-center">
                <Input
                    className="border border-gray-300 p-2 rounded-lg flex-1 bg-white"
                    placeholder={"Type a command..."}
                    value={input}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyPress}
                />
                <Button
                    className="p-5 text-lg rounded-lg ml-4"
                    onClick={handleSendMessage}
                >
                    Send
                </Button>
            </div>
        </div>
    );
};

export default ChatBox;
