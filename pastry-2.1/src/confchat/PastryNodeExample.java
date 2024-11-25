package confchat;

import rice.environment.Environment;
import rice.pastry.*;
import rice.pastry.socket.*;
import java.net.InetSocketAddress;

public class PastryNodeExample {
    public static void main(String[] args) throws Exception {
        // Create the environment
        Environment env = new Environment();
        env.getParameters().setString("loglevel", "INFO");

        // Create a NodeIdFactory for generating random node IDs
        NodeIdFactory nidFactory = new rice.pastry.standard.RandomNodeIdFactory(env);

        // Get the port from the first argument
        int bindPort = Integer.parseInt(args[0]);

        // Set up the SocketPastryNodeFactory with a binding address
        InetSocketAddress bindAddress = new InetSocketAddress("0.0.0.0", bindPort);
        SocketPastryNodeFactory factory = new SocketPastryNodeFactory(nidFactory, bindAddress.getAddress(), bindPort, env);

        // Create a PastryNode
        PastryNode node = factory.newNode();
        System.out.println("Node created with ID: " + node.getId());

        // Bootstrapping logic
        if (args.length > 1) {
            InetSocketAddress bootstrapAddress = new InetSocketAddress(args[1], Integer.parseInt(args[2]));
            System.out.println("Bootstrapping to " + bootstrapAddress);

            boolean bootstrapped = false;
            while (!bootstrapped) {
                try {
                    node.boot(bootstrapAddress);
                    synchronized (node) {
                        while (!node.isReady()) {
                            node.wait(500);
                            System.out.print(".");
                        }
                    }
                    bootstrapped = true;
                } catch (Exception e) {
                    System.out.println("Bootstrap failed, retrying in 5 seconds...");
                    Thread.sleep(5000);
                }
            }
        } else {
            System.out.println("No bootstrap node provided. Starting standalone node.");
            synchronized (node) {
                while (!node.isReady()) {
                    node.wait(500);
                    System.out.print(".");
                }
            }
        }

        System.out.println("\nNode is ready!");

        // Start your application
        SimpleChatApp app = new SimpleChatApp(node);
        app.startCLI();
    }
}
