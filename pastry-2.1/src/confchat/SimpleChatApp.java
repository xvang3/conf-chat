package confchat;

import rice.p2p.commonapi.Application;
import rice.p2p.commonapi.Endpoint;
import rice.p2p.commonapi.Message;
import rice.p2p.commonapi.Node;
import rice.p2p.commonapi.RouteMessage;
import rice.p2p.commonapi.NodeHandle;

public class SimpleChatApp implements Application {
    private Endpoint endpoint;

    public SimpleChatApp(Node node) {
        this.endpoint = node.buildEndpoint(this, "SimpleChatApp");
        this.endpoint.register();
    }

    @Override
    public void deliver(rice.p2p.commonapi.Id id, Message message) {
        System.out.println("Received message: " + message);
    }

    @Override
    public boolean forward(RouteMessage message) {
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

    public void startCLI() {
        System.out.println("SimpleChatApp running. Add more functionality here.");
    }
}
