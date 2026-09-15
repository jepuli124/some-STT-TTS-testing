
import { ConversationProvider } from '@elevenlabs/react';
import { MyConversationComponent } from './components/Conversation';



export default function App() {
  

  return (
    <ConversationProvider>
      <MyConversationComponent></MyConversationComponent>
    </ConversationProvider>
  );
}
