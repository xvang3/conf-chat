package confchat;

import rice.p2p.commonapi.Message;
import java.io.Serializable;

public class ChatMessage implements Message, Serializable {
    private String sender;
    private String content;

    public ChatMessage(String sender, String content) {
        this.sender = sender;
        this.content = content;
    }

    public String getSender() {
        return sender;
    }

    public String getContent() {
        return content;
    }

    @Override
    public int getPriority() {
        // Define message priority (0 is highest priority)
        return Message.LOW_PRIORITY;
    }

    @Override
    public String toString() {
        return "[" + sender + "]: " + content;
    }
}
