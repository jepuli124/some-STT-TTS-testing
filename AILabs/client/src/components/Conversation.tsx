import { useConversation } from "@elevenlabs/react";
import { useCallback } from "react";


async function getToken(): Promise<string> {
  const response = await fetch("/api/token");
  if (!response.ok) {
    throw Error("Failed to get conversation token");
  }
  const data = await response.json();
  return data.token;
}

export function MyConversationComponent() {
  const conversation = useConversation({
    onConnect: () => console.log("Connected"),
    onDisconnect: () => console.log("Disconnected"),
    onError: (error: string) => console.error("Error:", error),
  });

  const startConversation = useCallback(async () => {
    await navigator.mediaDevices.getUserMedia({ audio: true });
    const token = await getToken();
    await conversation.startSession({ conversationToken: token });
  }, [conversation]);

  const stopConversation = useCallback(async () => {
    await conversation.endSession();
  }, [conversation]);
  
  return (
    <div>
      <p>Status: {conversation.status}</p>
      <button onClick={startConversation} disabled={conversation.status === "connected"}>
        Start conversation
      </button>
      <button onClick={stopConversation} disabled={conversation.status !== "connected"}>
        End conversation
      </button>
    </div>
  );
}
