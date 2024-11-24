package confchat;

import rice.pastry.*;
import rice.pastry.socket.*;
import rice.environment.Environment;
import java.net.InetAddress;

public class PastryNodeExample {
    public static void main(String[] args) throws Exception {
        // Set up the Pastry environment
        Environment env = new Environment();

        // Create a RandomNodeIdFactory for generating unique node IDs
        NodeIdFactory nidFactory = new rice.pastry.standard.RandomNodeIdFactory(env);

        // Specify the port to bind to
        int bindPort = 9001;

        // Set up a PastryNodeFactory
        PastryNodeFactory factory = new SocketPastryNodeFactory(nidFactory, bindPort, env);

        // Create a PastryNode
        PastryNode node = factory.newNode();

        // Print the Node's ID to verify setup
        System.out.println("Created new node with ID: " + node.getId().toString());

        // Wait until the node is ready to start
        synchronized (node) {
            while (!node.isReady()) {
                node.wait(500);
            }
        }

        System.out.println("Node is ready!");

        ChatApp app = new ChatApp(node);

        // Start the command line interface
        app.startCLI();


    }
}
