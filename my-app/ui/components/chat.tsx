'use client';

import * as React from 'react';

import { Send } from 'lucide-react';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import axios from 'axios';
import { ScrollArea } from '@/components/ui/scroll-area';

interface ChatCardProps {
  sessionId: string;
}

export function ChatCard({ sessionId }: ChatCardProps) {
  const [namespace, setNamespace] = React.useState('');
  const [mode, setMode] = React.useState('query');
  const [loading, setLoading] = React.useState(false);
  const [placeholder, setPlaceholder] = React.useState('Ask question');
  const [messages, setMessages] = React.useState([
    {
      role: 'agent',
      content:
        'Hi, I am an AI Assistant. Start by adding data or asking questions.',
    },
  ]);

  const sendQuery = async (
    query: string,
    sessionId: string,
    namespace: string
  ) => {
    try {
      const response = await axios.get(
        `/api/v1/chat?query=${query}&session_id=${Date.now().toString()}&namespace=${namespace}`
      );
      setMessages((prevMessages) => [
        ...prevMessages, // Spread the previous messages
        {
          role: 'agent',
          content: response?.data?.response,
        },
      ]);
    } catch (error) {
      console.log('Error getting response from bot. Please try again.');
    }
  };

  const sendAddData = async (
    query: string,
    sessionId: string,
    namespace: string
  ) => {
    const payload = {
      session_id: sessionId,
      source: query,
      // If namespace is not provided, we default to "", which is the default ns in pinecone
      namespace: namespace ?? '',
    };

    try {
      const response = await axios.post('/api/v1/add', payload);
      setMessages((prevMessages) => [
        ...prevMessages, // Spread the previous messages
        {
          role: 'agent',
          content: response?.data?.message,
        },
      ]);
    } catch (error) {
      console.log('Error getting response from bot. Please try again.');
    }
  };

  const sendChatMessage = async (
    query: string,
    sessionId: string,
    namespace: string
  ) => {
    if (mode === 'add') {
      await sendAddData(query, sessionId, namespace);
    } else {
      await sendQuery(query, sessionId, namespace);
    }
  };

  const onModeChange = async () => {
    if (mode === 'add') {
      setPlaceholder('Ask question');
      setMode('query');
    } else {
      setPlaceholder('Add data (enter text or url)');
      setMode('add');
    }
  };

  return (
    <>
      <Card>
        <ScrollArea className='mt-6 h-[60vh] max-h-[calc(100vh - 200px)]'>
          <CardContent>
            <div className='space-y-4'>
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={cn(
                    'flex w-fit max-w-[75%] flex-col gap-2 rounded-lg px-3 py-2 text-sm',
                    message.role === 'user'
                      ? 'ml-auto bg-primary text-primary-foreground'
                      : 'bg-muted'
                  )}
                >
                  {message.content}
                </div>
              ))}
            </div>
          </CardContent>
        </ScrollArea>
        <CardFooter className='bottom-0 my-4'>
          <form
            onSubmit={async (event: any) => {
              event.preventDefault();
              const currentMessage = event.currentTarget.message.value;
              event.target.message.value = '';
              if (currentMessage === '') {
                return;
              }
              setMessages([
                ...messages,
                {
                  role: 'user',
                  content: currentMessage,
                },
              ]);

              await sendChatMessage(currentMessage, sessionId, namespace);
            }}
            className='w-full'
          >
            <div className='flex items-center w-full space-x-2'>
              <div className='flex flex-col items-center'>
                <div className='flex items-center'>
                  <Switch onCheckedChange={onModeChange} />
                </div>
                <label className='text-[9px] mt-1 text-muted-foreground'>
                  mode: {mode}
                </label>
              </div>
              <Input
                id='message'
                placeholder={placeholder}
                className='flex-1'
                autoComplete='off'
                disabled={loading}
              />
              <Button type='submit' size='icon'>
                <Send className='w-4 h-4' />
                <span className='sr-only'>Send</span>
              </Button>
            </div>

            <Input
              id='namespace'
              placeholder='namespace'
              className='w-[200px]'
              autoComplete='off'
              value={namespace}
              onChange={(event) => setNamespace(event.target.value)}
            />
          </form>
        </CardFooter>
      </Card>
    </>
  );
}
