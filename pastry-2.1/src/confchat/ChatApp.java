package confchat;

import rice.p2p.commonapi.Application;
import rice.p2p.commonapi.Endpoint;
import rice.p2p.commonapi.Message;
import rice.p2p.commonapi.RouteMessage;
import rice.p2p.commonapi.NodeHandle;
import rice.pastry.PastryNode;
import rice.pastry.Id;

import java.util.Scanner;

public class ChatApp implements Application {
    private PastryNode node;
    private Endpoint endpoint;

    public ChatApp(PastryNode node) {
        this.node = node;
        this.endpoint = node.buildEndpoint(this, "chat");
        this.endpoint.register();
    }

    @Override
    public void deliver(rice.p2p.commonapi.Id id, Message message) {
        if (message instanceof ChatMessage) {
            ChatMessage chatMessage = (ChatMessage) message;
            System.out.println("Received message from " + chatMessage.getSender() + ": " + chatMessage.getContent());
        } else {
            System.out.println("Received unknown message: " + message);
        }
    }

    @Override
    public boolean forward(RouteMessage message) {
        // Allow forwarding of messages
        return true;
    }

    @Override
    public void update(NodeHandle handle, boolean joined) {
        if (joined) {
            System.out.println("Node joined: " + handle.getId());
        } else {
            System.out.println("Node left: " + handle.getId());
        }
    }

    public void sendMessage(Id recipientId, String sender, String content) {
        ChatMessage message = new ChatMessage(sender, content);

        // Send the message to the recipient
        endpoint.route(recipientId, message, null);

        System.out.println("Sent message to " + recipientId + ": " + content);
    }

    public void startCLI() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("ChatApp CLI started. Type your messages below:");

        while (true) {
            System.out.println("Enter message (format: <recipientNodeId> <message>):");
            String input = scanner.nextLine();
            String[] parts = input.split(" ", 2);

            if (parts.length != 2) {
                System.out.println("Invalid input format. Use: <recipientNodeId> <message>");
                continue;
            }

            String recipientIdStr = parts[0];
            String messageText = parts[1];

            try {
                // Convert recipientId string to rice.pastry.Id
                Id recipientId = Id.build(recipientIdStr.getBytes());
                sendMessage(recipientId, node.getId().toString(), messageText);
            } catch (Exception e) {
                System.out.println("Failed to send message: " + e.getMessage());
            }
        }
    }
}
