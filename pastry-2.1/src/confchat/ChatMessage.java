package confchat;

import rice.p2p.commonapi.Message;
import java.io.Serializable;

public class ChatMessage implements Message, Serializable {
    private final String sender;
    private final String content;

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
        return Message.LOW_PRIORITY;
    }
}
