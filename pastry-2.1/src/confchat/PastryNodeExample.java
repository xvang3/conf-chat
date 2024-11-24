package confchat;

import rice.environment.Environment;
import rice.p2p.commonapi.*;
import rice.pastry.*;
import rice.pastry.socket.*;

import java.io.IOException;
import java.net.InetAddress;

public class PastryNodeExample {
    public static void main(String[] args) throws IOException {
        // Port to bind to
        int bindport = 9001;


        // Host for the node
        InetAddress host = InetAddress.getLocalHost();
        int bootPort = 9001;


        // Create an Environment instance (required for FreePastry)
        Environment env = new Environment();


        // Create node and bootstrap using the Environment
        NodeIdFactory nidFactory = new rice.pastry.standard.RandomNodeIdFactory(env);
        SocketPastryNodeFactory factory = new SocketPastryNodeFactory(nidFactory, bindport, env);
        PastryNode node = factory.newNode();

        System.out.println("Created new node with ID:  " + node.getId().toStringFull());

    }
}
